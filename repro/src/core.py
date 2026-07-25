"""Core ULSE implementation for arXiv 2508.12674 reproduction.

Implements ULSE-n1 and ULSE-n2 exactly as defined in the paper and the official
code (github.com/hisanor013/ULSE). Uses eigendecomposition of L L^T for
numerical stability with large graphs.

Key formula derivation:
  From the SVD L = U Sigma V^T, we have V^(t) = L^(t) U Sigma^{-1} (block-wise).
  So the ULSE-n1 embedding simplifies:
    Y^(t) = V^(t) Sigma^{1/2} - U Sigma^{-1/2}
          = L^(t) U Sigma^{-1/2} - U Sigma^{-1/2}
          = (L^(t) - I) U Sigma^{-1/2}
  And ULSE-n2:
    Y^(t) = V^(t) Sigma^{1/2} = L^(t) U Sigma^{-1/2}
  Both avoid computing V directly.
"""

from __future__ import annotations

import numpy as np
from scipy.linalg import eigh


# ---------------------------------------------------------------------------
# DSBM generator
# ---------------------------------------------------------------------------

def dsbm(
    n: int,
    K: int,
    T: int,
    B_list: list[np.ndarray] | None = None,
    rho: float = 1.0,
    pi: np.ndarray | None = None,
    rng: np.random.Generator | None = None,
    labels: np.ndarray | None = None,
) -> tuple[list[np.ndarray], np.ndarray]:
    """Generate a dynamic stochastic block model.

    P_{ij}^{(t)} = rho * B^{(t)}[z_i, z_j] with symmetric B^{(t)}.
    Returns list of T adjacency matrices and (T, n) label array.
    """
    if rng is None:
        rng = np.random.default_rng()
    if pi is None:
        pi = np.ones(K) / K
    if labels is None:
        labels = rng.choice(K, size=n, p=pi)
    if B_list is None:
        B_list = [np.full((K, K), 0.1) for _ in range(T)]

    adj_list = []
    for t in range(T):
        B = B_list[t]
        P = rho * B[np.ix_(labels, labels)]
        P = np.maximum(P, 0)
        np.fill_diagonal(P, 0)
        upper = rng.random((n, n)) < P
        A = np.zeros((n, n), dtype=float)
        A[upper] = 1.0
        A = A + A.T
        adj_list.append(A)

    label_arr = np.tile(labels, (T, 1))
    return adj_list, label_arr


def make_B_matrices(K: int, T: int, p: float = 0.5, q: float = 0.1) -> list[np.ndarray]:
    """Create B^(t) matrices for a DSBM with a merging pattern.

    t=0: all communities distinct. t=1: communities 0,1 merge. t>=2: 1,2 merge.
    """
    B_list = []
    for t in range(T):
        B = np.full((K, K), q)
        np.fill_diagonal(B, p)
        if t == 1 and K >= 2:
            B[0, 1] = B[1, 0] = p
        if t >= 2 and K >= 3:
            B[1, 2] = B[2, 1] = p
        B_list.append(B)
    return B_list


# ---------------------------------------------------------------------------
# Normalized Laplacians
# ---------------------------------------------------------------------------

def n1_laplacian(A: np.ndarray, reg: float = 0.1) -> np.ndarray:
    """ULSE-n1 normalization: L = I - D_r^{-1/2} A D_r^{-1/2}, D_r = D + reg*I."""
    n = A.shape[0]
    degrees = A.sum(axis=1) + reg
    D_inv_sqrt = np.diag(1.0 / np.sqrt(degrees))
    return np.eye(n) - D_inv_sqrt @ A @ D_inv_sqrt


def n2_laplacian(A: np.ndarray, agg_degrees: np.ndarray, reg: float = 0.1) -> np.ndarray:
    """ULSE-n2 normalization: L = -D_agg_r^{-1/2} A D_r^{-1/2}."""
    agg_r = agg_degrees + reg
    D_agg_inv_sqrt = np.diag(1.0 / np.sqrt(agg_r))
    degrees_t = A.sum(axis=1) + reg
    D_t_inv_sqrt = np.diag(1.0 / np.sqrt(degrees_t))
    return -D_agg_inv_sqrt @ A @ D_t_inv_sqrt


