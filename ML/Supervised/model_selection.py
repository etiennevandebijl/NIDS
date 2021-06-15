#!/usr/bin/env python

"""
This module performs the model selection phase.
"""

# Author: Etienne van de Bijl
# License: BSD 3 clause

import glob
import warnings
from sklearn.model_selection import StratifiedShuffleSplit

from project_paths import get_data_folder, get_results_folder
from Zeek.utils import read_preprocessed
from ML.utils import rename_and_select_labels, create_output_path
from ML.Supervised.models import models
from ML.Supervised.fit_model import perform_train_validation
from ML.Supervised.output import store_results

from application import Application, tk

warnings.filterwarnings("ignore")

def compute_and_store_results(dataset, group_labels, select_classes, output_path, protocol, folder):
    """
    Function to compute select labels/ group them and get results.

    Parameters
    ----------
    dataset : pandas dataframe
        DESCRIPTION.
    group_labels : dictionary
        Mapping of multiple attacks to a single new label.
    select_classes : list of strings
        Selected labels.
    output_path : string
    protocol : string
    folder : string
        Folder name describing the case.
    Returns
    -------
    None.

    """
    output_path = create_output_path(output_path, protocol, folder)
    df_ = rename_and_select_labels(dataset, group_labels, select_classes, output_path)

    splitter = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=0)
 
    results = perform_train_validation(df_, models, splitter)
    store_results(results, output_path)

def main_clf_sl(experiment, version, protocols):
    """
    Main function to start model selection.

    Parameters
    ----------
    experiment : string
    version : string
    protocols : list of strings

    Returns
    -------
    None.

    """
    input_path = get_data_folder(experiment, "BRO", version) + "Train-Test 0/"
    output_path = get_results_folder(experiment, "BRO", version, "Supervised") + \
                                     "Train-Test 0/Holdout/Selection/"

    for protocol in protocols:
        print("---" + experiment + "--" + version + "--" + protocol.upper() + "----")
        for file_path in glob.glob(input_path + protocol + "_train.csv", recursive=True):

            dataset = read_preprocessed(file_path)

            labels = dataset["Label"].unique().tolist()
            attacks = [l for l in labels if l != "Benign"]

            for attack in attacks:
            #    if "Botnet" in attack:
                    compute_and_store_results(dataset, {}, ["Benign", attack], output_path,
                                          protocol, "Benign vs " + attack)
            if len(attacks) > 1:
                compute_and_store_results(dataset, {}, labels, output_path, protocol, "Complete")
                compute_and_store_results(dataset, {"Malicious":attacks}, ["Benign", "Malicious"],
                                          output_path, protocol, "Benign vs Malicious")

if __name__ == "__main__":
    APP = Application(master=tk.Tk(), v_setting=5)
    APP.mainloop()
    for exp in APP.selected_values["Experiments"]:
        for vers in APP.selected_values["Version"]:
            main_clf_sl(exp, vers, APP.selected_values["Files"])
