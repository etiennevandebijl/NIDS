import glob
import warnings
from itertools import chain, combinations

from project_paths import get_data_folder, get_results_folder
from BRO.utils import read_preprocessed
from ML.utils import rename_and_select_labels, create_output_path
from ML.Supervised.fit_model import perform_train_test_search_opt_params
from ML.Supervised.output import store_results
from ML.Supervised.models import models

from application import Application, tk

warnings.filterwarnings("ignore")

def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def main_clf_sl_(experiment, version, protocols):
    data_path = get_data_folder(experiment, "BRO", version) + "Train-Test 0/"
    output_path = get_results_folder(experiment, "BRO", version, "Supervised") + "Train-Test 0/DDoS/"
    
    for protocol in protocols:
        print("---" + experiment + "--2_Preprocessed_DDoS--" + protocol.upper() + "----")
        for file_path in glob.glob(data_path + protocol + "_train.csv", recursive=True):

            df_train = read_preprocessed(file_path)
            df_test  = read_preprocessed(file_path.replace("train", "test"))

            labels = df_train["Label"].unique().tolist()
            attacks = [l for l in labels if l != "Benign"]
        
            ps = list(powerset(attacks))

            for train_case in ps:
                if len(train_case) > 0:
                    train_attacks = list(train_case)

                    folder_name = [a.replace("DDoS - ","").replace("DoS - ","").replace("Botnet Ares","Botnet_Ares") for a in train_attacks]
                    folder_name = ' '.join(sorted(folder_name))

                    output_path_ = create_output_path(output_path, protocol, folder_name)

                    df_train_ = rename_and_select_labels(df_train, {"Malicious": train_attacks},
                                                         ["Benign","Malicious"], output_path_,
                                                         "train_labels")
                    df_test_  = rename_and_select_labels(df_test, {"Malicious" :attacks},
                                                         ["Benign","Malicious"], output_path_, 
                                                         "test_labels")
    
                    results = perform_train_test_search_opt_params(df_train_, df_test_, models)
                    store_results(results, output_path_)

if __name__ == "__main__":
    APP = Application(master=tk.Tk(), v_setting=1)
    APP.mainloop()
    for exp in APP.selected_values["Experiments"]:
        for vers in APP.selected_values["Version"]:
            main_clf_sl_(exp, vers, APP.selected_values["Files"])

    



