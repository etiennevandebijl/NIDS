import glob
import warnings
import pandas as pd
from itertools import chain, combinations
from sklearn.model_selection import StratifiedShuffleSplit

from project_paths import get_data_folder, get_results_folder, go_or_create_folder
from Zeek.utils import read_preprocessed
from ML.Supervised.fit_model import perform_train_validation, perform_train_test
from ML.Supervised.output import store_results
from ML.utils import rename_and_select_labels
from ML.Transfer.models import models

from application import Application, tk

warnings.filterwarnings("ignore")

NAMES = {"DoS - Hulk": "Hulk",
         "DDoS - HOIC": "HOIC",
         "DDoS - LOIC": "LOIC",
         "DDoS - LOIC - HTTP": "HLOIC",
         "DDoS - LOIC - UDP": "ULOIC",
         "DoS - SlowHTTPTest": "Test",
         "DoS - GoldenEye": "Eye",
         "DDoS - Botnet": "Bot",
         "DoS - Slowloris": "Slow",
         "Web Attack - Brute Force": "BF",
         "Web Attack - XSS": "XSS",
         "Web Attack - SQL Injection": "SQL"}

# %% Settings

RS = range(10)
EXPERIMENT = "Paper"
BALANCING = False
if BALANCING:
    EXPERIMENT = "Experiment"
RESTRICT_TRAIN_LEN = False
TRAIN_VAR_LEN = 1
DOWN_SAMPLE_TRAIN = False
DOWN_SAMPLE_TRAIN_PERC = 0.1
DOWN_SAMPLE_TEST = False
DOWN_SAMPLE_TEST_PERC = 0.1

'''
For the 2018 dataset we need to sample data for the training.
GNB: nothing
DT + RF: In the hyperparameter tuning we sampled 10% with random_state = 0.
KNN: For KNN we did both train and test 1% to speed up the process for all models.

For 2017_2018 we can use all data. We only use train random state 0
For 2018_2017 we only used for now all data for GNB
For 2018_2017 10% for hyperparameter tuning for RF and DT
1% for both training and hyperparametertuning for KNN
'''
# %%


def powerset(iterable):
    l_iter = list(iterable)
    return chain.from_iterable(combinations(l_iter, r) for r in range(len(l_iter)+1))

def labels_check(df_train, df_test):
    labels_train = df_train["Label"].unique().tolist()
    labels_test = df_test["Label"].unique().tolist()
    if set(labels_train) != set(labels_test):
        print("BIG WARNING: Labels are not identical")

def create_foldername(train_case):
    attack_list = []
    for attack in list(train_case):
        if attack in NAMES.keys():
            attack_list.append(NAMES[attack])
        else:
            attack_list.append(attack)
    folder_name = ' '.join(sorted(attack_list))
    return folder_name

def select_train_labels(df_train, df_test, test_attack, output_path):
    labels = df_train["Label"].unique()
    attacks = [l for l in labels if l != "Benign"]
    if test_attack is not None:
        attacks = [l for l in attacks if l != test_attack]
    pow_s = [a for a in list(powerset(attacks)) if len(a) > 0]

    if RESTRICT_TRAIN_LEN:
            pow_s = [a for a in pow_s if len(a) == TRAIN_VAR_LEN]
    print(pow_s)
    for train_case in pow_s:
        folder_name = create_foldername(train_case)
        print(folder_name)
        output_path_case = go_or_create_folder(output_path, folder_name)

        df_train_ = rename_and_select_labels(df_train, {"Malicious": train_case},
                                            ["Benign", "Malicious"], output_path_case,
                                            "train_labels_info")

        if BALANCING:
            N = df_train_[df_train_["Label"] == "Benign"].shape[0]
            P = df_train_[df_train_["Label"] == "Malicious"].shape[0]

            if P < N:
                df_M = df_train_[df_train_["Label"] == "Malicious"]
                df_B = df_train_[df_train_["Label"] == "Benign"].sample(n=P, random_state=0)
                df_train_ = pd.concat([df_M, df_B], ignore_index = True)


        splitter = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=0)
            
        if DOWN_SAMPLE_TRAIN:
            df_train_d = df_train_.sample(frac = DOWN_SAMPLE_TRAIN_PERC, 
                                          random_state=0)
            results_search = perform_train_validation(df_train_d, models, splitter)
        else:
            results_search = perform_train_validation(df_train_, models, splitter)
 
        opt_models = {}
        for model, result in results_search.items():
            opt_models[model] = result[0]
    
        if DOWN_SAMPLE_TEST:
            df_train_d = df_train_.sample(frac = DOWN_SAMPLE_TEST_PERC, 
                                             random_state=0)
            results = perform_train_test(df_train_d, df_test, opt_models)  
        else:
            results = perform_train_test(df_train_, df_test, opt_models)  
           
        store_results(results, output_path_case)


