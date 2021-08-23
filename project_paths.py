#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Script for setting paths to the required files."""

__author__ = "Etienne van de Bijl"
__copyright__ = "Copyright 2021, CWI"
__license__ = "GPL"
__email__ = "evdb@cwi.nl"
__status__ = "Production"

import os
import pandas as pd

if os.path.isdir('C:/Users/Etienne/'):
    OS_PATH = "C:/Users/Etienne/Dropbox/Internship Business Analytics/"
else:
    OS_PATH = "/home/etienne/Dropbox/Internship Business Analytics/"
PROJECT_PATH = OS_PATH + "Project Graph-Based Intrusion Detection/"
DATA_PATH = PROJECT_PATH + "Intrusion Detection Datasets/"


def get_data_folder(experiment_name, analyser, version):
    """Retrieve path to set of datasets."""
    return DATA_PATH + experiment_name + "/" + analyser + "/" + version + "/"


def get_labelling_scheme(experiment_name):
    """Get path of labelling scheme."""
    path = DATA_PATH + experiment_name + "/Experiment setup/Labeling_scheme.csv"
    return pd.read_csv(path, sep=";", parse_dates=["Start", "End"])


def get_results_folder(experiment_name, analyser, version, method):
    """Return of result folder."""
    path = PROJECT_PATH + "Results/" + experiment_name + "/" + analyser \
        + "/" + version + "/" + method + "/"
    return path


def go_or_create_folder(path, folder):
    """Path walks to path + folder and creates it is necessary."""
    if not os.path.isdir(path+folder):
        os.mkdir(path + folder)
    return path + folder + "/"
