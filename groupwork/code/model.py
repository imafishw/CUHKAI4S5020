"""Two-dimensional SPD quadratic models; deterministic float64 inputs."""
import numpy as np

def problem(kappa, theta=np.pi / 6):
    c, s = np.cos(theta), np.sin(theta)
    q = np.array([[c, -s], [s, c]], dtype=np.float64)
    h = q @ np.diag([1.0, float(kappa)]) @ q.T
    return h, q @ np.ones(2), q

def optimal_parameters(mu, largest):
    root = np.sqrt(largest / mu)
    return 2 / (largest + mu), 4 / (np.sqrt(largest) + np.sqrt(mu))**2, ((root-1)/(root+1))**2

def spectral_radius(h, alpha, beta=0.0):
    return max(abs(r) for lam in np.linalg.eigvalsh(h)
               for r in np.roots([1, -(1 + beta - alpha * lam), beta]))
