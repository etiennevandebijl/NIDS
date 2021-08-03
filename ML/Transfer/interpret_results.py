import os
import glob
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

from project_paths import get_results_folder

input_path = get_results_folder("CIC-IDS-2017", "BRO", "2_Preprocessed_DDoS", "Supervised") + "Train-Test 0/Paper/http-tcp/"

NAMES = {"DoS - Hulk": "Hulk",
         "DDoS - HOIC": "HOIC",
         "DDoS - LOIC": "LOIC",
         "DDoS - LOIC - HTTP": "HLOIC",
         "DDoS - LOIC - UDP": "ULOIC",
         "DoS - SlowHTTPTest": "Test",
         "DoS - GoldenEye": "Eye",
         "DDoS - Botnet": "Bot",
         "DoS - Slowloris": "Slow"}
NAMES2 = {y: x for x, y in NAMES.items()}


results = []
for file in glob.glob(input_path + '**/scores.csv', recursive=True):
    tags = file.split(os.sep)
    test_attack = tags[-4]
    train_attacks = tags[-3].split(" ")

    train_attacks = [NAMES2[l] for l in train_attacks]

    model = tags[-2]
    number_of_attacks = len(train_attacks)

    df = pd.read_csv(file, sep=";", decimal=",", index_col=0).fillna(0)
    f1 = df.loc["Malicious", "F1 Score"]
    n = df[["Benign", "Malicious"]].sum().sum()
    f1_b = df.loc["Malicious", "F1 Baseline"]
    #if test_attack not in train_attacks:
    results.append([test_attack, len(train_attacks), str(train_attacks), 
                        model, f1, n, round(f1_b,3)])

df = pd.DataFrame(results, columns = ["Test", "Number of trained D(D)oS attacks",
                                      "Train", "Model", "F1", 'n', "F1 Baseline"])
df = df[df["Number of trained D(D)oS attacks"] == 1]

results2 = {}
for test_attack, group in df.groupby("Test"):
    pivot = pd.pivot_table(group, values = "F1",
                           index = ["Train", "Number of trained D(D)oS attacks", 
                                    "n", "F1 Baseline"], columns="Model")
    results2[test_attack] = pivot


df_list = []
for test_attack, pivot in results2.items():
    tab = pivot.reset_index()[["Train","DT"]]
    tab["Test"] = test_attack
    tab["Train"] = tab["Train"].map(lambda x: x.replace("['","").replace("']",""))
    df_list.append(tab)

df_new = pd.concat(df_list)
df_new = df_new[["Train","Test","DT"]].reset_index(drop=True)
df_new = df_new[df_new["Test"] != "Malicious"]

df_new = df_new[df_new["DT"] > 0]
df_new["DT"] = df_new["DT"].round(3)
G = nx.from_pandas_edgelist(df_new,source='Train',
                                   target='Test',edge_attr=True,
                                   create_using=nx.DiGraph())

plt.figure(figsize = (15,15))
cmap = plt.get_cmap('YlOrRd')
pos=nx.spring_layout(G)
colors = [cmap(G[u][v]['DT']) for u,v in G.edges()]

nx.draw_networkx(G, pos, edge_color=colors, connectionstyle="arc3,rad=0.1" )
#nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
plt.title("CIC-IDS-2017 HTTP-TCP Decision Tree F1 score as Directed Graph")
plt.show()
