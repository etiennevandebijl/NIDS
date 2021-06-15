# /usr/bin/env python

"""
In this function we only select DDoS Attacks.
"""

# Author: Etienne van de Bijl
# License: BSD 3 clause

import glob
import pandas as pd

from project_paths import get_data_folder
from Zeek.utils import read_preprocessed, statistics_dataset
from application import Application, tk

def equalize_ddos(dataset, ddos):
    """
    This function downsamples the DDoS attacks.

    Parameters
    ----------
    dataset : pandas dataframe
        log file of bro.
    ddos : list of strings
        list of the attacks in the bro file.

    Returns
    -------
    dataset : pandas dataframe
        Downsampled towards an equal number of instances.

    """
    dataset_b = dataset[dataset["Label"] == "Benign"]
    dataset_m = dataset[dataset["Label"] != "Benign"]
    least_instances = dataset_m["Label"].value_counts().min()

    pd_list = [dataset_b]
    for attack in ddos:
        df_attack = dataset_m[dataset_m["Label"] == attack].sample(least_instances)
        pd_list.append(df_attack)
    dataset = pd.concat(pd_list)
    return dataset

def select_ddos(experiment, version, protocols, equalize=True):
    """
    In this function we only select DDoS attacks.

    Parameters
    ----------
    experiment : string
    version : TYPE
    protocols : list of strings
    equalize : boolean
        We can downsampled the DDoS attacks towards the lowest number.

    Returns
    -------
    None.

    """
    data_path = get_data_folder(experiment, "BRO", version)
    output_path = get_data_folder(experiment, "BRO", "2_Preprocessed_DDoS")

    for protocol in protocols:
        for file_path in glob.glob(data_path + "/" + protocol + ".csv", recursive=True):
            print("---" + experiment + "--" + version + "--" + protocol.upper() + "----")
            dataset = read_preprocessed(file_path)

            ddos = [a for a in dataset["Label"].unique() if ("DoS" in a or "DDoS" in a or "Bot" in a)]
            if len(ddos) == 0:
                continue
            dataset = dataset[dataset["Label"].isin(ddos + ["Benign"])]

            #Is this necessary?
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
