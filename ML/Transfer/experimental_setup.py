import glob
import warnings
from itertools import chain, combinations

from project_paths import get_data_folder, get_results_folder, go_or_create_folder
from Zeek.utils import read_preprocessed
from ML.Supervised.fit_model import perform_train_test_search_opt_params
from ML.Supervised.output import store_results
from ML.utils import rename_and_select_labels
from ML.Supervised.models import models

from application import Application, tk
#Convenience as the CIC-IDS-2017 attack is the same as the 2018
warnings.filterwarnings("ignore")

NAMES = {"DoS - Hulk": "Hulk",
         "DDoS - HOIC": "HOIC",
         "DDoS - LOIC": "LOIC",
         "DDoS - LOIC - HTTP": "HLOIC", 
         "DDoS - LOIC - UDP": "ULOIC",             
         "DoS - SlowHTTPTest": "Test",
         "DoS - GoldenEye": "Eye",
         "DDoS - Botnet": "Bot",
         "DoS - Slowloris": "Slow"}

def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

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
    attacks = [l for l in labels if (l != "Benign")]
    if test_attack != None:
        attacks = [l for l in attacks if (l != test_attack)]
    ps = list(powerset(attacks))
        
    for train_case in ps:
        if len(train_case) == 1:
            folder_name = create_foldername(train_case)
            print(folder_name)
            output_path_case = go_or_create_folder(output_path, folder_name)
            df_train_ = rename_and_select_labels(df_train, {"Malicious": train_case}, 
                                            ["Benign", "Malicious"], output_path_case, 
                                            "train_labels_info")
            results = perform_train_test_search_opt_params(df_train_, df_test, models)
            store_results(results, output_path_case)
    

def compute_transfer_learning(df_train, df_test, output_path):
    labels = df_test["Label"].unique()
    attacks = [l for l in labels if l != "Benign"]
    # attacks = [l for l in attacks if not "Slow" in l]
    
    for attack in attacks:
        print("Attack " + attack)
        output_path_attack = go_or_create_folder(output_path, attack)
        df_test_ = rename_and_select_labels(df_test, {"Malicious": [attack]}, 
                                            ["Benign", "Malicious"], output_path_attack, 
                                            "test_labels_info")
        select_train_labels(df_train, df_test_, "all", output_path_attack)
    # if len(attacks) > 1:
    #     output_path_m = go_or_create_folder(output_path, "Malicious")
    #     df_test_ = rename_and_select_labels(df_test, {"Malicious": attacks}, 
    #                                         ["Benign", "Malicious"], output_path_m, 
    #                                         "test_labels_info")
    #     select_train_labels(df_train, df_test_, None, output_path_m)

def main_clf_sl(experiment, version, protocols):
    data_path = get_data_folder(experiment, "BRO", version) + "Train-Test 2/"
    output_path = get_results_folder(experiment, "BRO", version, "Supervised") + \
                                     "Train-Test 2/Paper/"
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
            main_clf_sl(exp, vers, APP.selected_values["Files"])
