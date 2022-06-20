import os
import glob
import pandas as pd
import numpy as np

from project_paths import get_results_folder
from ML.Transfer.experimental_setup import NAMES
NAMES_ = {y: x for x, y in NAMES.items()}

DATASET = "CIC-IDS-2017"
PROTOCOL = "http-FIX-tcp-FIX"
RS = 20

MODELS = ['GNB', "DT", "RF", "KNN"]

#%% 

results = []
for rs in range(RS):
    input_path = get_results_folder(DATASET, "BRO", "2_Preprocessed_DDoS",
                                "Supervised") + "Train-Test " + str(rs) + "/Paper/" + PROTOCOL + "/"

    for file in glob.glob(input_path + '**/scores.csv', recursive=True):
        tags = file.split(os.sep)
        model = tags[-2]
        train_attacks = tags[-3].split(" ")
        test_attack = tags[-4]

        train_attacks = [NAMES_[l] for l in train_attacks]
        number_of_attacks = len(train_attacks)

        df = pd.read_csv(file, sep=";", decimal=",", index_col=0).fillna(0)

        precision = df.loc["Malicious", "Precision"]
        recall = df.loc["Malicious", "Recall"]
        f1 = df.loc["Malicious", "F1 Score"]
    
        results.append([test_attack, len(train_attacks), str(train_attacks),
                        model, precision, recall, f1, rs] )

df = pd.DataFrame(results, columns = ["Test", "Number of trained D(D)oS attacks",
                                      "Train", "Model", "Pr", "Rc", 'f1', 'RS'])

 # %%

df_ = df[df["Number of trained D(D)oS attacks"] == 1]
df_ = df_[df_["Test"] != "Malicious"]
df_["Train"] = df_["Train"].map(lambda x: x.replace("['","").replace("']",""))
df_ = df_[df_["Test"] == df_["Train"]]
df_ = df_.drop(["Number of trained D(D)oS attacks", "Train"], axis = 1)
df_["Test"] = df_["Test"].str.replace("DDoS - ","").str.replace("DoS - ","")

#%%

df__m = df_.groupby(["Test", "Model"])[["f1"]].agg(['mean', 'std']).reset_index()
df__m.columns = ["Test", "Model", "Mean", "Std"]

df__m["Std"] = (df__m["Std"] * 10).round(3)
df__m["Mean"] = df__m["Mean"].round(4)
df__m = df__m.pivot_table(values = ["Mean", "Std"], index = ["Test"], columns = ["Model"])
df__m = df__m.swaplevel(0, 1, 1).sort_index(1)
df__m = df__m.reindex(MODELS, axis=1, level=0)
not_one = df__m != 1.0 
df__m = df__m.astype(str)[not_one]
df__m = df__m.fillna("1.0000")
df__m = df__m.replace("0.0","0.000")

#%% Precision Recall

df__ = df_.groupby(["Test", "Model"])[["Pr","Rc"]].mean().reset_index() 
df__ = df__.pivot_table(values = ["Pr","Rc"], index = ["Test"], columns = ["Model"]) * 1000
df__ = df__.reindex(MODELS, axis=1, level=1)
not_one = df__ < 1000
df__ = df__.apply(np.floor).astype(int).astype(str)[not_one]
df__ = "0." + df__
df__ = df__.fillna("1.000")






