#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main program to preprocess log files constructed by Zeek."""

__author__ = "Etienne van de Bijl"
__copyright__ = "Copyright (C) 2021 Etienne van de Bijl"
__license__ = "GPL"
__email__ = "evdb@cwi.nl"
__status__ = "Production"

import warnings
import datetime
import pandas as pd

from project_paths import get_data_folder
from Zeek.utils import fix_col_order, statistics_dataset
from Zeek.Preprocessing.utils import merge_zeek_log_files
from Zeek.Preprocessing.network import network_preprocessing
from Zeek.Preprocessing.conn import preprocessing_conn
from Zeek.Preprocessing.ftp import preprocessing_ftp
from Zeek.Preprocessing.http import preprocessing_http
from Zeek.Preprocessing.ssh import preprocessing_ssh
from Zeek.Preprocessing.ssl_ import preprocessing_ssl
from Zeek.Preprocessing.dns import preprocessing_dns

from application import Application, tk

warnings.filterwarnings("ignore")

FUNCTIONS = {"dns": preprocessing_dns,
             "ftp": preprocessing_ftp,
             "http": preprocessing_http,
             "ssh": preprocessing_ssh,
             "ssl": preprocessing_ssl}


def finish_dataset(log_file, df_uid_label, experiment, output_path, protocol):
    """Preprocess dataset."""
    print("-----Network Transformation-----  " + str(datetime.datetime.now()))
    log_file = network_preprocessing(log_file, experiment)
    print("-----Apply Labelling------------  " + str(datetime.datetime.now()))
    log_file = log_file.merge(df_uid_label, how="left", on="uid")
    print("-----Apply Final Touch----------  " + str(datetime.datetime.now()))
    log_file = fix_col_order(log_file)
    log_file.sort_values(by=['ts', "uid"], inplace=True)
    print("-----Writing Data---------------  " + str(datetime.datetime.now()))
    log_file.to_csv(output_path + protocol + ".csv", index=False)
    print("-----Saving statistics----------  " + str(datetime.datetime.now()))
    statistics_dataset(log_file, output_path, protocol)
    print("-----" + experiment + "-" + protocol.upper() + "-Completed-  " +
          str(datetime.datetime.now()) + "\n")


def main(experiment, protocols_list):
    """Iterate log files.

    This script calls all protocol preprocessing function to preprocess
    the Zeek log files. Only TCP and UDP are performed together as they
    belong in the same conn.log so we cannot seperately preprocess these.
    It is possible, but not desired for now.

    Parameters
    ----------
    experiment : string
        Performs the task

    protocols_list: list of strings
        List of the protocols of interest for this job
    """
    data_path = get_data_folder(experiment, "Zeek", "1_Raw")
    output_path = get_data_folder(experiment, "Zeek", "2_Preprocessed")
    uid_label = pd.read_csv(data_path.replace("1_Raw/", "labelling.csv"),
                            sep=";")

    for protocol in protocols_list:
        log_file = merge_zeek_log_files(data_path, protocol)

        if log_file.empty:
            continue

        if protocol == "conn":
            tcp_log, udp_log = preprocessing_conn(log_file)
            finish_dataset(tcp_log, uid_label, experiment, output_path, "tcp")
           # finish_dataset(udp_log, uid_label, experiment, output_path, "udp")
        else:
            log_file = FUNCTIONS[protocol](log_file)
            finish_dataset(log_file, uid_label, experiment,
                           output_path, protocol)


if __name__ == "__main__":
    APP = Application(master=tk.Tk())
    APP.mainloop()
    for exp in APP.selected_values["Experiments"]:
        main(exp, APP.selected_values["Files"])
