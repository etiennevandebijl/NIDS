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

DATASET = "CIC-IDS-2018"
PROTOCOL = "http-tcp"
RS = 7

#%% 

results = []
for rs in range(RS):
    input_path = get_results_folder(DATASET, "BRO", "2_Preprocessed_DDoS",
                                "Supervised") + "Train-Test " + str(rs) + "/Paper/" + PROTOCOL + "/"
    # input_path = get_results_folder(DATASET, "BRO", "2_Preprocessed_DDoS",
    #                             "Supervised") + "/Paper/" + PROTOCOL + "/"

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

def label_point(x, y, val, ax):
    a = pd.concat({'x': x, 'y': y, 'val': val}, axis=1)
    for i, point in a.iterrows():
        ax.text(point['x'], point['y'], str(point['val']))    

for index, group in df[df["Model"]=="DT"].groupby(["Test", "Model"]):
    group_ = group[~group["Train"].str.contains(index[0])]
    group_ = group_.groupby(["Test","Train", "Model",
                            "Number of trained D(D)oS attacks"])[["F1", "F1 Baseline"]].mean().reset_index()
    group_.plot.scatter(x = "Number of trained D(D)oS attacks", y = "F1", figsize = (8,8))
    plt.title("Model: " + index[1] + ", Test-Attack: " + index[0])
    #label_point(group_["Number of trained D(D)oS attacks"] - 1, group_["F1"], group_["Train"], plt.gca())
    plt.show()

# %%
for index, group in df[df["Model"]=="DT"].groupby(["Test", "Model"]):
    group_ = group[~group["Train"].str.contains(index[0])]
    
    plt.figure(figsize = (20, 13))
    sns.pointplot(x = "Number of trained D(D)oS attacks", y = "F1", hue = "Train", 
                  dodge=True, data = group_, )
    plt.legend([],[], frameon=False)
    plt.title("Model: " + index[1] + ", Test-Attack: " + index[0])
    plt.show()
    
#%%

attacks_included = []
df_ = df.copy()
for i in list(NAMES.keys()):
    if np.sum(df_["Train"].str.contains("'" + i + "'")) > 0:
        df_[i] = df_["Train"].str.contains("'" + i + "'")
        df_[i] = df_[i].replace(True, "O").replace(False, "X")
        attacks_included.append(i)
attacks_included = sorted(attacks_included)

model = "GNB"
for index, group in df_[df_["Model"]==model].groupby(["Test", "Model"]):
    group_ = group[~group["Train"].str.contains(index[0])]
    attacks_ = [n for n in attacks_included if n != index[0]]
    group_["Train Tuple"] = group_[attacks_].agg('-'.join, axis=1)
    Train_Tuple_unique = list(group_["Train Tuple"].unique())
    Length_Train = [a.count("O") for a in Train_Tuple_unique]
    Z = [x for _, x in sorted(zip(Length_Train, Train_Tuple_unique))]
    group_["Number of malicious classes in training"] = group_["Train Tuple"].str.count("O")
    group_["Number of malicious classes in training"] = group_["Number of malicious classes in training"].astype(str) + \
        " attack" + np.where(group_["Number of malicious classes in training"] == 1, "", "s") + " in training data"
    
    plt.figure(figsize = (20, 13))
    sns.swarmplot(x = "Train Tuple", y = "F1", hue = "Number of malicious classes in training",
                   data = group_, order = Z)
    plt.xticks(rotation=90)
    plt.grid()
    plt.ylabel(r"$F_1$ score for each test set", fontsize=12)
    plt.title(DATASET +" performance of " + index[1] + \
              " by testing on N=" + str(RS) + " benign vs malicious classification problems with " + \
                  index[0] + " as malicious test class", fontsize=14)
    plt.xlabel("Malicious train classes (" + ")-(".join(attacks_) + ") where X = excluded and O = included", fontsize=12 )
    plt.axhline(baselines[index[0]], color = "black",  label='Dutch Draw Baseline')
    handles, labels = plt.gca().get_legend_handles_labels()
    labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))
    plt.legend(handles, labels)
    pathje = get_results_folder(DATASET, "BRO", "2_Preprocessed_DDoS", "Supervised") + \
                "Paper-Results/"
    pathje = go_or_create_folder(pathje, "Subsetlearning")
    pathje = go_or_create_folder(pathje, index[0])    
   # plt.savefig(pathje + DATASET + "-" + model + "-" + index[0] + "-" + str(RS) + ".png"  )
    plt.show()


#%%
df_ = df[df["Number of trained D(D)oS attacks"] == 1]
df_ = df_.groupby(["Test", "Train", "Model"])[["F1", "F1 Baseline"]].mean().reset_index()

# %%

group_test = {}
baselines = {}
for test, group in df_.groupby("Test"):
    group_test[test] = pd.pivot_table(group, values = "F1", columns="Model",
                                           index = ["Train"])
    baselines[test] = group[["Test","F1 Baseline"]].drop_duplicates().values[0][1]

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

#%% 

for model, group in group_model.items():
    plt.figure(figsize = (10,10))
    dd = pd.pivot_table(group, index = "Train", columns = "Test", values = "F1")
    sns.heatmap(dd, annot=True, cmap = "RdYlGn")
    plt.title("F1 score for model " + model + " training one attack")
    plt.tight_layout()
    #plt.savefig(input_path + DATASET + "-" + model + "-heatmap.png")
    plt.show()
    
# %%

cmap = plt.get_cmap('YlOrRd')
pos = None
for model, group in group_model.items():
    group_ = group[group["F1"] > 0.0] #Only show if its better than the baseline
    plt.figure(figsize = (15, 15))

    G = nx.from_pandas_edgelist(group_, source='Train', target='Test',
                            edge_attr=True, create_using=nx.DiGraph())

    pos=nx.circular_layout(G)
    colors = [cmap(G[u][v]['F1']) for u,v in G.edges()]

    nx.draw_networkx(G, pos = pos, edge_color=colors, width = 5,
                     connectionstyle="arc3,rad=0.1")
    plt.title(model)
    #plt.savefig(input_path + DATASET + "-" + model + ".png")
    plt.show()