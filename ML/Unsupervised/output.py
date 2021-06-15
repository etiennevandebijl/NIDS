import numpy as np
import pandas as pd
from joblib import dump
from sklearn.base import clone

from project_paths import go_or_create_folder
from ML.Unsupervised.eval import score_curve, curve_moments
from ML.Unsupervised.vis import interpret_scores, boxplot_scores_label, scatter_plot_ts_scores, score_per_class

def store_as_and_models(dataset, results, models, output_path):
    for model, clf in models.items():
        dataset[model] = results[model]
        output_path_model = go_or_create_folder(output_path, model)
        dump(clone(clf), output_path_model + "clf.joblib")

    dataset = dataset[["uid", "ts"] + list(models.keys()) + ["Label"]]
    dataset.to_csv(output_path + "anomaly-scores.csv", sep=";", decimal=",", index=False)
    return dataset

def create_figures(df, output_path):
    y_true = np.where(df["Label"] != "Benign", 1, 0)
    n = len(y_true)
    P = int(np.sum(y_true))

    score_model = {}
    for model in  [c for c in df.columns if not c in ["ts", "uid", "Label"]]:
        output_path_model = go_or_create_folder(output_path, model)

        #Anomaly Score plots
        boxplot_scores_label(df, model, output_path_model)
        for date, df_day in df.groupby(df["ts"].dt.date):
            if df_day["Label"].nunique() > 1:
                scatter_plot_ts_scores(df_day, model, output_path_model, date)
        
        #Curve info
        df_scores = score_curve(y_true, df[model].tolist())
        stats_curve = curve_moments(df_scores, n, P)
        score_model[model] = stats_curve
        interpret_scores(df_scores, n, P, model, output_path_model)

        #Prediction
        df_P = predict_threshold(df, model, P, n, output_path_model, "P")
        df_max_F1 = predict_threshold(df, model, stats_curve["F1_score-idxmax"],
                                      n, output_path_model, "max-F1")

        df_scores_class = pd.concat([df_P, df_max_F1], 1)
        df_scores_class.columns = ["Score Threshold P","Score Threshold Max F1"]
        df_scores_class.to_csv(output_path_model + "class_comparison.csv", sep=";", decimal=",")

    df_comp = pd.DataFrame(score_model).T
    df_comp.to_csv(output_path + "model_comparison.csv", sep=";", decimal=",")

def predict_threshold(df, model, label_positive, n, path=None, threshold=""):
    y_pred = [1] * label_positive + [0] * (n - label_positive)
    df_ = df.sort_values(by=[model], ascending=False)
    df_["Prediction"] = y_pred
    df_["Predicted"] = np.where(df_["Prediction"] == 1, "Predicted Malicious", "Predicted Benign")
    pvt = pd.pivot_table(df_, index="Label", columns="Predicted",
                         values="Prediction", aggfunc="count").fillna(0)
    if not "Predicted Benign" in pvt.columns:
        pvt["Predicted Benign"] = 0
    if not "Predicted Malicious" in pvt.columns:
        pvt["Predicted Malicious"] = 0

    pvt = (pvt.T / pvt.sum(1)).T * 100
    pvt = pvt.sort_index()

    class_dist = df["Label"].value_counts() * 100 / n
    score_per_class(pvt, class_dist, n, path, threshold)
    return df_.groupby("Label")["Prediction"].mean() * 100
