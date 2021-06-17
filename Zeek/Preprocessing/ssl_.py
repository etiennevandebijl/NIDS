#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module is used to proprocess ssl.log."""

__author__ = "Etienne van de Bijl"
__copyright__ = "Copyright (C) 2021 Etienne van de Bijl"
__license__ = "GPL"
__email__ = "evdb@cwi.nl"
__status__ = "Production"
from Zeek.Preprocessing.utils import common_used_practice

COMMON_NEXT_PROTOCOL = ["http/1.1", "h2"]
IGNORED_VARS = ["cert_chain_fuids", "client_cert_chain_fuids",
                "client_subject", "client_issuer", "issuer",
                "subject", "cipher", "curve"]


def preprocessing_ssl(ssl_log):
    """Preprocess ssl.log files of Zeek.

    Function to process ssl.log file.

    Parameters
    ----------
    ssl_log : pandas dataframe
        A converted bro file of the ssl.log.

    Returns
    -------
    ssl_log : pandas dataframe
        A preprocessed ssl log file.

    """
    ssl_log['missing_values'] = (ssl_log == "-").sum(axis=1)
    ssl_log = ssl_log.drop(IGNORED_VARS, 1)

    ssl_log["version"] = ssl_log["version"].str.replace("-", "0")
    ssl_log["version"] = ssl_log["version"].str.extract(r'(\d+)').astype(int)

    ssl_log = common_used_practice(ssl_log, "last_alert", [])
    ssl_log = common_used_practice(ssl_log, "next_protocol",
                                   COMMON_NEXT_PROTOCOL)

    ssl_log["server_name_dot"] = ssl_log["server_name"].str.count(r'\.')
    ssl_log["server_name_dash"] = ssl_log["server_name"].str.count("-")
    ssl_log["server_name_len"] = ssl_log["server_name"].str.len()
    ssl_log["server_name_unq"] = ssl_log["server_name"].apply(lambda x:
                                                              len("".join(set(x))))
    ssl_log = ssl_log.drop(["server_name"], 1)

    return ssl_log

# from Zeek.Preprocessing.utils import merge_bro_log_files
# from project_paths import get_data_folder
# zeek_ssl_log = merge_bro_log_files(get_data_folder("CIC-IDS-2017",
#                                                    "BRO", "1_Raw"), "ssl")
# df_SSL = preprocessing_ssl(zeek_ssl_log)
