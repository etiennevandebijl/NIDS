import os
import glob
import pandas as pd
import networkx as nx
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

from project_paths import get_results_folder, go_or_create_folder
from ML.Transfer.experimental_setup import NAMES
NAMES_ = {y: x for x, y in NAMES.items()}

DATASET = "CIC-IDS-2017_CIC-IDS-2018"
VARIANT = "Web"
EXPERIMENT = "Paper"

PROTOCOL = "http-tcp"
RS = 1
if DATASET == "CIC-IDS-2018":
    RS = 10

#%% 

results = []
for rs in range(RS):
    # input_path = get_results_folder(DATASET, "Zeek", "2_Preprocessed_" + VARIANT,
    #                             "Supervised") + "Train-Test " + str(rs) + \
    #                             "/" + EXPERIMENT + "/" + PROTOCOL + "/"
    input_path = get_results_folder(DATASET, "Zeek", "2_Preprocessed_" + VARIANT,
                                "Supervised") + "/" + EXPERIMENT + "/"  + PROTOCOL + "/"

    for file in glob.glob(input_path + '**/scores.csv', recursive=True):
        tags = file.split(os.sep)
        model = tags[-2]
        train_attacks = tags[-3].split(" ")
        test_attack = tags[-4]

        train_attacks = [NAMES_[l] for l in train_attacks]
        number_of_attacks = len(train_attacks)

        df = pd.read_csv(file, sep=";", decimal=",", index_col=0).fillna(0)

        f1 = df.loc["Malicious", "F1 Score"]
        n = df[["Benign", "Malicious"]].sum().sum()
        f1_b = df.loc["Malicious", "F1 Baseline"]
    
        results.append([test_attack, len(train_attacks), str(train_attacks),
                        model, f1, n, round(f1_b,3), rs] )

df = pd.DataFrame(results, columns = ["Test", "Number of trained D(D)oS attacks",
                                      "Train", "Model", "F1", 'n', "F1 Baseline", 'RS'])


# %%

plt.rc('text', usetex=True)
plt.rc('font', **{'size': 15.0})
plt.rc('text.latex', preamble=r'\usepackage{lmodern}')

# %%

df__ = df[df["Number of trained D(D)oS attacks"] == 1]
df__ = df__.groupby(["Test", "Train", "Model"])[["F1", "F1 Baseline"]].mean().reset_index()

df__ = df__[df__["Test"] != "Malicious"]
df__["Train"] = df__["Train"].map(lambda x: x.replace("['","").replace("']",""))
df__["Train"] = df__["Train"].str.replace("DDoS - ","").str.replace("DoS - ","")
df__["Train"] = df__["Train"].str.replace("- HTTP","")
df__["Train"] = df__["Train"].str.replace("Web Attack - ","")
df__["Test"] = df__["Test"].str.replace("DDoS - ","").str.replace("DoS - ","")
df__["Test"] = df__["Test"].str.replace("- HTTP","")
df__["Test"] = df__["Test"].str.replace("Web Attack - ","")


df__["Train - Model"] = df__["Train"] + np.where(df__["Model"].isin(["DT","RF"]),  " -  ", " - ") + df__["Model"]

baselines = {row["Test"]:row["F1 Baseline"] for _, row in df__.iterrows()}

for bl in baselines.items():
    df__ = df__.append({'Test': bl[0], "Model":"Dutch Draw", "F1":bl[1]
                        , "Train":"", "Train - Model": " Dutch Draw"
                        }, ignore_index=True)


df__ = df__.pivot_table(values = "F1", index = ["Test"], columns = ["Train - Model"]).T

if EXPERIMENT == "WEB":
    plt.figure(figsize = (7,8))
else:
    plt.figure(figsize = (9,13))
ax = sns.heatmap(df__, annot = np.array(["{:.3f}".format(data)
                            for data in df__.values.ravel()]).reshape(
                                    np.shape(df__)),
                  cmap = "RdYlGn", fmt='',
                  cbar_kws = dict(use_gridspec=True, location="top"))
ax.axhline(1, color='white', lw=5)
ax.axhline(5, color='white', lw=5)
ax.axhline(9, color='white', lw=5)
ax.axhline(13, color='white', lw=5)
ax.axhline(17, color='white', lw=5)
ax.axhline(21, color='white', lw=5)
plt.xticks(rotation=90)
pathje = get_results_folder(DATASET, "Zeek", "2_Preprocessed_" + VARIANT, "Supervised") + "Paper-Results/"
pathje = go_or_create_folder(pathje, "Heatmap")
plt.ylabel("Class (Training) - Model")
plt.xlabel("Class (Testing)")
plt.tight_layout()
#plt.savefig(pathje + "Results Experiment 2 " + DATASET + " " + VARIANT + ".png", dpi = 400)
plt.show()

#%% 
# df_ = df[df["Number of trained D(D)oS attacks"] == 1]
# df_ = df_.groupby(["Test", "Train", "Model"])[["F1", "F1 Baseline"]].mean().reset_index()

# %%

# group_test = {}
# baselines = {}
# for test, group in df_.groupby("Test"):
#     group_test[test] = pd.pivot_table(group, values = "F1", columns="Model",
#                                            index = ["Train"])
#     baselines[test] = group[["Test","F1 Baseline"]].drop_duplicates().values[0][1]

# # %%

# group_model = {}
# for model, group in df_.groupby("Model"):
#     group_ = group[["Train","Test","F1"]]
#     group_ = group_[group_["Test"] != "Malicious"]
#     group_["Train"] = group_["Train"].map(lambda x: x.replace("['",
#                                                               "").replace("']",
#                                                                           ""))
#     group_["F1"] = group_["F1"].round(3)
#     group_model[model] = group_


#%% 

# for model, group in group_model.items():
#     for test, value in baselines.items():
#         new_row = {"Train": "Baseline", "Test":test, "F1": value}
#         if test != "Malicious":
#             group = group.append(new_row,  ignore_index=True)
#     plt.figure(figsize = (10,10))
    
#     dd = pd.pivot_table(group, index = "Train", columns = "Test", values = "F1")
    
#     ax = sns.heatmap(dd, annot=True, cmap = "RdYlGn", fmt='.5g')
#     ax.axhline(1, color='black', lw=5)
#     plt.title("F1 score for model " + model + " training one attack")
#     plt.tight_layout()
#     pathje = get_results_folder(DATASET, "Zeek", "2_Preprocessed_" + VARIANT, "Supervised") + \
#                 "Paper-Results/"
#     pathje = go_or_create_folder(pathje, "Heatmap") 
#   #  plt.savefig(pathje + DATASET + "-" + model + "-heatmap.png")
#     plt.show()

# # %%

# cmap = plt.get_cmap('YlOrRd')
# pos = None
# for model, group in group_model.items():
#     group_ = group[group["F1"] > 0.0] #Only show if its better than the baseline
#     plt.figure(figsize = (15, 15))

#     G = nx.from_pandas_edgelist(group_, source='Train', target='Test',
#                             edge_attr=True, create_using=nx.DiGraph())

#     pos=nx.circular_layout(G)
#     colors = [cmap(G[u][v]['F1']) for u,v in G.edges()]

#     nx.draw_networkx(G, pos = pos, edge_color=colors, width = 5,
#                      connectionstyle="arc3,rad=0.1")
#     plt.title(model)
#     #plt.savefig(input_path + DATASET + "-" + model + ".png")
#     plt.show()
