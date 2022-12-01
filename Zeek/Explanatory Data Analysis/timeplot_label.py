#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module makes figures of the class-time of the labels."""

__author__ = "Etienne van de Bijl"
__copyright__ = "Copyright 2021, CWI"
__license__ = "GPL"
__email__ = "evdb@cwi.nl"
__status__ = "Production"

import glob
import seaborn as sns
import matplotlib.pyplot as plt

from project_paths import get_data_folder, get_results_folder, \
    go_or_create_folder
from Zeek.utils import read_preprocessed, print_progress
from application import Application, tk

sns.set(font_scale=1.2)


def class_time(dataset, experiment, output_folder, file_name):
    """Create plot of attacks over time.

    Makes actual figures.

    Parameters
    ----------
    dataset : pandas dataframe
    experiment : string
    output_folder : string
    file_name : string

    Returns
    -------
    None.

    """
    _, axis = plt.subplots(1, 1, sharey=True,
                           figsize=(12, 3 + 0.1 *
                                    len(dataset["Label"].unique())))
    sns.stripplot(ax=axis, x="ts", y="Label", data=dataset)
    plt.close(2)

    axis.set_title("Attack Scheme " + experiment + ' ' + file_name.upper())
    axis.set_xlim(min(dataset["ts"]), max(dataset["ts"]))
    axis.set_xlabel("Time")
    axis.set_ylabel("Label")

    plt.tight_layout()
    plt.savefig(output_folder + file_name + "-class-time.png")
    plt.close()


def timeplot(experiment, version, protocols):
    """Make timeplot of attacks per protocol.

    This function makes a time plot of the classes.

    Parameters
    ----------
    experiment : string
    version : string
    protocols : list of strings

    Returns
    -------
    None.

    """
    data_path = get_data_folder(experiment, "Zeek", version)
    output_folder = get_results_folder(experiment, "Zeek",
                                       version, "EDA") + "class-time/"

    for protocol in protocols:
        print_progress(experiment, version, protocol.upper())
        for file_path in glob.glob(data_path + "/" + protocol + ".csv",
                                   recursive=True):

            dataset = read_preprocessed(file_path)
            class_time(dataset, experiment, output_folder, protocol)

            grouped_dates = dataset.groupby(dataset["ts"].dt.date)
            for date, df_date in grouped_dates:
                if len(df_date["Label"].unique()) > 1:
                    output_folder_day = go_or_create_folder(output_folder,
                                                            str(date))
                    class_time(df_date, experiment,
                               output_folder_day, protocol)


if __name__ == "__main__":
    APP = Application(master=tk.Tk(), v_setting=1)
    APP.mainloop()
    for exp in APP.selected_values["Experiments"]:
        for vers in APP.selected_values["Version"]:
            timeplot(exp, vers, APP.selected_values["Files"])
