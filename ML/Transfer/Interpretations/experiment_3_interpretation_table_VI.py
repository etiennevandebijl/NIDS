import os
import glob
import pandas as pd
import numpy as np

from project_paths import get_results_folder
from ML.Transfer.experimental_setup import NAMES
NAMES_ = {y: x for x, y in NAMES.items()}

DATASET = "CIC-IDS-2018"
VARIANT = "Web"
EXPERIMENT = "Paper"

PROTOCOL = "http-FIX-tcp-FIX"
RS = 20
if DATASET == "CIC-IDS-2018":
    RS = 10

#%% 

results = []
for rs in range(RS):
    input_path = get_results_folder(DATASET, "Zeek", "2_Preprocessed_" + VARIANT,
                                "Supervised") + "Train-Test " + str(rs) + \
                                "/" + EXPERIMENT + "/" + PROTOCOL + "/"

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
    
        if test_attack != "Malicious":
            results.append([test_attack, str(train_attacks),
                        model, f1, rs] )

df = pd.DataFrame(results, columns = ["Test", "Train", "Model", "F1", 'RS'])

#%% Summarize

df = df.groupby(['Test', 'Train', 'Model'])['F1'].mean().reset_index()

# %% Ignore Train in Test

pd_list = []
for index, group in df.groupby(["Test", "Model"]):
    group_ = group[~group["Train"].str.contains(index[0])]
    pd_list.append(group_)

df = pd.concat(pd_list)

#%%

df["Test"] = df["Test"].str.replace("DDoS - ","").str.replace("DoS - ","")    
df["Train"] = df["Train"].str.replace("DDoS - ","").str.replace("DoS - ","")   


# Best F1 score for combination Model and Test
indexes = []
for index, group in df.groupby(["Test", "Model"]):
    max_index = group["F1"].idxmax()
    indexes.append(max_index)
df_M_T = df.loc[indexes,:].reset_index(drop=True)

df_M_T = pd.pivot_table(df_M_T, columns = "Model", index = "Test")  
df_M_T = df_M_T * 1000
df_M_T = df_M_T.apply(np.floor).astype(int).astype(str)
df_M_T = "0." + df_M_T
df_M_T = df_M_T.sort_index()

# Best F1 score for Test
indexes = []
for index, group in df.groupby(["Test"]):
    max_index = group["F1"].idxmax()
    indexes.append(max_index)
df_T = df.loc[indexes,:].reset_index(drop=True)
df_T = df_T.sort_values(by = ["Test"])
df_T["Train"] = df_T["Train"].str.replace("[","{").str.replace("]","}").str.replace("'","")

df_M_T["Train Set Opt Model"] = df_T["Train"].values

