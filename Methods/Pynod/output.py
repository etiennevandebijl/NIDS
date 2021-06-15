# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from project_paths import go_or_create_folder
from ML.Unsupervised.eval import score_curve, curve_moments
from ML.Unsupervised.vis import interpret_scores
import matplotlib.pyplot as plt
import seaborn as sns

def plot_distances(dist_weight, labels, ts_list, metric, output_path):
    plt.figure(figsize=(15,10))
    sns.scatterplot(x=ts_list, y=dist_weight, hue=labels)
    plt.ylabel(metric)
    plt.xlabel("Time")
    plt.tight_layout()
    plt.savefig(output_path + metric + ".png")
    plt.close()

def output(df_dist, labels, ts_list, output_path):
    distance_names = df_dist.columns.tolist()
    try:
        df_dist_old = pd.read_csv(output_path + "distance-metrics.csv",
                                    sep=";", decimal=",", index_col=0)
        df_dist_old.drop(["Label"], 1, inplace=True)
        for name in df_dist_old.columns:
            if not name in distance_names:
                df_dist[name] = df_dist_old[name].values
    except FileNotFoundError:
        pass  

    n = df_dist.shape[0]
    P = np.sum(labels)

    scores_scaler_model = []
    for metric in df_dist:
        metric_dist = df_dist[metric].tolist()

        df_scores = score_curve(labels, metric_dist)
        stats = curve_moments(df_scores, n, P)
        stats["Baseline"] = 2 * P / (P + n)
        stats["Metric"] = metric
        scores_scaler_model.append(stats)

        distances_path = go_or_create_folder(output_path, "Distances")
        plot_distances(metric_dist, labels, ts_list, metric, distances_path)
        
        interpret_path = go_or_create_folder(output_path, "Curves")
        interpret_scores(df_scores, n, P, metric, interpret_path + metric)

    df_comp = pd.DataFrame(scores_scaler_model)
    df_comp["F1_score-idxmax"] = df_comp["F1_score-idxmax"] / n
    df_comp["Recall-idxmax"] = df_comp["Recall-idxmax"] / n        
    df_comp.to_csv(output_path + "metric_comparison.csv",
                           sep=";", decimal=",", index=False)
    
    df_dist["Label"] = labels
    df_dist.to_csv(output_path + "distance-metrics.csv",
                           sep=";", decimal=",", index=False)