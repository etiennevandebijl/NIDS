import scipy
import numpy as np


def coin_expected_recall(theta):
    return theta


def coin_expected_precision(theta, P, n):
    return (P / n) * (1 - (1 - theta)**n)


def coin_expected_f1_score(theta, P, n):
    if theta == 0.0:
        return 0.0

    if theta == 1.0:
        return 2 * (P / (P + n))

    f1 = 0
    terms = [k / (k + P) for k in range(n)]
    binom = [scipy.stats.binom.pmf(k, n, theta) for k in range(n)]
    f1 = 2 * (P / n) * np.sum([t*b for t, b in zip(terms, binom)])
    return f1


def coin_expectations(theta, P, n):
    rc = coin_expected_recall(theta)
    pr = coin_expected_precision(theta, P, n)
    f1 = coin_expected_f1_score(theta, P, n)
    return [rc, pr, f1]


def coin_optimal_expectations(P, n):
    return [1.0, P/n,  2 * (P / (P + n))], 1.0
