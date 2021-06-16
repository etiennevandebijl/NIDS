#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Label connections conn.log and store uid + label in labelling.csv."""

__author__ = "Etienne van de Bijl"
__copyright__ = "Copyright (C) 2021 Etienne van de Bijl"
__license__ = "GPL"
__email__ = "evdb@cwi.nl"
__status__ = "Production"

import glob
import pandas as pd
from tqdm import tqdm

from project_paths import get_data_folder, get_labelling_scheme
from Zeek.Preprocessing.utils import bro_reader

SELECT_COLS = ["uid", "ts", "id.orig_h", "id.orig_p", "id.resp_h", "id.resp_p"]


def identify_attack(log_file, attack, vise_versa=False):
    """Identify attacks.

    Searches for instances in the df which confirm the meta data of the attack.
    Labels these instances with the corresponding attack.

    Parameters
    ----------
    log_file : pandas dataframe
        The BRO conn.log converted file.

    attack : pandas row
        Row of a pandas dataframe describing meta data about an attack.

    vise_versa : boolean
        A indicator whether originator and responder should be swapped.

    Returns
    -------
    log_file : pandas dataframe
        The same log_file but the Label column is now not only benign but the
        corresponding attack name if the instance comfirmed with the attack.

    """
    src, dst = "orig", "resp"
    if vise_versa:
        src, dst = "resp", "orig"

    cond = ((log_file["id."+src+"_h"].str.contains(attack["Source_IP"])) &
            (log_file["id."+dst+"_h"].str.contains(attack["Destination_IP"])) &
            (log_file["ts"] > attack["Start"]) &
            (log_file["ts"] <= attack["End"]))

    if not pd.isnull(attack["Source_Port"]):
        cond = (cond & (log_file["id."+src+"_p"] == attack["Source_Port"]))
    if not pd.isnull(attack["Destination_Port"]):
        cond = (cond & (log_file["id."+dst+"_p"] == attack["Destination_Port"]))
    log_file.loc[cond, 'Label'] = attack["Label"]
    return log_file


def apply_labeling_scheme(log_file, experiment_name):
    """
    Labelling a BRO log file.

    Parameters
    ----------
    log_file : pandas dataframe
        A BRO converted log file.

    experiment_name : string
        The name of the experiment.

    Returns
    -------
    log_file : pandas dataframe
        Original log file with a new column with the corresponding labels.

    """
    df_labels = get_labelling_scheme(experiment_name)
    df_labels = df_labels[(df_labels["Start"] <= log_file["ts"].max()) &
                          (df_labels["End"] >= log_file["ts"].min())]

    log_file['Label'] = "Benign"

    for _, row in tqdm(df_labels.iterrows(), total=df_labels.shape[0]):
        log_file = identify_attack(log_file, row, False)
        log_file = identify_attack(log_file, row, True)
    return log_file


def label_experiment_conn_log(experiment_name):
    """Label conn.log.

    This function starts the labelling procedure on all conn.log files for
    the corresponding experiment_name.

    Parameters
    ----------
    experiment_name : string
        The name of the experiment.
    """
    data_path = get_data_folder(experiment_name, "BRO", "1_Raw")

    pd_list = []
    for file_path in glob.glob(data_path + "**/conn.log", recursive=True):
        conn_log = bro_reader(file_path)[SELECT_COLS]
        uid_label = apply_labeling_scheme(conn_log, experiment_name)
        pd_list.append(uid_label[["uid", "Label"]])
    df_uid_label = pd.concat(pd_list, axis=0)
    file_name = data_path.replace("1_Raw/", "labelling.csv")
    df_uid_label.to_csv(file_name, sep=";", index=False)


if __name__ == "__main__":
    # label_experiment_conn_log("CIC-IDS-2017")
    # label_experiment_conn_log("ISCX-IDS-2012")
    # label_experiment_conn_log("UNSW-NB15")
    # label_experiment_conn_log("CIC-IDS-2018")
    print("Done")
