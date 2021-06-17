#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module to check labelling dataset."""

__author__ = "Etienne van de Bijl"
__copyright__ = "Copyright 2021, CWI"
__license__ = "GPL"
__email__ = "evdb@cwi.nl"
__status__ = "Production"

import pandas as pd
from project_paths import get_data_folder

data_path = get_data_folder("CIC-IDS-2018", "BRO", "1_Raw")
file_name = data_path.replace("1_Raw/", "labelling.csv")
df = pd.read_csv(file_name, sep=";")

print(df["Label"].value_counts())
# Test if uid are unique:
print(len(df["uid"].unique()) == df.shape[0])
