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
from Zeek.utils import read_preprocessed, print_progress
sns.set(font_scale=1.2)

TAGS = ["selected_colslocal_", "method_", "_mime_types_", "xx_code", "proto_", "rcode_",
        "qclass_", "qtype_", "last_alert_", "next_protocol_", "service_"]


def plot_bar(dataset, selected_cols, protocol, label, title, output_path):
    """Make barplot of feature."""
    datasets = dataset["Experiment"]
    output_path_ = go_or_create_folder(output_path, label)
    
    df = dataset[selected_cols].T
    df.columns = datasets
    if df.shape[0] > 0 and df.shape[1] > 0:
        df.plot(kind="bar", figsize=(10, 7))
        plt.title(protocol.upper() + " " + label +  " binary features")
        plt.xlabel("Feature")
        plt.xticks(rotation=80)
        plt.ylabel("Percentage")
        plt.tight_layout()
    
        plt.savefig(output_path_ + '-'.join(sorted(datasets)) + "-" + protocol.upper() + \
                    "-" + label + "-" + title + ".png")
        plt.close()

def group_features(df, label, output_path):
    df = df.loc[:, (df != 0).any(axis=0)]

    for tag in TAGS:
        select_cols = [c for c in df.columns if tag in c]
        plot_bar(df, select_cols, protocol, label, tag, output_path)

    select_cols = [c for c in df.columns if tag not in c and 
                   c != "Experiment" and c != "Label"]
    plot_bar(df, select_cols, protocol, label, "other", output_path)
    

def get_means(df, exp, label):
    df = df[df["Label"] == label].select_dtypes(include=['bool']).mean() * 100
    df["Experiment"] = exp
    df["Label"] = label
    return df
    
def bin_plot(experiments, version, protocol):
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
    output_path = go_or_create_folder(output_path, protocol)
    output_path = go_or_create_folder(output_path, '-'.join(sorted(experiments)))

    pd_list = []
    for exp in experiments:
        path = get_data_folder(exp, "BRO", version) + protocol + ".csv"
        print_progress(exp, version, protocol.upper())
        try:
            dataset = read_preprocessed(path)
            for label in dataset["Label"].unique():
                df = get_means(dataset, exp, label)
                pd_list.append(df)
            dataset.loc[dataset["Label"] != "Benign", 'Label'] = "Malicious"
            df = get_means(dataset, exp, "Malicious")
            pd_list.append(df)
        except FileNotFoundError:
            print("File-Not-Found")
    
    if len(pd_list) > 0:
        df = pd.concat(pd_list, axis=1).T.fillna(0)

        for label, group in df.groupby("Label"):
            group_features(group, label, output_path)


if __name__ == "__main__":
    APP = Application(master=tk.Tk(), v_setting=1)
    APP.mainloop()
    for vers in APP.selected_values["Version"]:
        for protocol in APP.selected_values["Files"]:
            bin_plot(APP.selected_values["Experiments"], vers, protocol)
