#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module plots the numerical data in boxplots."""
__author__ = "Etienne van de Bijl"
__copyright__ = "Copyright 2021, CWI"
__license__ = "GPL"
__email__ = "evdb@cwi.nl"
__status__ = "Production"

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from project_paths import PROJECT_PATH, go_or_create_folder, get_data_folder
from Zeek.utils import read_preprocessed, print_progress
from application import Application, tk

sns.set(font_scale=1.2)


def plot_box(dataset, protocol, label, output_path):
    """Plot the boxplots for each feature."""
    datasets = dataset["Experiment"].unique()
    dataset = dataset.loc[:, (dataset != 0).any(axis=0)] #NEW REGEL

    output_path_ = go_or_create_folder(output_path, label)    
    
    for feature in dataset.columns:
        if feature != "Experiment" and feature != "Label":

            plt.figure(figsize=(10, 6))
            sns.boxplot(x="Experiment", y=feature, data=dataset)
            plt.title(label + " comparison " + feature + " vs datasets")
            plt.xticks(rotation=60)
            plt.tight_layout()
            plt.savefig(output_path_ +'-'.join(sorted(datasets)) + "-" + \
                        protocol.upper() + "-" + label + "-" + feature.upper() + ".png")
            plt.show()
            plt.close()


def boxplots(experiments, version, protocol):
    """Create boxplots of numerical data.

    This function plots the numerical data in boxplots.

    Parameters
    ----------
    experiments : string
        experiments
    version : string
        version
    protocols : list of strings
        protocols
    """
    output_path = PROJECT_PATH + "Results/EDA/BRO/" + version + "/"
    output_path = go_or_create_folder(output_path, protocol)
    output_path = go_or_create_folder(output_path, '-'.join(sorted(experiments)))
    
    pd_list = []
    for exp in experiments:
        try:
            print_progress(exp, version, protocol.upper())
            path = get_data_folder(exp, "BRO", version) + protocol + ".csv"
            dataset = read_preprocessed(path)
            for label, group in dataset.groupby("Label"):
                dataset = group.select_dtypes(include=['int','float'])
                dataset.loc[:,"Experiment"] = exp
                dataset.loc[:,"Label"] = label                
                pd_list.append(dataset)
        except FileNotFoundError:
            print("File not found.")
    
    if len(pd_list) > 0:
        df = pd.concat(pd_list).fillna(0.0)
    
        for label, group in df.groupby("Label"):
            if label == "Benign":
                plot_box(group, protocol, label, output_path)


if __name__ == "__main__":
    APP = Application(master=tk.Tk(), v_setting=1)
    APP.mainloop()
    for vers in APP.selected_values["Version"]:
        for protocol in APP.selected_values["Files"]:
            boxplots(APP.selected_values["Experiments"], vers, protocol)
