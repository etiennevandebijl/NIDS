#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module to select only DDoS/DoS attacks."""

__author__ = "Etienne van de Bijl"
__copyright__ = "Copyright 2021, CWI"
__license__ = "GPL"
__email__ = "evdb@cwi.nl"
__status__ = "Production"

import glob
import pandas as pd

from project_paths import get_data_folder
from Zeek.utils import read_preprocessed, statistics_dataset, print_progress
from application import Application, tk


def equalize_ddos(dataset, ddos):
    """Equalizing the DDoS/DoS Samples.

    This function downsamples DoS/DDoS attacks.

    Parameters
    ----------
    dataset : pandas dataframe
        log file of Zeek.
    ddos : list of strings
        list of the attacks in the Zeek file.

    Returns
    -------
    dataset : pandas dataframe
        Downsampled towards an equal number of instances.

    """
    dataset_b = dataset[dataset["Label"] == "Benign"]
    dataset_m = dataset[dataset["Label"] != "Benign"]
    lower_b = dataset_m["Label"].value_counts().min()

    pd_list = [dataset_b]
    for attack in ddos:
        df_attack = dataset_m[dataset_m["Label"] == attack].sample(lower_b)
        pd_list.append(df_attack)
    dataset = pd.concat(pd_list)
    return dataset


def select_ddos(experiment, version, protocols, equalize=True):
    """Select only DDoS/DoS malicious traffic + Benign.

    In this function we only select DDoS attacks.

    Parameters
    ----------
    experiment : string
    version : string
    protocols : list of strings
    equalize : boolean
        We can downsampled the DDoS attacks towards the lowest number.

    Returns
    -------
    None.

    """
    data_path = get_data_folder(experiment, "Zeek", version)
    output_path = get_data_folder(experiment, "Zeek", "2_Preprocessed_DDoS")

    for protocol in protocols:
        for file_path in glob.glob(data_path + "/" + protocol + ".csv",
                                   recursive=True):
            print_progress(experiment, version, protocol.upper())
            dataset = read_preprocessed(file_path)

            ddos = [a for a in dataset["Label"].unique() if ("DoS" in a or
                                                             "DDoS" in a or
                                                             "Bot" in a)]
            if len(ddos) == 0:
                continue
            dataset = dataset[dataset["Label"].isin(ddos + ["Benign"])]

            # Is this necessary?
            if equalize:
                dataset = equalize_ddos(dataset, ddos)

            dataset.to_csv(output_path + protocol + ".csv", index=False)
            statistics_dataset(dataset, output_path, protocol)


if __name__ == "__main__":
    APP = Application(master=tk.Tk(), v_setting=4)
    APP.mainloop()
    for exp in APP.selected_values["Experiments"]:
        for vers in APP.selected_values["Version"]:
            select_ddos(exp, vers, APP.selected_values["Files"], False)
