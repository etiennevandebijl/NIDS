#!/usr/bin/env python

"""
This module makes figures of the class-time of the labels.
"""

# Author: Etienne van de Bijl 2020

import glob
import seaborn as sns
import matplotlib.pyplot as plt

from project_paths import get_data_folder, get_results_folder, go_or_create_folder
from Zeek.utils import read_preprocessed
from application import Application, tk

sns.set(font_scale=1.2)

def class_time(dataset, experiment, output_folder, file_name):
    """
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
                           figsize=(12, 3 + 0.1 * len(dataset["Label"].unique())))
    sns.stripplot(ax=axis, x="ts", y="Label", data=dataset)
    plt.close(2)

    axis.set_title("Attack Scheme " + experiment + ' ' + file_name.upper())
    axis.set_xlim(min(dataset["ts"]), max(dataset["ts"]))
    axis.set_xlabel("Time")
    axis.set_ylabel("Label")

    plt.tight_layout()
    plt.savefig(output_folder + file_name + "-class-time.png")
    plt.close()

def catplot(experiment, version, protocols):
    """
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
    data_path = get_data_folder(experiment, "BRO", version)
    output_folder = get_results_folder(experiment, "BRO", version, "EDA") + "class-time/"

    for protocol in protocols:
        print("---" + experiment + "--" + version + "--" + protocol.upper() + "----")
        for file_path in glob.glob(data_path + "/" + protocol + ".csv", recursive=True):

            dataset = read_preprocessed(file_path)
            class_time(dataset, experiment, output_folder, protocol)

            grouped_dates = dataset.groupby(dataset["ts"].dt.date)
            for date, df_date in grouped_dates:
                if len(df_date["Label"].unique()) > 1:
                    output_folder_day = go_or_create_folder(output_folder, str(date))
                    class_time(df_date, experiment, output_folder_day, protocol)

if __name__ == "__main__":
    APP = Application(master=tk.Tk(), v_setting=1)
    APP.mainloop()
    for exp in APP.selected_values["Experiments"]:
        for vers in APP.selected_values["Version"]:
            catplot(exp, vers, APP.selected_values["Files"])
        
