#!/usr/bin/env python

"""
This module is used to proprocess ssh.log
"""

# Author: Etienne van de Bijl
# License: BSD 3 clause

IGNORED_VARS = ["compression_alg", "cipher_alg", "host_key_alg", "kex_alg",
                "mac_alg", "host_key", "direction", "client", "server"]

def preprocessing_ssh(ssh_log):
    """
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

#from Zeek.Preprocessing.utils import merge_bro_log_files
#from project_paths import get_data_folder
#ssh_log = merge_bro_log_files(get_data_folder("ISCX-IDS-2012", "BRO", "1_Raw"), "ssh")
#ssh_log_new = preprocessing_ssh(ssh_log)
