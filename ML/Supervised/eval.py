import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix

def feature_importance_statistics(fitted_models, model, feature_names):
    df = pd.DataFrame()
    if hasattr(fitted_models[0], 'feature_importances_'):
        fi_importances = []
        for m in fitted_models:
            fi_importances.append(m.feature_importances_.tolist())
        fi_importances_mean = np.mean(np.array(fi_importances), axis=0)
        df = pd.DataFrame(fi_importances_mean.T, index=feature_names, columns=[model])
    return df

def evaluation_metrics(y, y_pred, labels):
    cm = confusion_matrix(y, y_pred, labels=labels)
    df = pd.DataFrame(cm, index=labels, columns=labels)

    df["TP"] = cm.diagonal()
    df["FP"] = cm.sum(axis=0) - cm.diagonal()
    df["FN"] = cm.sum(axis=1) - cm.diagonal()

    df["Recall"] = df["TP"] / (df["TP"] + df["FN"])
    df["Precision"] = df["TP"] / (df["TP"] + df["FP"])
    df["F1 Score"] = 2 * df["Precision"] * df["Recall"] / (df["Precision"] + df["Recall"])
    df["F1 Baseline"] = 2 * (df["TP"] + df["FN"]) / (df["TP"] + df["FN"] + cm.sum().sum())
    return df.fillna(0)
    