import os
import pathlib
import datetime
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from project_paths import get_data_folder, get_results_folder
from ML.Transfer.experimental_setup import powerset, create_foldername

EXPERIMENTS = ["CIC-IDS-2017", "UNSW-NB15", "ISCX-IDS-2012"]
PROTOCOLS = ["dns", "ftp", "http", "ssh", "ssl", "udp", "tcp",
             "ftp-tcp", "ssh-tcp", "ssl-tcp", "http-tcp", "dns-udp"]

# %% Functions

def check_os_path_isdir_dataset(experiments, version, files):
    "This function looks if the datasets exists."
    exists_list = []
    missing_list = []
    for exp in experiments:
        for file in files:
            path = get_data_folder(exp, "BRO", version) + file + ".csv"
            if os.path.exists(path):
                exists_list.append([exp, version, file, path]) 
            else:
                missing_list.append([exp, version, file, path])
    COLUMNS = ["Experiment", "Version", "File", "Path"]
    df_exists = pd.DataFrame(exists_list, columns = COLUMNS)
    df_missing = pd.DataFrame(missing_list, columns = COLUMNS)
    return df_exists, df_missing

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

# %% Graph

df_exists, df_missing = check_os_path_isdir_dataset(EXPERIMENTS, "4_Feature_Reduction", PROTOCOLS)
TIMES = ["5s", "1min", "2min", "10min", "30min", "60min"]
files = [ p + "-edges-" + t for p in PROTOCOLS for t in TIMES]
df_exists, df_missing = check_os_path_isdir_dataset(EXPERIMENTS, "5_Graph", files)

def files_graph():
    files = ['distance-metrics.csv', 'metric_comparison.csv']
    for dist in ["ED", "WD", "UD", "MCSWD"]:
        for model in ["IForest_5", "IForest_10", "PCA_0.1", "PCA_0.5","PCA_0.9"]:
            files.append("Curves/"+dist+"-"+model+"scores-per-threshold.png")
            files.append("Distances/"+dist+"-"+model+".png")  

    for dist in ["MCSED","MCSVD","NED","VEO"]:
        files.append("Curves/"+dist+"scores-per-threshold.png")
        files.append("Distances/"+dist+".png")
    return files

exists_list = []
missing_list = []

for exp in EXPERIMENTS:
    for protocol in PROTOCOLS:
        for time in ["5s", "1min", "2min", "10min", "30min", "60min"]:
            source_dataset_path = get_data_folder(exp, "BRO", "5_Graph") + protocol + "-edges-" + time + ".csv"
            if not os.path.isfile(source_dataset_path):
                continue
            output_path = get_results_folder(exp, "BRO", "5_Graph", protocol) + time + "/Delta1/" 
            files = files_graph()
            exists, missing = analyse_check_files(files, source_dataset_path, output_path, exp, "5_Graph", protocol)
            exists_list.extend(exists)
            missing_list.extend(missing)
            
df_exists = pd.DataFrame(exists_list, columns = ["Experiment", "Version", "Protocol", "File",
                                                 "Path", "Modified Time", "On Time"])
df_missing = pd.DataFrame(missing_list, columns = ["Experiment", "Version", "Protocol", 
                                                  "File", "Path"])

plt.figure(figsize = (10,10))
sns.scatterplot(data = df_exists, x = "Modified Time", y = "Experiment")
plt.show()

# %% Unsupervised

df_exists, df_missing = check_os_path_isdir_dataset(EXPERIMENTS, "2_Preprocessed", PROTOCOLS)

def files_unsupervised(source_dataset_path):
    files_ = ["boxplot-anomaly-score-per-label.png","class_comparison.csv",
              "clf.joblib","max-F1-malicious-labelled-per-label.png",
              "P-malicious-labelled-per-label.png",'scores-per-threshold.png']
    
    subfolders = []
    labels = determine_labels(source_dataset_path)
    for l in labels:
        if l != "Benign":
            subfolders.append("Benign vs " + l + "/") 
    if len(labels) > 2:
        subfolders.append("Benign vs Malicious/") 
    
    files = []
    for sf in subfolders:
        files.append(sf + "anomaly-scores.csv")
        files.append(sf + "labels_info.json")
        files.append(sf + "model_comparison.csv")

        for model in ["IForest_5", "IForest_10", "PCA_0.1", "PCA_0.5", "PCA_0.9"]:
            for f in files_:
                files.append(sf + model + "/" + f)
    return files
    
exists_list = []
missing_list = []

for exp in EXPERIMENTS:
    for version in ["2_Preprocessed","3_Downsampled"]:
        for protocol in PROTOCOLS:
            source_dataset_path = get_data_folder(exp, "BRO", version) + protocol + ".txt"
            if not os.path.isfile(source_dataset_path):
                continue
            output_path = get_results_folder(exp, "BRO", version, "Unsupervised") + protocol + "/"
            files = files_unsupervised(source_dataset_path)
            exists, missing = analyse_check_files(files, source_dataset_path, output_path, exp, version, protocol)
            exists_list.extend(exists)
            missing_list.extend(missing)

