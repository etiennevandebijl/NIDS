import os
import glob
import pandas as pd
import ast

from project_paths import get_results_folder
from ML.Transfer.experimental_setup import NAMES
NAMES_ = {y: x for x, y in NAMES.items()}

DATASET = "CIC-IDS-2017"
PROTOCOL = "http-tcp"
RS = 20

#%% 

results = []
for rs in range(RS):
    input_path = get_results_folder(DATASET, "BRO", "2_Preprocessed_DDoS",
                                "Supervised") + "Train-Test " + str(rs) + "/Paper/" + PROTOCOL + "/"

    for file in glob.glob(input_path + '**/scores.csv', recursive=True):
        tags = file.split(os.sep)
        model = tags[-2]
        train_attacks = tags[-3].split(" ")
        train_attacks = [NAMES_[l] for l in train_attacks]
        test_attack = tags[-4]
        
        df = pd.read_csv(file, sep=";", decimal=",", index_col=0).fillna(0)
        f1 = df.loc["Malicious", "F1 Score"]
    
        if test_attack != "Malicious":
            results.append([test_attack, len(train_attacks), str(train_attacks),
                        model, f1, rs] )

df = pd.DataFrame(results, columns = ["Test", "Number of trained D(D)oS attacks",
                                      "Train", "Model", "F1", 'RS'])

#%%

df = df.groupby(['Test', "Number of trained D(D)oS attacks", 'Train', 'Model'])['F1'].mean().reset_index()

#%% Ignore instances where Train is in Test

pd_list = []
for index, group in df.groupby(["Test", "Model"]):
    group_ = group[~group["Train"].str.contains(index[0])]
    pd_list.append(group_)
df = pd.concat(pd_list)

#%% Make matrix with adding one attack

results = []
for index, group in df.groupby(["Model", "Test"]):

    for _, row in group.iterrows():
        train = ast.literal_eval(row["Train"])

        if len(train) == 1:
            continue
        
        sub_group = group[(group["Number of trained D(D)oS attacks"] == len(train) - 1)]

        for attack in train:
            sub_train = [a for a in train if a != attack]
            hit_group = sub_group[sub_group["Train"] == str(sub_train)]
            
            if hit_group.shape[0] == 1:
                F1_ = hit_group["F1"].values[0]
                results.append([index[1], str(sub_train), str(train), 
                                attack, index[0], F1_, row["F1"]])
            else:
                print("BIG WARNING")


df_results = pd.DataFrame(results, columns = ["Test", "Train_", "Train", "Attack", "Model", "F1_", "F1"])

#%% Analysis

df_results["Diff"] = df_results["F1"] - df_results["F1_"]

df_rest = df_results.groupby(["Test", "Model", "Attack"])["Diff"].mean().reset_index()

# Find maximum change
pd_index_list = []
for index, group_ in df_results.groupby(["Test"]):
    max_index = group_["F1"].idxmax()
    pd_index_list.append(group_.loc[max_index])

df_result = pd.DataFrame(pd_index_list)
df_result.drop(["Train"], axis = 1, inplace=True)
        
    
    
    