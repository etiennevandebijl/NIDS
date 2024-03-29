#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module makes figures of the class-distribution of the labels."""

__author__ = "Etienne van de Bijl"
__copyright__ = "Copyright 2021, CWI"
__license__ = "GPL"
__email__ = "evdb@cwi.nl"
__status__ = "Production"

import glob
import seaborn as sns
import matplotlib.pyplot as plt

from project_paths import get_data_folder, get_results_folder
from Zeek.utils import read_preprocessed, print_progress
from application import Application, tk

def class_count_plot(dataset, output_folder, protocol):
    """Do the counting."""
    pvt_table = dataset["Label"].value_counts().reset_index()
    pvt_table["Percentage"] = pvt_table["Label"] * 100 / \
        pvt_table["Label"].sum()

    width = min(max(4 + pvt_table.shape[0] * 0.9, 6), 15)
    plt.figure(figsize=(width, 7))

    sns.set(style="whitegrid", font_scale=1.2)
    figure_sns = sns.barplot(x="index", y="Percentage", data=pvt_table)

    for _, row in pvt_table.iterrows():
        figure_sns.text(row.name, row["Percentage"], row["Label"],
                        color='black', ha="center")

    plt.title(protocol.upper() + " Number of Instances per Label")
    plt.xlabel("Label")
    plt.xticks(rotation=70)
    plt.tight_layout()
    plt.savefig(output_folder + protocol + "-class-distribution.png")
    plt.close()


def class_count(experiment, version, protocols):
    """Count frequency of labels."""
    data_path = get_data_folder(experiment, "Zeek", version)
    output_folder = get_results_folder(experiment, "Zeek", version, "EDA") + \
        "class-distribution/"

    for protocol in protocols:
        print_progress(experiment, version, protocol.upper())
        for file_path in glob.glob(data_path + "/" + protocol + ".csv",
                                   recursive=True):
            dataset = read_preprocessed(file_path)
            class_count_plot(dataset, output_folder, protocol)


if __name__ == "__main__":
    APP = Application(master=tk.Tk(), v_setting=1)
    APP.mainloop()
    for exp in APP.selected_values["Experiments"]:
        for vers in APP.selected_values["Version"]:
            class_count(exp, vers, APP.selected_values["Files"])