df_exists = pd.DataFrame(exists_list, columns = ["Experiment", "Version", "Protocol", "File",
                                                 "Path", "Modified Time", "On Time"])
df_missing = pd.DataFrame(missing_list, columns = ["Experiment", "Version", "Protocol",
                                                  "File", "Path"])

# plt.figure(figsize = (10,10))
# sns.scatterplot(data = df_exists, x = "Modified Time", y = "Experiment")
# plt.show()

# %% Supervised Holdout

def files_supervised(source_dataset_path):
    subfolders = []
    labels = determine_labels(source_dataset_path)
    for l in labels:
        if l != "Benign":
            subfolders.append("Benign vs " + l + "/") 
    if len(labels) > 2:
        subfolders.append("Benign vs Malicious/") 
        subfolders.append("Complete/") 
                
    files = []
    for sf in subfolders:
        files.append(sf + "feature_importance.csv")
        files.append(sf + "model-comp.png")

        for model in ["DT","ADA","GNB","KNN","RF"]:
            files.append(sf + model + "/scores.csv")
            files.append(sf + model + "/opt_clf.joblib")
            files.append(sf + model + "/" + model + " score.png")
        for model in ["DT","ADA","RF"]:
            files.append(sf + model + "/feature-importance.csv")
            files.append(sf + model + "/feature-importance.png")
    return files
    
exists_list = []
missing_list = []

part = "Evaluation"
RS = 0

for exp in EXPERIMENTS:
    for version in ["2_Preprocessed","3_Downsampled"]:
        for protocol in PROTOCOLS:
            source_dataset_path = get_data_folder(exp, "BRO", version) + "Train-Test " + str(RS) + "/" + protocol + "_train.txt"
            if not os.path.isfile(source_dataset_path):
                continue
            output_path = get_results_folder(exp, "BRO", version, "Supervised") + "Train-Test " + str(RS) +"/Holdout/" + part + "/" + protocol + "/" 
            files = files_supervised(source_dataset_path)
            exists, missing = analyse_check_files(files, source_dataset_path, output_path, exp, version, protocol)
            exists_list.extend(exists)
            missing_list.extend(missing)   
            
df_exists = pd.DataFrame(exists_list, columns = ["Experiment", "Version", "Protocol", "File",
                                                 "Path", "Modified Time", "On Time"])
df_missing = pd.DataFrame(missing_list, columns = ["Experiment", "Version", "Protocol", 
                                                  "File", "Path"])

plt.figure(figsize = (10,10))
sns.scatterplot(data = df_exists, x = "Modified Time", y = "Experiment")
plt.show()

# %% Supervised Transfer Learning

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
            # files.append(sf + model + "/opt_clf.joblib")
            # files.append(sf + model + "/" + model + " score.png")
        # for model in ["DT", "RF"]:
        #     files.append(sf + model + "/feature-importance.csv")
        #     files.append(sf + model + "/feature-importance.png")
    return files

exists_list = []
missing_list = []

EXP_RS = {"CIC-IDS-2018": 10}

for exp in EXP_RS.keys():
    for protocol in ["http-FIX-tcp-FIX"]:
        for RS in range(EXP_RS[exp]):
            train_dataset_path = get_data_folder(exp, "BRO", "2_Preprocessed_DDoS") + "Train-Test " + str(RS) + "/" + protocol + "_train.txt"
            if not os.path.isfile(train_dataset_path):
                continue
            test_dataset_path = train_dataset_path.replace("train","test")

            output_path = get_results_folder(exp, "BRO", "2_Preprocessed_DDoS", "Supervised") + "Train-Test " + str(RS) + "/Paper/" + protocol + "/"
            files = transfer_files(train_dataset_path, test_dataset_path)
            exists, missing = analyse_check_files(files, train_dataset_path, output_path, exp, "2_Preprocessed_DDoS", protocol)
            missing = [a + [a[4].replace(output_path,"").split("/")[0], a[4].replace(output_path,"").split("/")[1],  RS] for a in missing]
            missing = [a + [a[4].replace(output_path,"").split("/")[2] if len(a[4].replace(output_path,"").split("/")) == 4 else ""] for a in  missing]
            exists_list.extend(exists)
            missing_list.extend(missing)

df_exists = pd.DataFrame(exists_list, columns = ["Experiment", "Version", "Protocol", "File",
                                                 "Path", "Modified Time", "On Time"])
df_missing = pd.DataFrame(missing_list, columns = ["Experiment", "Version", "Protocol", 
                                                  "File", "Path", "Train", "Test", "RS", "Model"])
df_missing = df_missing[['Experiment', 'Version', 'Protocol',  'Train', 'Test','Model','RS', 'File','Path']]

# plt.figure(figsize = (10,10))
# sns.scatterplot(data = df_exists, x = "Modified Time", y = "Experiment")
# plt.show()

df_missing = df_missing[df_missing["Model"] == 'RF']

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