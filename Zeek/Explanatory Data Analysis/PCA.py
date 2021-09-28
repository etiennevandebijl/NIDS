#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 16:22:05 2021

@author: etienne
"""
import seaborn as sns

import matplotlib.pyplot as plt

from application import Application, tk
from project_paths import get_data_folder
from Zeek.utils import read_preprocessed, print_progress, format_ML
import numpy as np

from sklearn import decomposition
from sklearn.manifold import TSNE

def PCA_plot(experiments, version, protocol):
    for exp in experiments:
        path = get_data_folder(exp, "BRO", version) + protocol + ".csv"
        print_progress(exp, version, protocol.upper())
        try:
            dataset = read_preprocessed(path)
            for label, group in dataset.groupby("Label"):
                #dataset = dataset[dataset["Label"] != "Benign"]
                #dataset = dataset[dataset["Label"] != "DoS - Hulk"]
                #dataset = dataset[dataset["Label"] != "DDoS - Botnet"]            
                X, y, _, _ = format_ML(group)
                model = decomposition.PCA(n_components=2)
                #model = TSNE(n_components=2, learning_rate='auto', init='random')
                #X = np.asarray(X, dtype='float64')
                model.fit(X)

                X = model.transform(X)
                X = np.log(X)
                print(model.explained_variance_ratio_)
                plt.figure(figsize = (10, 10))
                sns.scatterplot(x = X[:,0], y = X[:,1], hue = y)
                plt.show()
        except FileNotFoundError:
            print("File-Not-Found")
    

if __name__ == "__main__":
    APP = Application(master=tk.Tk(), v_setting=1)
    APP.mainloop()
    for vers in APP.selected_values["Version"]:
        for protocol in APP.selected_values["Files"]:
            PCA_plot(APP.selected_values["Experiments"], vers, protocol)