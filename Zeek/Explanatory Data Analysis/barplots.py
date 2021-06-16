#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Barplots features of benign traffic."""

__author__ = "Etienne van de Bijl"
__copyright__ = "Copyright 2021, CWI"
__license__ = "GPL"
__email__ = "evdb@cwi.nl"
__status__ = "Production"

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from application import Application, tk
from project_paths import PROJECT_PATH, go_or_create_folder, get_data_folder
from Zeek.utils import read_preprocessed
sns.set(font_scale=1.2)

TAGS = ["local_", "method_", "_mime_types_", "xx_code", "proto_", "rcode_",
        "qclass_", "qtype_", "last_alert_", "next_protocol_", "service_"]


def plot_bar(dataset, protocol, title, output_path):
    """Make barplot of feature."""
    output_path_p = go_or_create_folder(output_path, protocol)
    dataset.plot(kind="bar", figsize=(10, 7))
    plt.title(protocol.upper() + " binary features")
    plt.xlabel("Feature")
    plt.xticks(rotation=80)
    plt.ylabel("Percentage")
    plt.tight_layout()
    plt.savefig(output_path_p + protocol + "-benign-" + title + ".png")
    plt.close()


def bin_plot(experiments, version, protocols):
    """
    Plot binary features.

    Parameters
    ----------
    experiments : string
        Experiment name.
    version : string
        Version to plot.
    protocols : list of strings
        List of protocols.

    Returns
    -------
    None.

    """
    output_path = PROJECT_PATH + "Results/EDA/BRO/" + version + "/"

    for protocol in protocols:
        stats = {}
        for exp in experiments:
            print("---" + exp + "---" + protocol + "---")
            path = get_data_folder(exp, "BRO", version) + protocol + ".csv"
            try:
                dataset = read_preprocessed(path)
                dataset = dataset[dataset["Label"] == "Benign"]
                dataset = dataset.select_dtypes(include=['bool'])
                stats[exp] = dataset.mean()
            except FileNotFoundError:
                print("File-Not-Found")

        if len(stats) > 0:
            dataset = pd.DataFrame(stats).fillna(0) * 100
            dataset = dataset[(dataset.T != 0).any()]

            for tag in TAGS:
                df_tag = dataset.loc[dataset.index.str.contains(tag), :]
                if df_tag.shape[0] > 0:
                    plot_bar(df_tag, protocol, tag, output_path)
                dataset = dataset.loc[~dataset.index.str.contains(tag)]
            if dataset.shape[0] > 0:
                plot_bar(dataset, protocol, "other", output_path)


if __name__ == "__main__":
    APP = Application(master=tk.Tk(), v_setting=1)
    APP.mainloop()
    for vers in APP.selected_values["Version"]:
        bin_plot(APP.selected_values["Experiments"], vers,
                 APP.selected_values["Files"])
