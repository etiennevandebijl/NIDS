import numpy as np

def coin_expectations_micro(theta, P, n):
    return np.sum([t*p/n for t,p in zip(theta,P)])

def coin_optimal_theta_micro(P,n):
    if all(x == P[0] for x in P):
        theta = None
    else:
        theta = [0] * len(P)
        theta[P.index(max(P))] = 1
    return np.max(P)/n , theta 


