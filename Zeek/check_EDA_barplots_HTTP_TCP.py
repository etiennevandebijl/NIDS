#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 14:43:57 2022

@author: etienne
"""


path = get_data_folder("CIC-IDS-2017", "BRO", "2_Preprocessed_DDoS") + "http-tcp" + ".csv"
dataset = read_preprocessed(path)

dataset = dataset[dataset["referrer_query_len"] > 5000]

# 	uid
# 5323	C6zv9qN8qnxR3vKw6
# 5330	CHW81C3v7M95WUPwVk
# 5331	CLT7VS1FTggGHwok2f
# 5332	CpavB3xwI5VyA1lig
# 5335	CKhZa82edrEKlS1g9g
# 5336	CHW81C3v7M95WUPwVk
# 5339	CrGZnC3YltcCUajRMc

from Zeek.Preprocessing.utils import merge_bro_log_files
from project_paths import get_data_folder
zeek_http_log = merge_bro_log_files(get_data_folder("CIC-IDS-2017", "BRO", "1_Raw"), "http")
df = zeek_http_log[zeek_http_log["uid"] == "CKhZa82edrEKlS1g9g"]