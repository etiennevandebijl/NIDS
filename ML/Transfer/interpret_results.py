import os
import glob
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

from project_paths import get_results_folder
from ML.Transfer.experimental_setup import NAMES
NAMES_ = {y: x for x, y in NAMES.items()}

#%% 
input_path = get_results_folder("CIC-IDS-2017", "BRO", "2_Preprocessed_DDoS",
                                "Supervised") + "Train-Test 0/Paper/http-tcp/"

results = []
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
                        model, f1, n, round(f1_b,3)])

df = pd.DataFrame(results, columns = ["Test", "Number of trained D(D)oS attacks",
                                      "Train", "Model", "F1", 'n', "F1 Baseline"])

# %%

df_ = df[df["Number of trained D(D)oS attacks"] == 1]

# %%

group_test = {}
for test_attack, group in df_.groupby("Test"):
    group_test[test_attack] = pd.pivot_table(group, values = "F1", columns="Model",
                                           index = ["Train"])


# %%

group_model = {}
for model, group in df_.groupby("Model"):
    group_ = group[["Train","Test","F1"]]
    group_ = group_[group_["Test"] != "Malicious"]
    group_["Train"] = group_["Train"].map(lambda x: x.replace("['",
                                                              "").replace("']",
                                                                          ""))
    group_["F1"] = group_["F1"].round(3)
    group_model[model] = group_


# %%

cmap = plt.get_cmap('YlOrRd')
pos = None
for model, group in group_model.items():

    plt.figure(figsize = (15,15))

    G = nx.from_pandas_edgelist(group,source='Train', target='Test',
                            edge_attr=True, create_using=nx.DiGraph())

    if pos == None:
        pos=nx.spring_layout(G)
    colors = [cmap(G[u][v]['F1']) for u,v in G.edges()]

    nx.draw_networkx(G, pos, edge_color=colors, connectionstyle="arc3,rad=0.1")
    plt.title(model)
    plt.show()
