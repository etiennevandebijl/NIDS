import pandas as pd
import numpy as np

def score_curve(y_true, anomaly_scores):
    as_order_index = sorted(range(len(anomaly_scores)),
                            key=lambda k: anomaly_scores[k], reverse=True)
    y_order = y_true[as_order_index]
    y_order_inverse = -1 * (y_order - 1)

    tp = np.insert(np.cumsum(y_order), 0, 0)
    fp = np.insert(np.cumsum(y_order_inverse), 0, 0)

    pr = tp / (tp + fp)
    rc = tp / np.sum(y_true)
    f1 = 2 * pr * rc / (pr + rc)

    eval_metrics = np.stack((pr, rc, f1), axis=-1)
    df_scores = pd.DataFrame(eval_metrics, columns=["Precision", "Recall", "F1_score"])
    return df_scores.fillna(0)

def curve_moments(df, n, P):
    stats = {"n":n, "P": P}
    stats["F1_score-id-P"] = df.loc[P, "F1_score"]
    for m in ["Recall", "F1_score"]:
        stats[m + "-max"] = df[m].max()
        stats[m + "-idxmax"] = df[m].idxmax()
    return stats

# =============================================================================
# Example
# =============================================================================
#y_true = np.random.binomial(1,0.5, 20)
#anomaly_scores = np.random.uniform(size = 20)
#df_score_curve = score_curve(y_true, anomaly_scores)
