#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module to feature engineer the ssh.log file."""

__author__ = "Etienne van de Bijl"
__copyright__ = "Copyright (C) 2021 Etienne van de Bijl"
__license__ = "GPL"
__email__ = "evdb@cwi.nl"
__status__ = "Production"

IGNORED_VARS = ["compression_alg", "cipher_alg", "host_key_alg", "kex_alg",
                "mac_alg", "host_key", "direction", "client", "server"]


def preprocessing_ssh(ssh_log):
    """Featur enginer ssh.log file.

    Preprocess ssh log file.

    Parameters
    ----------
    ssh_log : pandas dataframe
        SSH log file.

    Returns
    -------
    ssh_log : pandas dataframe
        Preprocessed ssh file.

    """
    ssh_log['missing_values'] = (ssh_log == "-").sum(axis=1)
    ssh_log = ssh_log.drop(IGNORED_VARS, 1)

    ssh_log.loc[ssh_log["auth_success"] == "-", "auth_success"] = False
    ssh_log["auth_success"] = ssh_log["auth_success"].astype("bool")

    ssh_log.loc[ssh_log["version"] == "-", "version"] = -1
    ssh_log["version"] = ssh_log["version"].astype(int)
    return ssh_log

# from Zeek.Preprocessing.utils import merge_zeek_log_files
# from project_paths import get_data_folder
# zeek_ssh_log = merge_zeek_log_files(get_data_folder("ISCX-IDS-2012", "Zeek",
#                                               "1_Raw"), "ssh")
# df_SSH = preprocessing_ssh(zeek_ssh_log)
