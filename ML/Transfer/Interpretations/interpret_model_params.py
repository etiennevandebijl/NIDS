import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import joblib

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

    for file in glob.glob(input_path + '**/opt_clf.joblib', recursive=True):
        tags = file.split(os.sep)
        model = tags[-2]
        train_attacks = tags[-3].split(" ")
        test_attack = tags[-4]

        train_attacks = [NAMES_[l] for l in train_attacks]
        number_of_attacks = len(train_attacks)

        clf = joblib.load(file)
        
        results.append([model, test_attack, len(train_attacks), str(train_attacks),
                        rs, clf.get_params()] )

#%% RF

params = ["criterion", "class_weight", "n_estimators"]

results_RF = []
for result in results:
    if result[0] == "RF":
        dict_r = {k: v for k, v in result[-1].items() if k in params}
        results_RF.append(dict_r)

df_RF = pd.DataFrame(results_RF)
for col in df_RF:
    plt.figure()
    df_RF[col].value_counts().plot.bar()
    plt.show()
    
#%% KNN
params = ["algorithm"]

results_KNN = []
for result in results:
    if result[0] == "KNN":
        dict_r = {k: v for k, v in result[-1].items() if k == "algorithm"}
        results_KNN.append(dict_r)

df_KNN = pd.DataFrame(results_KNN)
for col in df_KNN:
    plt.figure()
    df_KNN[col].value_counts().plot.bar()
    plt.show()
    

#%% DT

params = ["criterion", "splitter", "class_weight", "max_features"]

results_DT = []
for result in results:
    if result[0] == "DT":
        dict_r = {k: v for k, v in result[-1].items() if k in params}
        results_DT.append(dict_r)

df_DT = pd.DataFrame(results_DT)
for col in df_DT:
    plt.figure()
    df_DT[col].value_counts().plot.bar()
    plt.show()