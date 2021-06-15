#!/usr/bin/env python

"""
This module plots the numerical data in boxplots.
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from project_paths import PROJECT_PATH, go_or_create_folder, get_data_folder
from Zeek.utils import read_preprocessed, format_ML
from application import Application, tk

sns.set(font_scale=1.2)

def plot_box(dataset, protocol, output_path):
    """
    This function plots the boxplots for each feature.
    """
    output_path_p = go_or_create_folder(output_path, protocol)
    for feature in dataset.columns:
        if feature != "Dataset":
            plt.figure(figsize=(10, 6))
            sns.boxplot(x="Dataset", y=feature, data=dataset)
            plt.title("Benign comparison "+ feature + " vs datasets")
            plt.xticks(rotation=60)
            plt.tight_layout()
            plt.savefig(output_path_p + protocol + "-benign-" + feature + ".png")
            plt.close()

def num_plot(experiments, version, protocols):
    """
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

    for protocol in protocols:
        pd_list = []
        for exp in experiments:
            try:
                print("---" + exp + "---" + protocol + "---")
                path = get_data_folder(exp, "BRO", version) + protocol + ".csv"
                dataset = read_preprocessed(path)
                dataset = dataset[dataset["Label"] == "Benign"] #Only normal
                dataset = dataset.select_dtypes(exclude=['bool'])

                x_data, _, feature_names, _ = format_ML(dataset)
                df_new = pd.DataFrame(x_data, columns=feature_names)
                df_new["Dataset"] = exp
                pd_list.append(df_new)
            except FileNotFoundError:
                print("File not found.")
        df_new = pd.concat(pd_list).fillna(0.0)
        df_new = df_new.loc[:, (df_new != 0).any(axis=0)]
        plot_box(df_new, protocol, output_path)

if __name__ == "__main__":
    APP = Application(master=tk.Tk(), v_setting=1)
    APP.mainloop()
    for vers in APP.selected_values["Version"]:
        num_plot(APP.selected_values["Experiments"], vers, APP.selected_values["Files"])
        
