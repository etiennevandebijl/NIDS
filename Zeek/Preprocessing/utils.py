# !/usr/bin/env python

"""
This module preprocesses all log files in the 2_Preprocessed folder.
"""

# Author: Etienne van de Bijl
# License: BSD 3 clause

import glob
import datetime
import pandas as pd

from brothon import bro_log_reader


def bro_reader(path):
    """
    This function reads a log file of the bro reader. Also adjusts the time-zones
    of the different datasets. Makes "ts" and "duration" in right format.

    Parameters
    ----------
    path : string
        Path to file.

    Returns
    -------
    log_file : pandas dataframe
        A log file with the corresponding log file in pandas form.

    """
    reader = bro_log_reader.BroLogReader(path)
    log_file = pd.DataFrame(reader.readrows())
    log_file["ts"] = pd.to_datetime(log_file["ts"])

    if ("CIC-IDS-2017" in path or "ISCX-IDS-2012" in path or "CIC-IDS-2018" in path):
        log_file["ts"] = log_file["ts"] - datetime.timedelta(hours=5) #Convert for canadian time

    if "UNSW-NB15" in path:
        log_file["ts"] = log_file["ts"] - datetime.timedelta(hours=9) #Convert Australian time

    if "duration" in log_file.columns:
        log_file["duration"] = pd.to_timedelta(log_file["duration"])
    return log_file

def merge_bro_log_files(experiment_path, file_name):
    """
    This function combines the different log files of a certain file_name.

    Parameters
    ----------
    experiment_path : string
        Path to the folder of the experiment.
    file_name : string
        File name of interest.

    Returns
    -------
    log_file : pandas dataframe
        Merged log file.

    """
    pd_list = []
    for path in glob.glob(experiment_path + "**/" + file_name + ".log", recursive=True):
        data = bro_reader(path)
        pd_list.append(data)
    log_file = pd.DataFrame()
    if len(pd_list) > 0:
        log_file = pd.concat(pd_list, axis=0)
    return log_file


def common_used_practice(log_file, feature, signatures):
    """
    This function does a one-hot encoder operation with a given set of signatures.

    Parameters
    ----------
    log_file : pandas dataframe
        Log file to one-hot encode.
    feature : string
        Feature to one-hot encode.
    signatures : list of strings
        List of signatures to one-hot encode.

    Returns
    -------
    log_file : pandas dataframe
        Log file which is one-hot encoded.

    """
    log_file[feature] = log_file[feature].astype(str)
    list_ = [str(s) for s in signatures] + ["-"]
    for i in list_:
        log_file[feature+"_"+i] = log_file[feature] == i
    log_file[feature+"_other"] = ~log_file[feature].isin(list_)
    log_file.drop(feature, 1, inplace=True)
    return log_file
