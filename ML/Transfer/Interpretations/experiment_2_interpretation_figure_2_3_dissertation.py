import os
import glob
import pandas as pd
#import networkx as nx
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

from project_paths import get_results_folder, go_or_create_folder
from ML.Transfer.experimental_setup import NAMES
NAMES_ = {y: x for x, y in NAMES.items()}

DATASET = "CIC-IDS-2017_CIC-IDS-2018"
#DATASET = "CIC-IDS-2018"
VARIANT = "DDoS"
EXPERIMENT = "Paper"

PROTOCOL = "http-tcp"
RS = 1
if DATASET == "CIC-IDS-2017":
    RS = 20
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
    df__ = pd.concat([df__, pd.DataFrame([{'Test': bl[0], "Model":"DD baseline", "F1":bl[1]
                        , "Train":"", "Train - Model": " DD baseline"
                        }])], ignore_index=True)

df__ = df__.pivot_table(values = "F1", index = ["Test"], columns = ["Train - Model"]).T

if VARIANT == "Web":
    plt.figure(figsize = (7,7))
else:
    plt.figure(figsize = (10,10))
ax = sns.heatmap(df__, annot = np.array(["{:.3f}".format(data)
                            for data in df__.values.ravel()]).reshape(
                                    np.shape(df__)), vmin=0.0, vmax=1.0,
                  cmap = "RdYlGn", fmt='',
                  cbar_kws = dict(use_gridspec=True, location="right", label="Average $F_1$ Score", shrink = 0.75))
ax.axhline(1, color='white', lw=5)
ax.axhline(5, color='white', lw=5)
ax.axhline(9, color='white', lw=5)
ax.axhline(13, color='white', lw=5)
ax.axhline(17, color='white', lw=5)
ax.axhline(21, color='white', lw=5)
plt.xticks(rotation=45)
plt.ylabel("Training attack - Classifier")
plt.xlabel("Testing attack")

pathje = get_results_folder(DATASET, "Zeek", "2_Preprocessed_" + VARIANT, "Supervised") + "Paper-Results/"
pathje = go_or_create_folder(pathje, "Heatmap")
plt.tight_layout()
plt.savefig(pathje + "Results Experiment 2 " + DATASET + " " + VARIANT + "-dissertation.png", dpi = 400)
plt.show()