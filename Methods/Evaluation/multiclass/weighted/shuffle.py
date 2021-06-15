from Methods.Evaluation.binary.shuffle import shuffle_expected_f1_score
import scipy.optimize as optimize
import numpy as np

def shuffle_expected_recall_weighted(d, P, n):
    return  np.sum([t*p/(n**2) for t,p in zip(d,P)])

def shuffle_expected_precision_weighted(d, P, n):
    count = [1 if c > 0 else 0 for c in d ]    
    return np.sum([c*(p/n)**2 for c,p in zip(count,P)])

def shuffle_expected_f1_weighted(d, P, n):
    sums = 0
    for i in range(len(P)):
        sums = sums + (P[i]/n) * shuffle_expected_f1_score(d[i], P[i], n)
    return sums 

def shuffle_expectations_weighted(d, P, n):
    rc = shuffle_expected_recall_weighted(d, P, n)
    pr = shuffle_expected_precision_weighted(d, P, n)
    f1 = shuffle_expected_f1_weighted(d, P, n)
    return [rc, pr, f1]

# =============================================================================
# Optimal values
# =============================================================================

def shuffle_optimal_recall_weighted(P, n):
    if all(x == P[0] for x in P):
        theta = None
    else:
        theta = [0] * len(P)
        theta[P.index(max(P))] = 1
    return np.max(P)/n , theta 

def shuffle_optimal_precision_weighted(P, n):
    return np.sum([p**2 for p in P]) / n**2, None

#Zou dit nog even moeten checken evt
def shuffle_optimal_f1_weighted(P, n):
    l = len(P)
    x0 = P
    cons = ({'type': 'eq', 'fun': lambda x:  np.sum(x) - n})
    bounds = [(0,n) for i in range(l)] 
    
    results = optimize.minimize(_max_f1_func, x0, args = (P, n), method='SLSQP', bounds= bounds, constraints=cons)
    d = [round(i) for i in results.x.tolist()]
    return shuffle_expected_f1_weighted(d, P, n), d

def _max_f1_func(d, P, n):
    return -1 * shuffle_expected_f1_weighted(d, P, n)

def shuffle_optimal_weighted(P, n):
    rc,_ = shuffle_optimal_recall_weighted(P, n)
    pr,_ = shuffle_optimal_precision_weighted(P, n)
    f1,_ = shuffle_optimal_f1_weighted(P, n)
    return [rc, pr, f1]

