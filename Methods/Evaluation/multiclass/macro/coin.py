from Methods.Evaluation.binary.coin import coin_expected_precision, coin_expected_f1_score
import scipy.optimize as optimize
import numpy as np

def coin_expected_recall_macro(P):
    return 1/len(P)

def coin_expected_precision_macro(theta, P, n):
    sums = 0
    for i in range(len(theta)):
        sums = sums + coin_expected_precision(theta[i], P[i], n)
    return sums / len(P)

def coin_expected_f1_macro(theta, P, n):
    sums = 0
    for i in range(len(theta)):
        sums = sums + coin_expected_f1_score(theta[i], P[i], n)
    return sums / len(P)

def coin_expectations_macro(theta, P, n):
    rc = coin_expected_recall_macro(P)
    pr = coin_expected_precision_macro(theta, P, n)
    f1 = coin_expected_f1_macro(theta, P, n)
    return [rc, pr, f1]

# =============================================================================
# Optimal values
# =============================================================================
    
def coin_optimal_recall_macro(P):
    return 1 / len(P), None

#Dit zou een betere oplossing moeten hebben maar niet echt een idee
def coin_optimal_precision_macro(P, n):
    x0 = P / n
    bounds = [(0,1) for i in range(len(P))]
    const = ({"type": "eq", "fun": lambda x: np.sum(x) - 1})

    results = optimize.minimize(_func_precision_sign, x0, method='SLSQP', bounds=bounds, tol = 1e-80, args = (P,n), constraints = const)
    theta =  results.x.tolist() 
    return coin_expected_precision_macro(theta, P, n), theta

def _func_precision_sign(x, P, n):
    return -1 *  coin_expected_precision_macro(x, P, n)
    
#Can we solve this?
def coin_optimal_f1_macro(P, n):
    x0 = P / n
    bounds = [(0,1) for i in range(len(P))]
    const = ({"type": "eq", "fun": lambda x: np.sum(x) - 1})

    results = optimize.minimize(_func_f1_sign, x0, method='SLSQP', bounds=bounds, tol = 1e-80, args = (P,n), constraints = const)
    theta =  results.x.tolist() 
    return coin_expected_f1_macro(theta, P, n), theta

def _func_f1_sign(x, P, n):
    return -1 *  coin_expected_f1_macro(x, P, n)

def coin_optimal_macro(P, n):
    rc,_ = coin_optimal_recall_macro(P)
    pr,_ = coin_optimal_precision_macro(P, n)
    f1,_ = coin_optimal_f1_macro(P, n)
    return [rc, pr, f1]
