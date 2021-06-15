import os
import glob
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from project_paths import get_results_folder
from application import Application, tk

def plot_fi(fi_dict, experiment, protocol, folder_path):
    df_fi = pd.concat(fi_dict)
    for model in df_fi.columns:
        df_pvt = df_fi.reset_index().pivot(index="Feature", columns="level_0")[model]

        plt.figure(figsize=(20, 15))
        chart = sns.heatmap(df_pvt, cmap="Blues")
        chart.set_xticklabels(chart.get_xticklabels(), rotation=70)

        plt.xlabel("Label")
        plt.ylabel("Feature")
        plt.title(experiment + " Feature Importance Binary Classification")

        plt.tight_layout()
        plt.savefig(folder_path + protocol + "/" + model + "-fi-heatmap.png")
        plt.close()

def interpret_fi(experiment, version, protocols):
    folder_path = get_results_folder(experiment, "BRO", version, "Supervised") + \
                                     "Train-Test 0/Holdout/Selection/"

    for protocol in protocols:
        print("---" + experiment + "--" + version + "--" + protocol.upper() + "----")
        fi_dict = {}
        for file_path in glob.glob(folder_path + protocol + "/*/feature_importance.csv",
                                   recursive=True):
            case = file_path.split(os.sep)[-2]
            if ("Benign" in case) and (not "Malicious" in case):
                attack = case.replace("Benign vs ", "")
                df_fi = pd.read_csv(file_path, sep=";", index_col=0, decimal=",").fillna(0)
                fi_dict[attack] = df_fi.rename_axis('Feature')

        if len(fi_dict) > 0:
            plot_fi(fi_dict, experiment, protocol, folder_path)

if __name__ == "__main__":
    APP = Application(master=tk.Tk(), v_setting=1)
    APP.mainloop()
    for exp in APP.selected_values["Experiments"]:
        for vers in APP.selected_values["Version"]:
            interpret_fi(exp, vers, APP.selected_values["Files"])
