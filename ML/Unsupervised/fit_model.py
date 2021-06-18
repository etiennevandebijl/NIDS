import warnings
import numpy as np
from tqdm import tqdm
from sklearn.model_selection import KFold
import time
from Zeek.utils import format_ML

warnings.filterwarnings("ignore")

def fit_model(dataset, models, train_benign=False):
    L = 1
    X, y, _, _ = format_ML(dataset, True)

    y_pred_dict = {}
    for model, clf in models.items():
        print(model)
        time.sleep(1)
        y_pred_rs = np.zeros((X.shape[0], L))
        for rs in range(L):
            y_pred_rs[:, rs] = fit_predict_kfold_all(clf, X, y,
                                                     rs, train_benign)
        y_pred_dict[model] = y_pred_rs.mean(1)
    return y_pred_dict

def fit_predict_kfold_all(clf, X, y, rs, train_benign=False):
    K = 10
    kf = KFold(n_splits=K, random_state=123*rs, shuffle=True)

    y_pred = np.zeros(X.shape[0])
    for train_index, test_index in tqdm(kf.split(X), total=K, desc="K-Fold"):
        if train_benign:
            benign_index = [i for i, y_i in enumerate(y[train_index]) if not y_i]
            clf.fit(X[benign_index])
        else:
            clf.fit(X[train_index])
        y_pred_as = clf.decision_function(X[test_index])
        if clf.__class__.__name__ == "IForest":
            y_pred_as = [y_i + 0.5 for y_i in y_pred_as]
        if clf.__class__.__name__ == "PCA":
            y_pred_as = np.log(y_pred_as)
        y_pred[test_index] = y_pred_as
    return y_pred

# =============================================================================
# Example
# =============================================================================
# from project_paths import get_data_folder
# from BRO.utils import read_preprocessed
# df = read_preprocessed(get_data_folder("UNSW-NB15", "BRO",
#   "2_Preprocessed") + "ftp.csv")
# from ML.Unsupervised.models import models
# df_= fit_model(df, models)
