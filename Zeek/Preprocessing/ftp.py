#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module to preprocess the ftp.log file of Zeek."""

__author__ = "Etienne van de Bijl"
__copyright__ = "Copyright 2021, CWI"
__license__ = "GPL"
__email__ = "evdb@cwi.nl"
__status__ = "Production"

import numpy as np

from Zeek.Preprocessing.utils import common_used_practice

# http://www.nsftools.com/tips/RawFTP.htm
# COMMON_COMMANDS = ["ABOR", "CWD", "DELE", "LIST", "MDTM", "MKD", "NLST",
#                     "PASS", "PASV", "PORT", "PWD", "QUIT", "RETR", "RMD",
#                     "RNFR", "RNTO", "SITE", "SIZE", "STOR", "TYPE", "USER"]

COMMON_COMMANDS = ["APPE", 'PASV', 'STOR', 'RETR',
                   'DELE', 'PORT', "EPSV", "STOU"]

COMMON_MIME_TYPES = ["application", "audio", "example", "font", "image",
                     "model", "text", "video"]

COMMON_REPLY_CODE_D1 = [1, 2, 3, 4, 5, 6]
COMMON_REPLY_CODE_D2 = [0, 1, 2, 3, 4, 5]

IGNORED_VARS = ["user", "password", "arg", "fuid", "reply_msg",
                "data_channel.orig_h", "data_channel.resp_h",
                "data_channel.resp_p", "data_channel.passive"]

UID_TS_ID = ["uid", "ts", "id.orig_h", "id.orig_p", "id.resp_h", "id.resp_p"]


def preprocessing_ftp(ftp_log):
    """Preprocess ftp.log file of Zeek.

    Preprocess the ftp.log files.

    Parameters
    ----------
    ftp_log : pandas dataframe
        A ftp log file.

    Returns
    -------
    ftp_log : pandas dataframe
        A new FTP log file based on the new features.

    """
    ftp_log['missing_values'] = (ftp_log == "-").sum(axis=1)
    ftp_log = ftp_log.drop(IGNORED_VARS, 1)

    ftp_log["file_size"] = ftp_log["file_size"].replace({'-': "0"})

    ftp_log["mime_type"] = ftp_log["mime_type"].str.split('/', expand=True)[0]

    ftp_log["reply_code"] = ftp_log["reply_code"].astype(str)
    ftp_log["reply_code_d1"] = np.where(ftp_log["reply_code"].str.len() == 3,
                                        ftp_log["reply_code"].str[0], "-")
    ftp_log["reply_code_d2"] = np.where(ftp_log["reply_code"].str.len() == 3,
                                        ftp_log["reply_code"].str[1], "-")

    ftp_log = common_used_practice(ftp_log, "command", COMMON_COMMANDS)
    ftp_log = common_used_practice(ftp_log, "mime_type", COMMON_MIME_TYPES)
    ftp_log = common_used_practice(ftp_log, "reply_code_d1",
                                   COMMON_REPLY_CODE_D1)
    ftp_log = common_used_practice(ftp_log, "reply_code_d2",
                                   COMMON_REPLY_CODE_D2)

    ftp_log = ftp_log.drop(["reply_code"], 1)

    ftp_log = _combine_ftp(ftp_log)
    return ftp_log


def _combine_ftp(ftp_log):
    """Merge FTP traffic on session uid.

    Merge all ftp traffic by the corresponding connection uid. The sum of all
    observed traffic is taken to get estimates on the behaviour.

    Parameters
    ----------
    ftp_log : pandas dataframe
        A ftp log file.

    Returns
    -------
    ftp_log_new : pandas dataframe
        A compressed ftp file.

    """
    uid_interval = ftp_log.groupby("uid")["ts"].agg([np.min,
                                                     np.max]).reset_index()
    uid_interval.columns = ["uid", "ts", "ts_"]
    uid_interval["duration"] = uid_interval["ts_"] - uid_interval["ts"]

    features = [c for c in ftp_log.columns if c not in UID_TS_ID]
    uid = [c for c in UID_TS_ID if c != "ts"]
    ftp_compressed_f = ftp_log.groupby(uid)[features].sum().reset_index()
    ftp_log_new = ftp_compressed_f.merge(uid_interval, how="left", on="uid")
    return ftp_log_new

# from Zeek.Preprocessing.utils import merge_bro_log_files
# from project_paths import get_data_folder
# zeek_ftp_log = merge_bro_log_files(get_data_folder("ISCX-IDS-2012",
#                                                    "BRO", "1_Raw"), "ftp")
# df_FTP = preprocessing_ftp(zeek_ftp_log)
