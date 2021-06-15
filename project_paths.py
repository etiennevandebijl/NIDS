import os
import pandas as pd

if os.path.isdir('C:/Users/Etienne/'):
    PROJECT_PATH = "C:/Users/Etienne/Dropbox/Internship Business Analytics/Project Graph-Based Intrusion Detection/"
else:
    PROJECT_PATH = "/home/etienne/Dropbox/Internship Business Analytics/Project Graph-Based Intrusion Detection/"

NID_PATH = PROJECT_PATH + "Intrusion Detection Datasets/"

def get_labelling_scheme(experiment_name):
    path = NID_PATH + experiment_name + "/Experiment setup/Labeling_scheme.csv"
    return pd.read_csv(path, sep=";", parse_dates=["Start", "End"])

def get_data_folder(experiment_name, analyser, version):
    return NID_PATH + experiment_name + "/" + analyser + "/" + version + "/"

def get_results_folder(experiment_name, analyser, version, method):
    path = PROJECT_PATH + "Results/" + experiment_name + "/" + analyser + "/" + version + "/" + method + "/"
    return path

# =============================================================================
# Folder creation
# =============================================================================

def go_or_create_folder(path, folder):
    if not os.path.isdir(path+folder):
        os.mkdir(path + folder)
    return path + folder + "/"

def latest_run_path(output_path, folders):
    for folder in folders:
        output_path = go_or_create_folder(output_path, folder)

    _, dirs, _ = next(os.walk(output_path))
    file_count = len(dirs)

    if file_count > 0:
        i = 0
        exists = True
        while exists:
            i = i + 1
            new_path = output_path + str(i)
            exists = os.path.isdir(new_path)
        os.rename(output_path + "AUTO/", output_path + str(i) + "/")
    return go_or_create_folder(output_path, "AUTO")
