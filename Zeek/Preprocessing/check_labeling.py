# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 14:56:51 2021

@author: Etienne
"""
import pandas as pd
from project_paths import get_data_folder

data_path = get_data_folder("CIC-IDS-2018", "BRO", "1_Raw")
file_name = data_path.replace("1_Raw/", "labelling.csv")
df = pd.read_csv(file_name, sep =";")

df["Label"].value_counts()
len(df["uid"].unique())
df.shape

