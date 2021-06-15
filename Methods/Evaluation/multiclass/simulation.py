from scipy.stats import hypergeom
from random import shuffle
import numpy as np
from sklearn.metrics import recall_score, precision_score, f1_score

# =============================================================================
# Coin
# =============================================================================

def coin_simulate_scores(theta, P, n, s, average = "macro",  modelled = True):
    scores = np.zeros((3,s)) #rc,pr,f1
    
    if modelled:
        for P_i,d_i in zip(P,theta):
            tp = np.random.binomial(P_i, d_i, s); fp = np.random.binomial(n-P_i, d_i, s)
            scores = scores + _compute_scores_label(tp, fp, P_i, n, len(P), average)
    else: 
        y_true = np.repeat(range(len(P)),P)   
        for i in range(s):
            y_pred = np.random.choice(len(P), size = n, p = theta)
            rc = recall_score(y_true, y_pred, average = average)
            pr = precision_score(y_true, y_pred , average =average)
            f1 = f1_score(y_true, y_pred , average = average)
            scores[:,i]=[rc,pr,f1]
    return scores

# =============================================================================
# Shuffle
# =============================================================================

def shuffle_simulate_scores(d, P, n, s, average = "macro", modelled = True):
    scores = np.zeros((3,s)) #rc,pr,f1
    
    if modelled:
         for P_i,d_i in zip(P,d):
            tp = hypergeom.rvs(n, d_i, P_i, size=s)
            scores = scores + _compute_scores_label(tp, d_i- tp, P_i, n, len(P), average)
    else:
        y_true = np.repeat(range(len(P)),P) 
        y_pred = np.repeat(range(len(P)),d)
        for i in range(s):
            shuffle(y_pred)
            rc = recall_score(y_true, y_pred, average = average)
            pr = precision_score(y_true, y_pred , average = average)
            f1 = f1_score(y_true, y_pred , average = average)
            scores[:,i]=[rc,pr,f1]
    return scores

def _compute_scores_label(tp, fp, P, n, c, average = "macro"):
    if average == "micro":
       return tp / n
        
    rc = np.nan_to_num(tp / P)
    pr = np.nan_to_num(tp / (tp + fp) ) 
    f1 = np.nan_to_num(2 * (pr * rc) / (pr + rc))   
    metrics = np.array([rc, pr, f1])

    if average == "macro":
        metrics = metrics / c
    if average == "weighted":
        metrics = metrics * (P / n)
    return metrics




