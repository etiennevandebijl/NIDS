#!/usr/bin/env python

"""Utils for Zeek."""

__author__ = "Etienne van de Bijl"
__copyright__ = "Copyright 2021, CWI"
__license__ = "GPL"
__email__ = "evdb@cwi.nl"
__status__ = "Production"

import io
import datetime
import numpy as np
import pandas as pd

IGNORE_COLS = ["uid", "ts", "ts_", "id.orig_h", "id.resp_h", "id.resp_p",
               "id.orig_p", "local_orig", "local_resp"]


def format_ML(df, binary=False):
    """Convert df to ML ready format."""
    df = df.drop([c for c in IGNORE_COLS if c in df.columns], 1)

    if "duration" in df.columns:
        df["duration"] = df["duration"] / datetime.timedelta(seconds=1)

    if binary:
        df["Label"] = df["Label"] != "Benign"

    X = df.drop(["Label"], 1)
    feature_names = X.columns.tolist()
    X = X.values * 1.0

    y = np.ravel(df["Label"])
    labels = np.unique(y)
    if binary:
        labels = [False, True]
    return X, y, feature_names, labels


def fix_col_order(df):
    """Set columns of csv in preferred order."""
    pref = ["uid", "ts", "ts_", "id.orig_h", "id.orig_p", "id.resp_h",
            "id.resp_p", "local_orig", "local_resp", "duration"]
    pref = [c for c in pref if c in df.columns]
    order = pref + [c for c in df.columns if (c not in pref and c != "Label")]
    if "Label" in df.columns:
        order = order + ["Label"]
    df = df[order]
    return df


def statistics_dataset(df, output_path, protocol):
    """Gather statistics of dataset and write them to txt."""
    shape = df.shape
    label_counts = df["Label"].value_counts()
    df.loc[df["Label"] != "Benign", "Label"] = "Malicious"
    normal_counts = df["Label"].value_counts()
    file = open(output_path + protocol + ".txt", "w")
    file.write("Shape: %s\r\n" % str(shape))
    buffer = io.StringIO()
    df.info(buf=buffer)
    s = buffer.getvalue()
    file.write(s)
    file.write("\n")
    file.write("Intrusion stats: \n")
    file.write("%s\r\n" % str(normal_counts))
    file.write("Label stats: \n")
    file.write("%s\r\n" % str(label_counts))
    file.close()


def read_preprocessed(path):
    """Read Zeek csv."""
    df = pd.read_csv(path)
    df["ts"] = pd.to_datetime(df["ts"])
    if "ts_" in df.columns:
        df["ts_"] = pd.to_datetime(df["ts_"])
    if "duration" in df.columns:
        df["duration"] = pd.to_timedelta(df["duration"])
    return df


def print_progress(experiment, version, file):
    """Print progress."""
    base = "---"
    loc1 = (15 - len(experiment)) * "-"
    loc2 = (21 - len(version)) * "-"
    loc3 = (10 - len(file)) * "-"
    printable = base + experiment + loc1 + version + loc2 + file + loc3
    printable = printable + str(datetime.datetime.now())
    print(printable)