def n1_laplacian_list(A_list: list[np.ndarray], reg: float = 0.1) -> list[np.ndarray]:
    return [n1_laplacian(A, reg) for A in A_list]


def n2_laplacian_list(A_list: list[np.ndarray], reg: float = 0.1) -> list[np.ndarray]:
    agg = sum(A.sum(axis=1) for A in A_list)
    return [n2_laplacian(A, agg, reg) for A in A_list]


def n1_laplacian_from_P(P: np.ndarray, reg: float = 0.1) -> np.ndarray:
    """Noise-free n1 Laplacian from probability matrix P."""
    n = P.shape[0]
    degrees = P.sum(axis=1) + reg
    D_inv_sqrt = np.diag(1.0 / np.sqrt(degrees))
    return np.eye(n) - D_inv_sqrt @ P @ D_inv_sqrt


def n2_laplacian_from_P(P: np.ndarray, agg_degrees: np.ndarray, reg: float = 0.1) -> np.ndarray:
    """Noise-free n2 Laplacian from probability matrix P."""
    agg_r = agg_degrees + reg
    D_agg_inv_sqrt = np.diag(1.0 / np.sqrt(agg_r))
    degrees_t = P.sum(axis=1) + reg
    D_t_inv_sqrt = np.diag(1.0 / np.sqrt(degrees_t))
    return -D_agg_inv_sqrt @ P @ D_t_inv_sqrt


def normalized_laplacian(A: np.ndarray, reg: float = 0.0) -> np.ndarray:
    """Standard normalized Laplacian I - D^{-1/2} A D^{-1/2}."""
    n = A.shape[0]
    degrees = A.sum(axis=1) + reg
    D_inv_sqrt = np.diag(1.0 / np.sqrt(degrees))
    return np.eye(n) - D_inv_sqrt @ A @ D_inv_sqrt


# ---------------------------------------------------------------------------
# Spectral helpers (eigendecomposition-based for stability)
# ---------------------------------------------------------------------------

def _gram_matrix(L_list: list[np.ndarray]) -> np.ndarray:
    """Compute M = sum_t L^(t) L^(t)^T efficiently."""
    n = L_list[0].shape[0]
    M = np.zeros((n, n))
    for L in L_list:
        M += L @ L.T
    return M


def _bottom_eig(L_list: list[np.ndarray], k: int) -> tuple[np.ndarray, np.ndarray]:
    """Compute the k smallest eigenpairs of M = sum_t L^(t) L^(t)^T.

    Returns (eigvecs, eigvals) sorted ascending.
    """
    M = _gram_matrix(L_list)
    eigvals, eigvecs = eigh(M, subset_by_index=[0, k - 1])
    eigvals = np.maximum(eigvals, 0.0)
    return eigvecs, eigvals


def _top_eig(L_list: list[np.ndarray], k: int) -> tuple[np.ndarray, np.ndarray]:
    """Compute the k largest eigenpairs of M = sum_t L^(t) L^(t)^T."""
    n = L_list[0].shape[0]
    M = _gram_matrix(L_list)
    eigvals, eigvecs = eigh(M, subset_by_index=[n - k, n - 1])
    eigvals = np.maximum(eigvals, 0.0)
    return eigvecs[:, ::-1], eigvals[::-1]


# ---------------------------------------------------------------------------
# ULSE embedding
# ---------------------------------------------------------------------------

