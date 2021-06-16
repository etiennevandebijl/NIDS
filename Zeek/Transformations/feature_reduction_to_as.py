#!/usr/bin/env python

"""Module extracts features to a single anomaly score."""

__author__ = "Etienne van de Bijl"
__copyright__ = "Copyright 2021, CWI"
__license__ = "GPL"
__email__ = "evdb@cwi.nl"
__status__ = "Production"


import glob
import numpy as np
from tqdm import tqdm

from project_paths import get_data_folder
from ML.Unsupervised.models import models
from Zeek.utils import read_preprocessed, format_ML, statistics_dataset
from application import Application, tk

COLS = ["uid", "ts", "ts_", "id.orig_h", "id.orig_p", "id.resp_h", "id.resp_p",
        "local_orig", "local_resp", "Label"]


def main_feature_reduction(experiment, protocols):
    """Reduce X to only one anomaly score using unsupervised learning alg."""
    data_path = get_data_folder(experiment, "BRO", "2_Preprocessed")
    output_path = get_data_folder(experiment, "BRO", "4_Feature_Reduction")

    for protocol in protocols:
        print("---" + experiment + "--2_Preprocessed--" + protocol.upper() + "----")
        for file_path in glob.glob(data_path + "/" + protocol + ".csv",
                                   recursive=True):
            df = read_preprocessed(file_path)

            df = df.loc[:, (df != 0).any(axis=0)]
            df = df.sample(frac=1, random_state=0).reset_index(drop=True)

            X, _, _, _ = format_ML(df)

            df = df[[c for c in df.columns if c in COLS]]

            for model, clf in tqdm(models.items()):
                clf.fit(X)
                y_pred_score = clf.decision_function(X)
                if "IForest" in model:
                    df[model] = [y + 0.5 for y in y_pred_score]
                else:
                    df[model] = np.log(y_pred_score)

        df.to_csv(output_path + protocol + ".csv", index=False)
        statistics_dataset(df, output_path, protocol)


if __name__ == "__main__":
    APP = Application(master=tk.Tk(), v_setting="2_Preprocessed")
    APP.mainloop()
    for exp in APP.selected_values["Experiments"]:
        main_feature_reduction(exp, APP.selected_values["Files"])
