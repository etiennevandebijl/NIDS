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


def go_or_create_folder(path, folder):
    if not os.path.isdir(path+folder):
        os.mkdir(path + folder)
    return path + folder + "/"
