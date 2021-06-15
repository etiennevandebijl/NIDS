import numpy as np

def shuffle_expectations_micro(d, P, n):
    return np.sum([t*p/(n**2) for t,p in zip(d,P)])

def shuffle_optimal_theta_micro(P, n):
    if all(x == P[0] for x in P):
        d = None
    else:
        d = [0] * len(P)
        d[P.index(max(P))] = n
    return np.max(P)/n , d 


