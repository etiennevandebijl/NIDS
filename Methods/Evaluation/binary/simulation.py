from scipy.stats import hypergeom
from random import shuffle
import numpy as np

# =============================================================================
# Coin
# =============================================================================

def coin_simulate_scores(theta, P, N, s, method = "binomial"):
    if method == "binomial":
        tp = np.random.binomial(P, theta, s);  fp = np.random.binomial(N, theta, s)
    else:
        y_true = np.array([1] * P + [0] * N)    
        y_pred = np.random.binomial(1, theta, (P + N,s))
        tp = np.matmul(y_true, y_pred); fp = y_pred.sum(0) - tp
    return  _coin_compute_scores(tp, fp, P)

def _coin_compute_scores(tp, fp, P):
    rc = np.nan_to_num(tp / P)
    pr = np.nan_to_num(tp / (tp + fp) ) 
    f1 = np.nan_to_num(2 * (pr * rc) / (pr + rc))   
    return np.array([rc, pr, f1])

# =============================================================================
# Shuffle
# =============================================================================
    
def shuffle_simulate_scores(d, P, N, s, method = "hypergeom"):
    n = N + P
    if method == "hypergeom":
        tp = hypergeom.rvs(n, d, P, size=s)
    else:
        y_true = np.array([1] * P + [0] * N)
        y_pred = [1] * d + [0] * (n - d)
        tp = [] 
        for i in range(s):
            shuffle(y_pred)
            tp.append(np.sum(np.multiply(y_true,y_pred)))

    scores = _shuffle_compute_scores(tp, d, P)
    return scores

def _shuffle_compute_scores(tp, d, P):
    rc = np.nan_to_num(tp / P)
    pr = np.nan_to_num(tp / d) 
    f1 = np.nan_to_num(2 * (pr * rc) / (pr + rc))   
    return np.array([rc, pr, f1])