def ulse_n1(
    A_list: list[np.ndarray],
    K: int,
    reg: float = 0.1,
) -> tuple[np.ndarray, list[np.ndarray], np.ndarray, np.ndarray]:
    """Compute ULSE-n1 embeddings.

    Paper Theorem 1: d = K - 1.
    Embedding: Y^(t) = (L^(t) - I) U Sigma^{-1/2}
    Selection: bottom K eigenvectors of L L^T, excluding the smallest.
    """
    T = len(A_list)
    n = A_list[0].shape[0]
    d = K - 1

    L_list = n1_laplacian_list(A_list, reg)

    # Bottom K eigenpairs (includes the trivial smallest)
    U_K, eigvals_K = _bottom_eig(L_list, K)
    sigma_K = np.sqrt(eigvals_K)  # ascending

    # Select indices 1..K-1 (exclude index 0, the trivial smallest)
    U_sel = U_K[:, 1:K]  # (n, K-1)
    sigma_sel = sigma_K[1:K]  # (K-1,)

    eps = 1e-12
    sigma_inv_sqrt = np.array([1.0 / np.sqrt(s) if s > eps else 0.0 for s in sigma_sel])
    Sigma_inv_sqrt = np.diag(sigma_inv_sqrt)

    U_Sigma_inv_sqrt = U_sel @ Sigma_inv_sqrt

    # Y^(t) = (L^(t) - I) U Sigma^{-1/2}
    Y_hat_list = []
    for t in range(T):
        Lt = L_list[t]
        Y_t = (Lt - np.eye(n)) @ U_Sigma_inv_sqrt
        Y_hat_list.append(Y_t.copy())

    Sigma_sqrt = np.diag(np.sqrt(sigma_sel))
    X_hat = U_sel @ Sigma_sqrt

    return X_hat, Y_hat_list, sigma_K, U_sel


def ulse_n2(
    A_list: list[np.ndarray],
    K: int,
    reg: float = 0.1,
) -> tuple[np.ndarray, list[np.ndarray], np.ndarray, np.ndarray]:
    """Compute ULSE-n2 embeddings.

    Paper Theorem 4: d = K.
    Embedding: Y^(t) = L^(t) U Sigma^{-1/2}
    Selection: top K eigenvectors of L L^T (largest singular values).
    """
    T = len(A_list)
    n = A_list[0].shape[0]

    L_list = n2_laplacian_list(A_list, reg)

    # Top K eigenpairs
    U_K, eigvals_K = _top_eig(L_list, K)
    sigma_K = np.sqrt(eigvals_K)  # descending

    eps = 1e-12
    sigma_inv_sqrt = np.array([1.0 / np.sqrt(s) if s > eps else 0.0 for s in sigma_K])
    Sigma_inv_sqrt = np.diag(sigma_inv_sqrt)

    U_Sigma_inv_sqrt = U_K @ Sigma_inv_sqrt

    # Y^(t) = L^(t) U Sigma^{-1/2}
    Y_hat_list = []
    for t in range(T):
        Lt = L_list[t]
        Y_t = Lt @ U_Sigma_inv_sqrt
        Y_hat_list.append(Y_t.copy())

    Sigma_sqrt = np.diag(np.sqrt(sigma_K))
    X_hat = U_K @ Sigma_sqrt

    return X_hat, Y_hat_list, sigma_K, U_K


def ulse(
    A_list: list[np.ndarray],
    K: int,
    variant: str = "n1",
    reg: float = 0.1,
) -> tuple[np.ndarray, list[np.ndarray], np.ndarray, np.ndarray]:
    if variant == "n1":
        return ulse_n1(A_list, K, reg)
    elif variant == "n2":
        return ulse_n2(A_list, K, reg)
    raise ValueError(f"Unknown variant: {variant}")


# ---------------------------------------------------------------------------
# Noise-free (population-level) embeddings
# ---------------------------------------------------------------------------

def noise_free_ulse_n1(
    P_list: list[np.ndarray],
    K: int,
    reg: float = 0.1,
) -> tuple[np.ndarray, list[np.ndarray], np.ndarray]:
    """Compute noise-free ULSE-n1 embeddings from probability matrices."""
    T = len(P_list)
    n = P_list[0].shape[0]

    L_list = [n1_laplacian_from_P(P, reg) for P in P_list]

    U_K, eigvals_K = _bottom_eig(L_list, K)
    sigma_K = np.sqrt(eigvals_K)

    U_sel = U_K[:, 1:K]
    sigma_sel = sigma_K[1:K]

    eps = 1e-12
    sigma_inv_sqrt = np.array([1.0 / np.sqrt(s) if s > eps else 0.0 for s in sigma_sel])
    Sigma_inv_sqrt = np.diag(sigma_inv_sqrt)

    U_Sigma_inv_sqrt = U_sel @ Sigma_inv_sqrt

    Y_tilde_list = []
    for t in range(T):
        Lt = L_list[t]
        Y_t = (Lt - np.eye(n)) @ U_Sigma_inv_sqrt
        Y_tilde_list.append(Y_t.copy())

    Sigma_sqrt = np.diag(np.sqrt(sigma_sel))
    X_tilde = U_sel @ Sigma_sqrt

    return X_tilde, Y_tilde_list, sigma_K


