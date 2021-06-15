import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from project_paths import get_results_folder
from Methods.Evaluation.multiclass.micro.shuffle import shuffle_optimal_theta_micro
from Methods.Evaluation.multiclass.macro.shuffle import shuffle_optimal_expected_f1_macro
from Methods.Evaluation.multiclass.weighted.shuffle import shuffle_optimal_f1_weighted

PROTOCOLS = ["TCP", "UDP", "HTTP", "DNS", "FTP", "SSH", "SSL"]
input_path = get_results_folder("CIC-IDS-2017", "BRO", "2_Preprocessed", "Supervised") + \
                                "Train-Test 0/Holdout/Evaluation/"

# =============================================================================
# Complete (Multiclass)
# =============================================================================

results = []
for f in glob.glob(input_path + "**/Complete/**/scores.csv", recursive=True):
    protocol = f.split("\\")[1].upper()
    model = f.split("\\")[3]
    df = pd.read_csv(f, sep=";", decimal=",", index_col=0).fillna(0)
    P = (df["TP"] + df["FN"]).values.tolist()
    n = np.sum(P)

    f1_micro = df["TP"].sum() / n
    f1_macro = df["F1 Score"].mean()
    f1_weighted = (P * df["F1 Score"]).sum() / n

    results.append([protocol, model, f1_micro, f1_macro, f1_weighted])

    f1_micro = shuffle_optimal_theta_micro(P, n)[0]
    f1_macro = shuffle_optimal_expected_f1_macro(P)[0]
    f1_weighted = shuffle_optimal_f1_weighted(P, n)[0]
    results.append([protocol, "Baseline", f1_micro, f1_macro, f1_weighted])

df_results = pd.DataFrame(results, columns=["Protocol", "Model", "F1 micro",
                                            "F1 macro", "F1 weighted"]).round(5)
df_results = df_results.drop_duplicates()

PROTO = [c for c in PROTOCOLS if c in df_results["Protocol"].unique()]
df_results_micro = df_results.pivot_table(index='Model', columns='Protocol',
                                          values="F1 micro")[PROTO]
df_results_macro = df_results.pivot_table(index='Model', columns='Protocol',
                                          values="F1 macro")[PROTO]
df_results_weighted = df_results.pivot_table(index='Model', columns='Protocol',
                                             values="F1 weighted")[PROTO]

# =============================================================================
# Attacks
# =============================================================================

results_dict = {}
for f in glob.glob(input_path + "**/Complete/**/scores.csv", recursive=True):
    protocol = f.split("\\")[1].upper()
    model = f.split("\\")[3]
    df = pd.read_csv(f, sep=";", decimal=",", index_col=0).fillna(0)
    results_dict[(model, protocol)] = df[["F1 Score", "F1 Baseline"]]
df = pd.concat(results_dict).rename_axis(['Model', "Protocol", "Attack"]).reset_index()

results_dict_ = {}
for model, df_model in df.groupby("Model"):
    results_dict_[model] = pd.pivot(df_model, index="Attack", columns="Protocol")["F1 Score"]

results_dict_ = {}
for protocol, df_p in df.groupby("Protocol"):
    df_pivot = pd.pivot(df_p, index="Attack", columns="Model")["F1 Score"]
    baseline = df_p[["Attack", "F1 Baseline"]].drop_duplicates()
    baseline.index = baseline["Attack"]
    baseline.drop(["Attack"], 1, inplace=True)
    results_dict_[protocol] = pd.concat([baseline, df_pivot], axis=1)

for protocol, df in results_dict_.items():
    df.plot(kind="bar", figsize=(20, 10))
    plt.title("Attack F1 score per model")
    plt.ylabel("F1 score")
    plt.show()

# =============================================================================
# Binary Benign vs Malicious
# =============================================================================

results_dict = {}
for f in glob.glob(input_path + "**/Benign vs Malicious/**/scores.csv", recursive=True):
    protocol = f.split("\\")[1].upper()
    model = f.split("\\")[3]
    df = pd.read_csv(f, sep=";", decimal=",", index_col=0).fillna(0)
    results_dict[(model, protocol)] = df[["F1 Score", "F1 Baseline"]]
df = pd.concat(results_dict).rename_axis(['Model', "Protocol", "Attack"]).reset_index()
df = df[df["Attack"] == "Malicious"]

results_dict_ = {}
for protocol, df_p in df.groupby("Protocol"):
    df_pivot = pd.pivot(df_p, index="Attack", columns="Model")["F1 Score"]
    baseline = df_p[["Attack", "F1 Baseline"]].drop_duplicates()
    baseline.index = baseline["Attack"]
    baseline.drop(["Attack"], 1, inplace=True)
    results_dict_[protocol] = pd.concat([baseline, df_pivot], axis=1)

# =============================================================================
# Binary One vs One
# =============================================================================

results = []
for f in glob.glob(input_path + "**/Benign vs */**/scores.csv", recursive=True):
    if not "Malicious" in f:
        tags = f.split("\\")
        protocol = tags[1].upper()
        attack = tags[2].replace("Benign vs ", "")
        model = tags[3]

        df = pd.read_csv(f, sep=";", decimal=",", index_col=0).fillna(0).round(5)
        results.append([protocol, attack, model, df.loc[attack, "F1 Score"]])
        results.append([protocol, attack, "Baseline", df.loc[attack, "F1 Baseline"]])
df_score_bin = pd.DataFrame(results, columns=["Protocol", "Attack", "Model",
                                              "F1 Score"]).drop_duplicates()

results_dict_attack = {}
for attack, df in df_score_bin.groupby("Attack"):
    df_ = pd.pivot_table(df, index="Model", columns="Protocol", values="F1 Score")
    results_dict_attack[attack] = df_[[c for c in PROTOCOLS if c in df_.columns]]

for protocol, group in df_score_bin.groupby("Protocol"):
    df_results = group.pivot_table(index='Attack', columns='Model', values="F1 Score")
    df_results.plot(kind="bar", figsize=(20, 10))
    plt.title(protocol + "attack F1 score per model")
    plt.ylabel("F1 score")
