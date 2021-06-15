from Methods.Evaluation.binary.coin import coin_expected_precision, coin_expected_f1_score
import scipy.optimize as optimize
import numpy as np

def coin_expected_recall_weighted(theta, P, n):
        return np.sum([t*p/n for t,p in zip(theta,P)])

def coin_expected_precision_weighted(theta, P, n):
    sums = 0
    for i in range(len(theta)):
        sums = sums + (P[i]/n) * coin_expected_precision(theta[i], P[i], n) 
    return sums

def coin_expected_f1_weighted(theta, P, n):
    sums = 0
    for i in range(len(theta)):
        sums = sums +  (P[i]/n) * coin_expected_f1_score(theta[i], P[i], n)
    return sums

def coin_expectations_weighted(theta, P, n):
    rc = coin_expected_recall_weighted(theta, P, n)
    pr = coin_expected_precision_weighted(theta, P, n)
    f1 = coin_expected_f1_weighted(theta, P, n)
    return [rc, pr, f1]

# =============================================================================
# Optimal values
# =============================================================================
def coin_optimal_recall_weighted(P, n):
    if all(x == P[0] for x in P):
        theta = None
    else:
        theta = [0] * len(P)
        theta[P.index(max(P))] = 1
    return np.max(P)/n , theta 

def coin_optimal_precision_weighted(P, n):
    x0 = P / n
    bounds = [(0,1) for i in range(len(P))]
    const = ({"type": "eq", "fun": lambda x: np.sum(x) - 1})

    results = optimize.minimize(_func_precision_sign, x0, method='SLSQP', bounds=bounds, tol = 1e-80, args = (P,n), constraints = const)
    theta =  results.x.tolist() 
    return coin_expected_precision_weighted(theta, P, n), theta

def _func_precision_sign(x, P, n):
    return -1 *  coin_expected_precision_weighted(x, P, n)

def coin_optimal_f1_weighted(P, n):
    x0 = P / n
    bounds = [(0,1) for i in range(len(P))]
    const = ({"type": "eq", "fun": lambda x: np.sum(x) - 1})

    results = optimize.minimize(_func_f1_sign, x0, method='SLSQP', bounds=bounds, tol = 1e-80, args = (P,n), constraints = const)
    theta =  results.x.tolist() 
    return coin_expected_f1_weighted(theta, P, n), theta

def _func_f1_sign(x, P, n):
    return -1 *  coin_expected_f1_weighted(x, P, n)

def coin_optimal_weighted(P, n):
    rc,_ = coin_optimal_recall_weighted(P, n)
    pr,_ = coin_optimal_precision_weighted(P, n)
    f1,_ = coin_optimal_f1_weighted(P, n)
    return [rc, pr, f1]
