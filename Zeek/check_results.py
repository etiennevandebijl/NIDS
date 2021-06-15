import os
import pathlib
import datetime
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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

#%% Graph

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

for exp in ["CIC-IDS-2017", "UNSW-NB15", "ISCX-IDS-2012"]:
    for protocol in ["dns", "ftp", "http", "ssh", "ssl", "udp", "tcp"]:
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

#%% Unsupervised

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
       
for exp in ["CIC-IDS-2017", "ISCX-IDS-2012", "UNSW-NB15"]:
    for version in ["2_Preprocessed","3_Downsampled"]:
        for protocol in ["dns","ftp","http","ssh","ssl","udp","tcp","ftp-tcp","ssh-tcp","ssl-tcp","http-tcp"]:
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

plt.figure(figsize = (10,10))
sns.scatterplot(data = df_exists, x = "Modified Time", y = "Experiment")
plt.show()

# TO DO: ISCX-IDS-2012 -- 2_Preprocessed -- http-tcp -- all models

#%% Supervised Holdout

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
split = "0"

for exp in ["CIC-IDS-2017", "ISCX-IDS-2012", "UNSW-NB15"]:
    for version in ["2_Preprocessed","3_Downsampled"]:
        for protocol in ["dns","ftp","http","ssh","ssl","udp","tcp","http-tcp","ftp-tcp","ssh-tcp","ssl-tcp",'dns-udp']:
            source_dataset_path = get_data_folder(exp, "BRO", version) + "Train-Test " + split + "/" + protocol + "_train.txt"
            if not os.path.isfile(source_dataset_path):
                continue
            output_path = get_results_folder(exp, "BRO", version, "Supervised") + "Train-Test " + split +"/Holdout/" + part + "/" + protocol + "/" 
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


#%% Supervised Transfer Learning

def transfer_files(source_dataset_path):
    labels = determine_labels(source_dataset_path)
    
    attacks = [l for l in labels if l != "Benign"]
    subfolders = []
    ps = list(powerset(attacks))
    for train_case in ps:
        if len(train_case) > 0:
            folder_name = create_foldername(train_case)
            for l in attacks:
                subfolders.append(l + "/" + folder_name + "/")
            if len(attacks) > 1:
                subfolders.append("Malicious/" + folder_name + "/")

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

for exp in ["CIC-IDS-2017","ISCX-IDS-2012", "UNSW-NB15","CIC-IDS-2018"]:
    for protocol in ["dns","ftp","http","ssh","ssl","udp","tcp","http-tcp","ftp-tcp","ssh-tcp","ssl-tcp",'dns-udp']:
        source_dataset_path = get_data_folder(exp, "BRO", "2_Preprocessed_DDoS") + "Train-Test 0/" + protocol + "_train.txt"
        if not os.path.isfile(source_dataset_path):
            continue
        output_path = get_results_folder(exp, "BRO", "2_Preprocessed_DDoS", "Supervised") + "Train-Test 0/Paper/" + protocol + "/"
        files = transfer_files(source_dataset_path)
        exists, missing = analyse_check_files(files, source_dataset_path, output_path, exp, "2_Preprocessed_DDoS", protocol)
        exists_list.extend(exists)
        missing_list.extend(missing)   
            
df_exists = pd.DataFrame(exists_list, columns = ["Experiment", "Version", "Protocol", "File",
                                                 "Path", "Modified Time", "On Time"])
df_missing = pd.DataFrame(missing_list, columns = ["Experiment", "Version", "Protocol", 
                                                  "File", "Path"])
#df_missing = df_missing[df_missing["Path"].str.contains("CIC")]
df_missing = df_missing[df_missing["Path"].str.contains("CIC-IDS-2018")]
df_missing = df_missing[df_missing["Path"].str.contains("DT")]