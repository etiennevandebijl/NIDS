from Methods.Evaluation.binary.shuffle import shuffle_expected_f1_score
import numpy as np

def shuffle_expected_recall_macro(P):
    return 1/len(P)

def shuffle_expected_precision_macro(d, P, n):
    count = [1 if c > 0 else 0 for c in d]    
    return np.sum([c*(p/n) for c,p in zip(count,P)]) / len(P)

def shuffle_expected_f1_macro(d, P, n):
    sums = 0
    for i in range(len(P)):
        sums = sums + shuffle_expected_f1_score(d[i], P[i], n)
    return sums / len(P)

def shuffle_expectations_macro(d, P, n):
    rc = shuffle_expected_recall_macro(P)
    pr = shuffle_expected_precision_macro(d, P, n)
    f1 = shuffle_expected_f1_macro(d, P, n)
    return [rc, pr, f1]

# =============================================================================
# Optimal values
# =============================================================================
    
def shuffle_optimal_expected_recall_macro(P):
    return 1 / len(P), None

def shuffle_optimal_expected_precision_macro(P):
    return 1 / len(P), None #all d not zero

def shuffle_optimal_expected_f1_macro(P):
    return 1 / len(P), P #d = P

def shuffle_optimal_macro(P):
    rc,_ = shuffle_optimal_expected_recall_macro(P)
    pr,_ = shuffle_optimal_expected_precision_macro(P)
    f1,_ = shuffle_optimal_expected_f1_macro(P)
    return [rc, pr, f1]