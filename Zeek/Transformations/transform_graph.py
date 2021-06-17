#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module used to transform anomaly scores to a dynamic graph dataset."""

__author__ = "Etienne van de Bijl"
__copyright__ = "Copyright 2021, CWI"
__license__ = "GPL"
__email__ = "evdb@cwi.nl"
__status__ = "Production"

import glob
from tqdm import tqdm
import pandas as pd

from project_paths import get_data_folder
from Zeek.utils import read_preprocessed, print_progress
from application import Application, tk
from ML.Unsupervised.models import models

MODELS = list(models.keys())
COLS = ["Source", "Target", "ts", "Weight", "Label"] + MODELS

# Parameters
FREQ = "60min"


def time_iterator(dataset):
    """Iterate over time to get edgeinfo per timeunit.

    Function iterates over time.

    Parameters
    ----------
    dataset : pandas dataframe

    Returns
    -------
    dataset_new : pandas dataframe

    """
    t_start = dataset["ts"].dt.round("min").min()
    t_end = dataset["ts"].dt.round("min").max()
    time_epochs = pd.date_range(t_start, t_end, freq=FREQ)

    results = []
    for i in tqdm(range(len(time_epochs)-1)):
        t_i = time_epochs[i]
        t_j = time_epochs[i+1]

        if "ts_" in dataset.columns:
            dataset_t_i = dataset[((dataset["ts_"] > t_i) &
                                   (dataset["ts"] <= t_j))]
        else:
            dataset_t_i = dataset[((dataset["ts"] > t_i) &
                                   (dataset["ts"] <= t_j))]

        if dataset_t_i.shape[0] > 0:
            grouped_by_edge = dataset_t_i.groupby(['id.orig_h', 'id.resp_h'])
            for edge, group in grouped_by_edge:
                lbl = group[group["Label"] != "Benign"].shape[0] > 0
                info = list(edge) + [t_j, group.shape[0], lbl] + \
                    group[MODELS].max().values.tolist()
                results.append(info)
    return pd.DataFrame(results, columns=COLS)


def connection_to_graph(experiment, protocols):
    """Map feature info to anomaly scores using unsupervised algortihms.

    Anomaly scores to graph data.

    Parameters
    ----------
    experiment : string
    protocols : list of strings.

    Returns
    -------
    None.

    """
    data_path = get_data_folder(experiment, "BRO", "4_Feature_Reduction")
    output_path = get_data_folder(experiment, "BRO", "5_Graph")

    for protocol in protocols:
        print_progress(experiment, "4_Feature_Reduction", protocol.upper())
        for file_path in glob.glob(data_path + "/" + protocol + ".csv",
                                   recursive=True):
            dataset = read_preprocessed(file_path)

            pd_list = []
            for _, group in dataset.groupby([dataset["ts"].dt.date]):
                df_day = time_iterator(group)
                pd_list.append(df_day)
            pd.concat(pd_list).to_csv(output_path + protocol +
                                      "-edges-" + FREQ + ".csv", index=False)


if __name__ == "__main__":
    APP = Application(master=tk.Tk(), v_setting="4_Feature_Reduction")
    APP.mainloop()
    for exp in APP.selected_values["Experiments"]:
        connection_to_graph(exp, APP.selected_values["Files"])
