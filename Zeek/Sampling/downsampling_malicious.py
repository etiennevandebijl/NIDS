# /usr/bin/env python

"""
This module downsamples the data.
"""

# Author: Etienne van de Bijl
# License: BSD 3 clause

import glob
import numpy as np
import pandas as pd

from project_paths import get_data_folder
from Zeek.utils import read_preprocessed, statistics_dataset
from application import Application, tk

MINIMUM_ROWS = 1000
PREF_INTRUSION_RATIO = 0.05
BOUND_INTRUSION_RATIO = 0.1


def downsample_malicious(dataset):
    """Downsampling malicious instances.

    This function downsamples the malicious instances towards an intrusion
    ratio equaling the preferred intrusion ratio.

    Parameters
    ----------
    dataset : TYPE
        DESCRIPTION.

    Returns
    -------
    dataset : TYPE
        DESCRIPTION.

    """
    dataset_b = dataset[dataset["Label"] == "Benign"]
    dataset_m = dataset[dataset["Label"] != "Benign"]

    scaler = PREF_INTRUSION_RATIO / (1 - PREF_INTRUSION_RATIO)
    positives_new = int(scaler * dataset_b.shape[0])

    cond = True
    i = 0
    while cond:
        dataset_m_new = dataset_m.sample(positives_new, random_state=i)
        cond = len(dataset_m["Label"].unique()) != len(dataset_m_new["Label"].unique())
        i = i + 1

    dataset = pd.concat([dataset_b, dataset_m_new])
    dataset = dataset.sort_values(by=['ts'])
    return dataset


def downsampling(experiment, protocols):
    """
    This function downsamples datasets. If the numnber of instances is below 1000,
    we skip the dataset. When the intrusion ratio is.

    Parameters
    ----------
    experiment : string
    protocols : list of strings
        string.

    Returns
    -------
    None.

    """
    data_path = get_data_folder(experiment, "BRO", "2_Preprocessed")
    output_path = get_data_folder(experiment, "BRO", "3_Downsampled")

    for protocol in protocols:
        print("---" + experiment + "--" + protocol.upper() + "----")
        for file_path in glob.glob(data_path + "/" + protocol + ".csv", recursive=True):
            dataset = read_preprocessed(file_path)

            if dataset.shape[0] < MINIMUM_ROWS:
                continue

            intrusion_ratio = np.sum(dataset["Label"] != "Benign") / dataset.shape[0]

            if intrusion_ratio > BOUND_INTRUSION_RATIO:
                dataset = downsample_malicious(dataset)
                dataset.to_csv(output_path + protocol + ".csv", index=False)
                statistics_dataset(dataset, output_path, protocol)
            else:
                print("---" + experiment + "--" + protocol.upper() + "- Ignore")


if __name__ == "__main__":
    APP = Application(master=tk.Tk(), v_setting="2_Preprocessed")
    APP.mainloop()
    for exp in APP.selected_values["Experiments"]:
        downsampling(exp, APP.selected_values["Files"])
