import os
import pandas as pd
from joblib import dump
from sklearn.base import clone
import matplotlib.pyplot as plt

from project_paths import go_or_create_folder

def store_results(results, output_path):
    list_method_fi = []
    dict_method_sc = {}

    for model, results_list in results.items():
        output_path_model = go_or_create_folder(output_path, model)

        clf, df_scores, df_fi = results_list
        dump(clone(clf), output_path_model + "opt_clf.joblib")

        _plot_and_save_score(df_scores, model, output_path_model)
        dict_method_sc[model] = df_scores["F1 Score"]

        if df_fi.shape[0] > 0:
            _plot_top_10_fi(df_fi, model, output_path_model)
            list_method_fi.append(df_fi)

    dict_method_sc, list_method_fi = not_selected_models(dict_method_sc, list_method_fi,
                                                         results, output_path)

    if len(list_method_fi) > 0:
        pd.concat(list_method_fi, axis=1).to_csv(output_path + "feature_importance.csv",
                                                 sep=";", decimal=",")
    df_model_scores = pd.DataFrame(dict_method_sc)
    _plot_model_comparison(df_model_scores, output_path)

def not_selected_models(dict_method_sc, list_method_fi, results, output_path):
    for name in os.listdir(output_path):
        if (os.path.isdir(output_path + "/" + name) and not name in results.keys()):
            df_scores = pd.read_csv(output_path + name + "/scores.csv", sep=";",
                                    decimal=",", index_col=0)
            dict_method_sc[name] = df_scores["F1 Score"]
            try:
                df_fi = pd.read_csv(output_path + name + "/feature-importance.csv",
                                    sep=";", decimal=",", index_col=0)
                list_method_fi.append(df_fi)
            except FileNotFoundError:
                pass
    return dict_method_sc, list_method_fi

# =============================================================================
# Visualization
# =============================================================================

def _plot_and_save_score(dataset, model, outpath_path):
    dataset.to_csv(outpath_path +"scores.csv", index=True, sep=";", decimal=",")
    dataset = dataset[["Precision", "Recall", "F1 Score", "F1 Baseline"]]
    dataset.plot(kind="bar", figsize=(15, 10), title=model+" score")
    plt.xticks(rotation=70)
    plt.ylabel('Metric Score')
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.savefig(outpath_path + model + " score.png")
    plt.close()

def _plot_model_comparison(dataset, output_path):
    dataset.plot(kind="bar", figsize=(15, 10), title="Model Comparison Based on F1 Score")
    plt.xticks(rotation=70)
    plt.ylabel('F1 Score')
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.savefig(output_path +"model-comp.png")
    plt.close()

# =============================================================================
# Feature Importances
# =============================================================================

def _plot_top_10_fi(dataset, model, output_path):
    dataset[model].to_csv(output_path + "feature-importance.csv", sep=";", decimal=",")
    dataset = dataset.sort_values(model, ascending=False)[model].iloc[0:10, ]
    dataset.T.plot(kind="bar", figsize=(12, 8), title=model + " Top Feature Importances")
    plt.xticks(rotation=70)
    plt.ylabel("Feature Importance")
    plt.xlabel('Feature')
    plt.tight_layout()
    plt.savefig(output_path + "feature-importance.png")
    plt.close()

