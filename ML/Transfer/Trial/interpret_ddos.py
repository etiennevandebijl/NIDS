import os
import glob
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from project_paths import get_results_folder

input_path = get_results_folder("CIC-IDS-2017", "BRO", "2_Preprocessed_DDoS", "Supervised") + "Train-Test 0/DDoS/http-tcp/"

attacks = {}
attacks2 = {}
i = 1
for folder in os.listdir(input_path):
    train_attacks = folder.split(" ")
    if len(train_attacks) == 1:
        attacks[train_attacks[0]] = str(i)
        attacks2[i] = train_attacks[0]
        i = i + 1

results = []
for folder in os.listdir(input_path):
    train_attacks = folder.split(" ")
    train_attacks = [attacks[x] for x in train_attacks]
    name = ",".join(train_attacks)
    for f in glob.glob(input_path + folder + "/**/scores.csv", recursive=True):
        model = f.split("\\")[1]
        df = pd.read_csv(f, sep=";", decimal=",", index_col=0).fillna(0)
        f1 = df.loc["Malicious", "F1 Score"]
        results.append([model, len(train_attacks),name,f1])
        
df = pd.DataFrame(results, columns = ["Model", "Number of trained D(D)oS attacks", "Name", "F1"])

def label_point(x, y, val, ax):
    a = pd.concat({'x': x, 'y': y, 'val': val}, axis=1)
    for i, point in a.iterrows():
        ax.text(point['x'], point['y'], str(point['val']))    
        
results_model = dict()
for model in df["Model"].unique():
    df_model = df[df["Model"]==model]
    df_min = df_model.groupby("Number of trained D(D)oS attacks")["F1"].min()
    df_max = df_model.groupby("Number of trained D(D)oS attacks")["F1"].max()
    results_model[model] = df_max
    
    df_max = df_max.reset_index()
    df_min = df_min.reset_index()
    df_max["Number of trained D(D)oS attacks"] = df_max["Number of trained D(D)oS attacks"] - 1
    df_min["Number of trained D(D)oS attacks"] = df_min["Number of trained D(D)oS attacks"] - 1
    
    f = plt.figure(figsize=(15,12)); ax = f.add_subplot(111)
    plt.title(model + " " + str(attacks2))
    sns.lineplot(x="Number of trained D(D)oS attacks", y="F1", data=df_max, ax=ax)
    sns.lineplot(x="Number of trained D(D)oS attacks", y="F1", data=df_min, ax=ax)
    sns.stripplot(x="Number of trained D(D)oS attacks", y="F1", data=df_model, ax=ax)
    plt.close(2)
    label_point(df_model["Number of trained D(D)oS attacks"] - 1, df_model["F1"], df_model["Name"], plt.gca())  
    plt.show()

df_results_model = pd.DataFrame(results_model)
df_results_model.drop(["GNB"], 1, inplace=True)
df_results_model.plot(figsize =(8,8)) 
plt.title("F1")
plt.show()    

# =============================================================================
# FP + FN
# =============================================================================

results = []
upperbound = 0
for folder in os.listdir(input_path):
    train_attacks = folder.split(" ")
    for f in glob.glob(input_path + folder + "/**/scores.csv", recursive = True):
        model = f.split("\\")[1]
        df = pd.read_csv(f, sep=";", decimal=",", index_col = 0).fillna(0)
        stat = df.loc["Malicious", "TP"]
        results.append([model, len(train_attacks),folder,stat])
        upperbound = df.loc["Malicious", "TP"] + df.loc["Malicious", "FN"]
        
df = pd.DataFrame(results, columns = ["Model","Number of trained D(D)oS attacks","Name","TP"])

results_model = dict()
for model in df["Model"].unique():
    df_model = df[df["Model"]==model]
    df_mean = df_model.groupby("Number of trained D(D)oS attacks")["TP"].mean()
    
    results_model[model] = df_mean
    
    df_mean = df_mean.reset_index()
    
    df_mean["Number of trained D(D)oS attacks"] = df_mean["Number of trained D(D)oS attacks"] - 1
    
    f = plt.figure(figsize=(15,12))
    ax = f.add_subplot(111)
    plt.title(model)
    plt.axhline(upperbound)
    sns.lineplot(x="Number of trained D(D)oS attacks", y="TP", data=df_mean, ax=ax)
    sns.stripplot(x="Number of trained D(D)oS attacks", y="TP", data=df_model, ax=ax)
    plt.close(2)
    plt.show()
df_results_model = pd.DataFrame(results_model)
df_results_model.drop(["GNB"], 1, inplace= True)
df_results_model.plot(figsize=(8,8)) 
plt.title("TP")
plt.show()    
    
    
    
    