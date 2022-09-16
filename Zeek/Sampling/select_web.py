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


def select_webattack(experiment, version, protocols):
    """Select only Web Attacks + Benign.

    In this function we only select Web attacks.

    Parameters
    ----------
    experiment : string
    version : string
    protocols : list of strings

    Returns
    -------
    None.

    """
    data_path = get_data_folder(experiment, "BRO", version)
    output_path = get_data_folder(experiment, "BRO", "2_Preprocessed_Web")

    for protocol in protocols:
        for file_path in glob.glob(data_path + "/" + protocol + ".csv",
                                   recursive=True):
            print_progress(experiment, version, protocol.upper())
            dataset = read_preprocessed(file_path)

            web = [a for a in dataset["Label"].unique() if "Web" in a]
            if len(web) == 0:
                continue
            dataset = dataset[dataset["Label"].isin(web + ["Benign"])]

            dataset.to_csv(output_path + protocol + ".csv", index=False)
            statistics_dataset(dataset, output_path, protocol)


if __name__ == "__main__":
    APP = Application(master=tk.Tk(), v_setting=4)
    APP.mainloop()
    for exp in APP.selected_values["Experiments"]:
        for vers in APP.selected_values["Version"]:
            select_webattack(exp, vers, APP.selected_values["Files"])