def noise_free_ulse_n2(
    P_list: list[np.ndarray],
    K: int,
    reg: float = 0.1,
) -> tuple[np.ndarray, list[np.ndarray], np.ndarray]:
    """Compute noise-free ULSE-n2 embeddings from probability matrices."""
    T = len(P_list)
    n = P_list[0].shape[0]

    agg = sum(P.sum(axis=1) for P in P_list)
    L_list = [n2_laplacian_from_P(P, agg, reg) for P in P_list]

    U_K, eigvals_K = _top_eig(L_list, K)
    sigma_K = np.sqrt(eigvals_K)

    eps = 1e-12
    sigma_inv_sqrt = np.array([1.0 / np.sqrt(s) if s > eps else 0.0 for s in sigma_K])
    Sigma_inv_sqrt = np.diag(sigma_inv_sqrt)

    U_Sigma_inv_sqrt = U_K @ Sigma_inv_sqrt

    Y_tilde_list = []
    for t in range(T):
        Lt = L_list[t]
        Y_t = Lt @ U_Sigma_inv_sqrt
        Y_tilde_list.append(Y_t.copy())

    Sigma_sqrt = np.diag(np.sqrt(sigma_K))
    X_tilde = U_K @ Sigma_sqrt

    return X_tilde, Y_tilde_list, sigma_K


def P_from_dsbm(labels: np.ndarray, B_list: list[np.ndarray], rho: float) -> list[np.ndarray]:
    P_list = []
    for B in B_list:
        P = rho * B[np.ix_(labels, labels)]
        np.fill_diagonal(P, 0)
        P_list.append(P)
    return P_list


# ---------------------------------------------------------------------------
# Procrustes alignment
# ---------------------------------------------------------------------------

def procrustes_align(Y: np.ndarray, Y_target: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Find orthogonal W minimizing ||Y - Y_target @ W||_F. Returns (aligned_Y, W)."""
    M = Y_target.T @ Y
    U_svd, _, Vt_svd = np.linalg.svd(M)
    W = U_svd @ Vt_svd
    return Y_target @ W, W


def two_to_inf_norm(M: np.ndarray) -> float:
    return float(np.max(np.linalg.norm(M, axis=1)))


# ---------------------------------------------------------------------------
# Conductance
# ---------------------------------------------------------------------------

def two_way_conductance(A: np.ndarray, partition: np.ndarray) -> float:
    n = A.shape[0]
    degrees = A.sum(axis=1)
    S = partition > 0
    Sc = ~S
    if not S.any() or not Sc.any():
        return 0.0
    vol_S = degrees[S].sum()
    vol_Sc = degrees[Sc].sum()
    if vol_S == 0 or vol_Sc == 0:
        return 0.0
    cut = A[np.ix_(S, Sc)].sum()
    return float(cut / min(vol_S, vol_Sc))


def exact_two_way_conductance_vec(A: np.ndarray, tol: float = 1e-10) -> float:
    """Exhaustive minimum 2-way conductance. Vectorized for speed. n <= 22."""
    n = A.shape[0]
    if n > 22:
        raise ValueError(f"Exhaustive conductance too expensive for n={n}")
    degrees = A.sum(axis=1)
    total = degrees.sum()
    best = float("inf")
    chunk = 1 << min(20, n)
    for start in range(1, (1 << n) - 1, chunk):
        end = min(start + chunk, (1 << n) - 1)
        size = end - start
        masks = np.arange(start, end, dtype=np.int64)
        bits = np.zeros((size, n), dtype=bool)
        for i in range(n):
            bits[:, i] = (masks >> i) & 1
        vols = bits @ degrees
        valid = (vols > tol) & (vols <= total / 2.0 + tol)
        if not valid.any():
            continue
        # cut = vol_S - ones_S^T A ones_S
        Ax = bits @ A
        internal = np.sum(Ax * bits, axis=1)
        cuts = vols - internal
        phis = np.where(valid, cuts / np.maximum(vols, tol), np.inf)
        best = min(best, float(np.min(phis)))
    return best
