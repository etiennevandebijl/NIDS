import glob

from project_paths import get_data_folder, get_results_folder
from Zeek.utils import read_preprocessed
from ML.Unsupervised.models import models
from ML.Unsupervised.fit_model import fit_model
from ML.Unsupervised.output import store_as_and_models, create_figures
from ML.utils import create_output_path, rename_and_select_labels
from application import Application, tk

def compute_and_store_results(dataset, group_labels, select_classes, output_path,
                              protocol, folder, train_benign=False):
    if train_benign:
        folder = folder + " - Train Benign"
    output_path = create_output_path(output_path, protocol, folder)

    df_ = rename_and_select_labels(dataset, group_labels, select_classes, output_path)
    results = fit_model(df_, models, train_benign)
    df_as = store_as_and_models(df_, results, models, output_path)
    create_figures(df_as, output_path)

def main_clf_usl(experiment, version, protocols):
    data_path = get_data_folder(experiment, "BRO", version)
    output_path = get_results_folder(experiment, "BRO", version, "Unsupervised")

    for protocol in protocols:
        print("---" + experiment + "--" + version + "--" + protocol.upper() + "----")
        for file_path in glob.glob(data_path + protocol + ".csv", recursive=True):
            dataset = read_preprocessed(file_path)
            dataset = dataset.loc[:, (dataset != 0).any(axis=0)]

            labels = dataset["Label"].unique().tolist()
            attacks = [l for l in labels if l != "Benign"]

            #for attack in attacks:
            #    if "DDoS" in attack:
            #        compute_and_store_results(dataset, {}, ["Benign", attack], output_path,
            #                              protocol, "Benign vs " + attack)
            if len(attacks) > 1: 
                compute_and_store_results(dataset, {}, labels, output_path, protocol,
                                          "Benign vs Malicious")

if __name__ == "__main__":
    APP = Application(master=tk.Tk(), v_setting=5)
    APP.mainloop()
    for exp in APP.selected_values["Experiments"]:
        for vers in APP.selected_values["Version"]:
            main_clf_usl(exp, vers, APP.selected_values["Files"])
