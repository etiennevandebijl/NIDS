import warnings

from project_paths import get_data_folder, get_results_folder, go_or_create_folder
from Zeek.utils import read_preprocessed

from application import Application, tk
warnings.filterwarnings("ignore")

from ML.Transfer.experimental_setup import compute_transfer_learning

def main_clf_sl(version, protocols):
    train_data_path = get_data_folder("CIC-IDS-2017", "BRO", version)
    test_data_path = get_data_folder("CIC-IDS-2018", "BRO", version) 
    output_path = get_results_folder("CIC-IDS-2017_CIC-IDS-2018", "BRO", version, "Supervised") + \
                                     "Paper/"
    for protocol in protocols:
        try:
            df_train = read_preprocessed(train_data_path + protocol + ".csv")
            df_test = read_preprocessed(test_data_path + protocol + ".csv")
        except:
            continue
        output_path_protocol = go_or_create_folder(output_path, protocol)
        compute_transfer_learning(df_train, df_test, output_path_protocol)


if __name__ == "__main__":
    APP = Application(master=tk.Tk(), v_setting=1)
    APP.mainloop()
    for vers in APP.selected_values["Version"]:
        main_clf_sl(vers, APP.selected_values["Files"])
