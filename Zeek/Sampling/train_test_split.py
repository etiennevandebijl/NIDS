# /usr/bin/env python

"""
This module splits data in train/test dataset.
"""

# Author: Etienne van de Bijl
# License: BSD 3 clause

import glob
from sklearn.model_selection import train_test_split

from project_paths import get_data_folder, go_or_create_folder
from Zeek.utils import read_preprocessed, statistics_dataset
from application import Application, tk

TRAIN_RATIO = 0.8
MINIMUM_ROWS = 1000
RS = 0


def store_df(dataset, protocol, output_path):
    """
    Store file.

    Parameters
    ----------
    dataset : pandas dataframe
        The train/test dataset.
    protocol : string
        Protocol of interest.
    output_path : string
        Output path.

    """
    dataset.to_csv(output_path + protocol + ".csv", index=False)
    statistics_dataset(dataset, output_path, protocol)


def train_test_split_ml(experiment, version, protocols):
    """
    Train test split.

    Parameters
    ----------
    experiment : string
    version : string
    protocols : string

    """
    data_path = get_data_folder(experiment, "BRO", version)
    output_path = go_or_create_folder(data_path, 'Train-Test ' + str(RS))

    for protocol in protocols:
        for file_path in glob.glob(data_path + "/" + protocol + ".csv",
                                   recursive=True):
            print("---" + experiment + "--" + version + "--" + protocol.upper() + "----")
            dataset = read_preprocessed(file_path)

            dataset = dataset.loc[:, (dataset != 0).any(axis=0)]

            single_attacks = dataset["Label"].drop_duplicates(keep=False).tolist()
            dataset = dataset[~dataset["Label"].isin(single_attacks)]

            if (dataset.shape[0] > MINIMUM_ROWS and len(dataset["Label"].unique()) > 1):
                df_train, df_test, _, _ = train_test_split(dataset, dataset["Label"],
                                                           stratify=dataset["Label"],
                                                           train_size=TRAIN_RATIO,
                                                           random_state=RS)
                store_df(df_train, protocol + "_train", output_path)
                store_df(df_test, protocol + "_test", output_path)


if __name__ == "__main__":
    APP = Application(master=tk.Tk(), v_setting=1)
    APP.mainloop()
    for exp in APP.selected_values["Experiments"]:
        for vers in APP.selected_values["Version"]:
            train_test_split_ml(exp, vers, APP.selected_values["Files"])
