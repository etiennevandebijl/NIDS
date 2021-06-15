#!/usr/bin/env python

"""
This module creates correlation plots
"""

# Author: Etienne van de Bijl 2020
# License: BSD 3 clause

import glob
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from project_paths import get_data_folder, get_results_folder, go_or_create_folder
from Zeek.utils import format_ML, read_preprocessed
from application import Application, tk

sns.set(font_scale=1.5)

def cor_plot(experiment, version, protocols):
    """
    Create correlation plot of the numeric features.

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
    output_folder = get_results_folder(experiment, "BRO", version, "EDA")+"correlations/"

    for protocol in protocols:
        print("---"+experiment+"--"+version+"--"+protocol.upper()+"----")
        for file_path in glob.glob(data_path+"/"+protocol+".csv", recursive=True):

            dataset = read_preprocessed(file_path)

            dataset = dataset.select_dtypes(exclude=['bool'])
            dataset = dataset.loc[:, (dataset != 0).any(axis=0)]

            x_data, _, feature_names, _ = format_ML(dataset)

            for method in ["spearman", "kendall", "pearson"]:
                output_path = go_or_create_folder(output_folder, method)
                corr = pd.DataFrame(x_data, columns=feature_names).corr(method=method)

                plt.figure(figsize=(20, 15))
                sns.heatmap(corr)

                plt.title(experiment+" "+protocol.upper()+" "+method+" correlation")
                plt.tight_layout()
                plt.savefig(output_path + protocol + "-correlation.png")
                plt.close()

if __name__ == "__main__":
    APP = Application(master=tk.Tk(), v_setting=1)
    APP.mainloop()
    for exp in APP.selected_values["Experiments"]:
        for vers in APP.selected_values["Version"]:
            cor_plot(exp, vers, APP.selected_values["Files"])
            
