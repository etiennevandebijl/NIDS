def shuffle_expected_recall(d, n):
    return d / n  

def shuffle_expected_precision(d, P, n):
    if d == 0:
        return 0
    return P / n 

def shuffle_expected_f1_score(d, P, n):
    if P == 0:
        return 0
    return (P / n) * ( 2 * d / (P + d) )

def shuffle_expectations(d, P, n):
    rc = shuffle_expected_recall(d, n)
    pr = shuffle_expected_precision(d, P, n)
    f1 = shuffle_expected_f1_score(d, P, n)
    return [rc, pr, f1]

def shuffle_optimal_expectations(P,n):
    return [1.0, P/n,  2 * (P / (P + n))], 1.0

