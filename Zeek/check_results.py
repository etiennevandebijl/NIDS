import os
import pathlib
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from project_paths import get_data_folder, get_results_folder
from ML.Transfer.experimental_setup import powerset, create_foldername

# %% Functions

def analyse_check_files(files, source_path, target_path, exp, version, protocol):
    fname = pathlib.Path(source_path)
    source_time = datetime.datetime.fromtimestamp(fname.stat().st_mtime)   
    exists = []    
    missing = []   
    for f in files:
        target = target_path + f
        base = [exp, version, protocol, os.path.basename(target), target]    
        if os.path.isfile(target):
            fname = pathlib.Path(target)
            target_time = datetime.datetime.fromtimestamp(fname.stat().st_mtime) 
            exists.append(base + [target_time, source_time < target_time])
        else:
            missing.append(base)
    return exists, missing

def determine_labels(file_info_path):
    '''This function looks in the summary file or a dataset for the labels'''
    labels = []
    read_line = False
    with open(file_info_path) as f:
        lines = f.readlines()
        for line in lines:
            if "Label stats" in line:
                read_line = True
                continue
            if "Name: Label, dtype: int64" in line:
                read_line = False
            if read_line:
                labels.append(line.split("    ")[0])
    return labels

def transfer_files(train_dataset_path, test_dataset_path):
    train_labels = determine_labels(train_dataset_path)
    train_attacks = [l for l in train_labels if l != "Benign"]
    test_labels = determine_labels(test_dataset_path)    
    test_attacks = [l for l in test_labels if l != "Benign"]    
    if len(test_attacks) > 1:
        test_attacks.append("Malicious")

    subfolders = []
    for test_attack in test_attacks:
        for train_attack_ss in list(powerset(train_attacks)):
            if len(train_attack_ss) > 0:
                folder_name = create_foldername(train_attack_ss)
                subfolders.append(test_attack + "/" + folder_name + "/")

    files = []
    for sf in subfolders:
        files.append(sf + "feature_importance.csv")
        files.append(sf + "model-comp.png")

        for model in ["DT", "GNB", "RF", "KNN"]:
            files.append(sf + model + "/scores.csv")
            files.append(sf + model + "/opt_clf.joblib")
            files.append(sf + model + "/" + model + " score.png")
        for model in ["DT", "RF"]:
            files.append(sf + model + "/feature-importance.csv")
            files.append(sf + model + "/feature-importance.png")
    return files

#%% 
PROTOCOL = "http-FIX-tcp-FIX"
PLOT = False

EXPERIMENT = "Experiment"
VARIANT = "Web"
DATASET = "CIC-IDS-2018"

RS = 20
if DATASET == "CIC-IDS-2018":
    RS = 10

def check_results():
    exists_list = []
    missing_list = []
    
    for rs in range(RS):
        train_dataset_path = get_data_folder(DATASET, "BRO", "2_Preprocessed_" + \
                                             VARIANT) + "Train-Test " + str(rs) + \
                                            "/" + PROTOCOL + "_train.txt"
        if not os.path.isfile(train_dataset_path):
            continue
        test_dataset_path = train_dataset_path.replace("train","test")

        output_path = get_results_folder(DATASET, "BRO", "2_Preprocessed_" + \
                                         VARIANT, "Supervised") + "Train-Test " + \
                                         str(rs) + "/" + EXPERIMENT + "/" + PROTOCOL + "/"
        files = transfer_files(train_dataset_path, test_dataset_path)
        
        exists, missing = analyse_check_files(files, train_dataset_path, output_path, DATASET, "2_Preprocessed_" + VARIANT, PROTOCOL)
        missing = [a + [a[4].replace(output_path,"").split("/")[0], a[4].replace(output_path,"").split("/")[1],  rs] for a in missing]
        missing = [a + [a[4].replace(output_path,"").split("/")[2] if len(a[4].replace(output_path,"").split("/")) == 4 else ""] for a in  missing]
        exists_list.extend(exists)
        missing_list.extend(missing)
    
    df_exists = pd.DataFrame(exists_list, columns = ["Experiment", "Version", "Protocol", "File",
                                                 "Path", "Modified Time", "On Time"])
    df_missing = pd.DataFrame(missing_list, columns = ["Experiment", "Version", "Protocol", 
                                                  "File", "Path", "Train", "Test", "RS", "Model"])
    df_missing = df_missing[['Experiment', 'Version', 'Protocol', 'Train', 'Test', 'Model', 'RS', 'File', 'Path']]
    
    if PLOT:
        plt.figure(figsize = (10,10))
        sns.scatterplot(data = df_exists, x = "Modified Time", y = "Experiment")
        plt.show()

    return df_exists, df_missing


df_exists, df_missing = check_results()

# %%

train_dataset_path = get_data_folder("CIC-IDS-2017", "BRO", "2_Preprocessed_DDoS") + "http-tcp.txt"
test_dataset_path = get_data_folder("CIC-IDS-2018", "BRO", "2_Preprocessed_DDoS") + "http-tcp.txt"
output_path = get_results_folder("CIC-IDS-2017_CIC-IDS-2018", "BRO", "2_Preprocessed_DDoS", "Supervised") + "/Paper/http-tcp/"
files = transfer_files(train_dataset_path, test_dataset_path)
exists, missing = analyse_check_files(files, train_dataset_path, output_path, "CIC-IDS_2017_CIC-IDS-2018", "2_Preprocessed_DDoS", protocol)
missing = [a + [a[4].replace(output_path,"").split("/")[0], a[4].replace(output_path,"").split("/")[1]] for a in missing]
missing = [a + [a[4].replace(output_path,"").split("/")[2] if len(a[4].replace(output_path,"").split("/")) == 4 else ""] for a in missing]

df_exists = pd.DataFrame(exists, columns = ["Experiment", "Version", "Protocol", "File",
                                                 "Path", "Modified Time", "On Time"])
df_missing = pd.DataFrame(missing, columns = ["Experiment", "Version", "Protocol", 
                                                  "File", "Path", "Train", "Test", "Model"])
df_missing = df_missing[['Experiment', 'Version', 'Protocol',  'Train', 'Test', 'Model',  'File','Path']]
