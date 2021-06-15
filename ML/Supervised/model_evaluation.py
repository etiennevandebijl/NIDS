import os
import glob
import json
import warnings
import joblib

from project_paths import get_data_folder, get_results_folder
from Zeek.utils import read_preprocessed
from ML.Supervised.fit_model import perform_train_test
from ML.Supervised.output import store_results
from ML.utils import rename_and_select_labels, create_output_path

from application import Application, tk

warnings.filterwarnings("ignore")

def compute_and_store_results(df_train, df_test, models, group_labels, select_classes,
                              output_path, protocol, folder_name):
    output_path = create_output_path(output_path, protocol, folder_name)
    df_train_ = rename_and_select_labels(df_train, group_labels, select_classes)
    df_test_ = rename_and_select_labels(df_test, group_labels, select_classes)
    results = perform_train_test(df_train_, df_test_, models)
    store_results(results, output_path)

def retrieve_models_dict(path, protocol, folder_name):
    models = {}
    for file_path in glob.glob(path + protocol + '/' + folder_name + \
                               "/**/opt_clf.joblib", recursive=True):
        models[file_path.split(os.sep)[-2]] = joblib.load(file_path)
    return models

def main_clf_sl(experiment, version, protocols):
    data_path = get_data_folder(experiment, "BRO", version) + "Train-Test 0/"
    models_path = get_results_folder(experiment, "BRO", version, "Supervised") + \
                                     "Train-Test 0/Holdout/Selection/"
    output_path = models_path.replace("Selection", "Evaluation")

    for protocol in protocols:
        print("---" + experiment + "--" + version + "--" + protocol.upper() + "----")
        try:
            df_train = read_preprocessed(data_path + protocol + "_train.csv")
            df_test = read_preprocessed(data_path + protocol + "_test.csv")
        except:
            continue
        
        for folder_name in os.listdir(models_path + protocol):
            if not "png" in folder_name:
                with open(models_path + protocol + "/" + folder_name + "/" + \
                          "labels_info.json") as file:
                    labels_info = json.load(file)
                group_labels = labels_info["group_labels"]
                selected_labels = labels_info["selected_labels"]

                models = retrieve_models_dict(models_path, protocol, folder_name)
                for m in ["DT","GNB","ADA","RF"]:
                    if m in models.keys():
                        models.pop(m)
                compute_and_store_results(df_train, df_test, models, group_labels,
                                          selected_labels, output_path, protocol, folder_name)

if __name__ == "__main__":
    APP = Application(master=tk.Tk(), v_setting=5)
    APP.mainloop()
    for exp in APP.selected_values["Experiments"]:
        for vers in APP.selected_values["Version"]:
            main_clf_sl(exp, vers, APP.selected_values["Files"])