def compute_transfer_learning(df_train, df_test, output_path):
    labels = df_test["Label"].unique()
    attacks = [l for l in labels if l != "Benign"]

    for attack in attacks:
        print("Attack " + attack)
        output_path_attack = go_or_create_folder(output_path, attack)
        df_test_ = rename_and_select_labels(df_test, {"Malicious": [attack]},
                                            ["Benign", "Malicious"], output_path_attack,
                                            "test_labels_info")
        select_train_labels(df_train, df_test_, "all", output_path_attack)
    if len(attacks) > 1:
        output_path_m = go_or_create_folder(output_path, "Malicious")
        df_test_ = rename_and_select_labels(df_test, {"Malicious": attacks},
                                            ["Benign", "Malicious"], output_path_m,
                                            "test_labels_info")
        select_train_labels(df_train, df_test_, None, output_path_m)

def main_clf_sl(experiment, version, protocols, rs):
    data_path = get_data_folder(experiment, "BRO", version) + "Train-Test " + str(rs) +"/"
    output_path = get_results_folder(experiment, "BRO", version, "Supervised")
    output_path = go_or_create_folder(output_path, "Train-Test " + str(rs))
    output_path = go_or_create_folder(output_path, EXPERIMENT)

    for protocol in protocols:
        for file_path in glob.glob(data_path + protocol + "_train.csv", recursive=True):
            print("---" + experiment + "--" + version + "--" + protocol.upper() + "----")
            df_train = read_preprocessed(file_path)
            df_test = read_preprocessed(file_path.replace("_train", "_test"))
            labels_check(df_train, df_test)
            output_path_protocol = go_or_create_folder(output_path, protocol)
            compute_transfer_learning(df_train, df_test, output_path_protocol)


if __name__ == "__main__":
    APP = Application(master=tk.Tk(), v_setting=1)
    APP.mainloop()
    for exp in APP.selected_values["Experiments"]:
        for vers in APP.selected_values["Version"]:
            for rs in RS:
                main_clf_sl(exp, vers, APP.selected_values["Files"], rs)


# =============================================================================
# Experiment 2
# =============================================================================
# def main_clf_sl_(version, protocols):
#     train_data_path = get_data_folder("CIC-IDS-2017", "BRO", version)
#     test_data_path = get_data_folder("CIC-IDS-2018", "BRO", version)
#     output_path = get_results_folder("CIC-IDS-2017_CIC-IDS-2018", "BRO", version,
#                                       "Supervised") + "Paper/"
#     for protocol in protocols:
#         try:
#             df_train = read_preprocessed(train_data_path + protocol + ".csv")
#             df_test = read_preprocessed(test_data_path + protocol + ".csv")
#         except:
#             continue
#         output_path_protocol = go_or_create_folder(output_path, protocol)
#         compute_transfer_learning(df_train, df_test, output_path_protocol)


# if __name__ == "__main__":
#     APP = Application(master=tk.Tk(), v_setting=1)
#     APP.mainloop()
#     for vers in APP.selected_values["Version"]:
#         main_clf_sl_(vers, APP.selected_values["Files"])
