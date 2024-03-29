#!/usr/bin/env python

"""Module splitting data in train and test sets."""

__author__ = "Etienne van de Bijl"
__copyright__ = "Copyright 2021, CWI"
__license__ = "GPL"
__email__ = "evdb@cwi.nl"
__status__ = "Production"

import glob
from sklearn.model_selection import train_test_split

from project_paths import get_data_folder, go_or_create_folder
from Zeek.utils import read_preprocessed, statistics_dataset, print_progress
from application import Application, tk

TRAIN_RATIO = 0.8
MINIMUM_ROWS = 1000
RS = 9


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
    """Split data in train and test.

    Train test split.

    Parameters
    ----------
    experiment : string
    version : string
    protocols : string

    """
    data_path = get_data_folder(experiment, "Zeek", version)
    output_path = go_or_create_folder(data_path, 'Train-Test ' + str(RS))

    for protocol in protocols:
        for file_path in glob.glob(data_path + "/" + protocol + ".csv",
                                   recursive=True):
            print_progress(experiment, version, protocol.upper())
            data = read_preprocessed(file_path)

            data = data.loc[:, (data != 0).any(axis=0)]

            single_attacks = data["Label"].drop_duplicates(keep=False).tolist()
            data = data[~data["Label"].isin(single_attacks)]

            if (data.shape[0] > MINIMUM_ROWS and
                    len(data["Label"].unique()) > 1):
                train, test, _, _ = train_test_split(data, data["Label"],
                                                     stratify=data["Label"],
                                                     train_size=TRAIN_RATIO,
                                                     random_state=RS)
                store_df(train, protocol + "_train", output_path)
                store_df(test, protocol + "_test", output_path)


if __name__ == "__main__":
    APP = Application(master=tk.Tk(), v_setting=1)
    APP.mainloop()
    for exp in APP.selected_values["Experiments"]:
        for vers in APP.selected_values["Version"]:
            train_test_split_ml(exp, vers, APP.selected_values["Files"])
