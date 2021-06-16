#!/usr/bin/env python

"""Script to proprocess dns.log."""

# Author: Etienne van de Bijl
# License: BSD 3 clause

import numpy as np
import pandas as pd

from Zeek.Preprocessing.utils import common_used_practice

COMMON_RCODES = list(range(6))
COMMON_QCLASS = [0, 1, 3, 4, 254, 255]
COMMON_QTYPE = [1, 2, 5, 6, 12, 15, 16, 20, 28]

# https://www.ietf.org/rfc/rfc1035.txt
# https://www.iana.org/assignments/dns-parameters/dns-parameters.xhtml
# http://dns-record-viewer.online-domain-tools.com/

IGNORED_VARS = ["rcode_name", "qclass_name", "qtype_name",
                "trans_id", "answers", "query"]


def preprocessing_dns(dns_log):
    """
    Dns log file preprocessing.

    Parameters
    ----------
    dns_log : pandas dataframe
        dns log bro.

    Returns
    -------
    dns_log : TYPE
        preprocessed dns file.

    """
    dns_log['missing_values'] = (dns_log == "-").sum(axis=1)
    dns_log = dns_log.drop(IGNORED_VARS, 1)

    dns_log["rtt"] = pd.to_timedelta(dns_log["rtt"]).dt.microseconds
    dns_log["Z"] = dns_log["Z"].astype(bool)

    dns_log = _aggregate_connection_dns(dns_log)

    dns_log = common_used_practice(dns_log, "proto", ["udp"])
    dns_log = common_used_practice(dns_log, "rcode", COMMON_RCODES)
    dns_log = common_used_practice(dns_log, "qclass", COMMON_QCLASS)
    dns_log = common_used_practice(dns_log, "qtype", COMMON_QTYPE)

    dns_log["answers_n"] = dns_log["TTLs"].str.count(",")
    dns_log["TTLs_mean"] = dns_log["TTLs"].apply(lambda x: np.mean(_ttls_fun_dns(x)))
    dns_log["TTLs_min"] = dns_log["TTLs"].apply(lambda x: np.min(_ttls_fun_dns(x)))
    dns_log["TTLs_max"] = dns_log["TTLs"].apply(lambda x: np.max(_ttls_fun_dns(x)))
    dns_log = dns_log.drop(["TTLs"], 1)
    return dns_log


def _aggregate_connection_dns(dns_log):
    """
    Worth noding: this still does not mean that the connections are unique.

    Parameters
    ----------
    dns_log : pandas dataframe
        dns log.

    Returns
    -------
    dns_log : pandas dataframe
        dns log combined per uid.

    """
    cols = [x for x in dns_log.columns if x not in ["ts", "rtt"]]
    dns_log = dns_log.groupby(cols).agg({'rtt': ['min', 'mean', "max"],
                                         'ts': ["count", "min",
                                                "max"]}).reset_index()
    dns_log.columns = cols + ["rtt_min", "rtt_mean", "rtt_max",
                              "count", "ts", "ts_"]
    dns_log["duration"] = (dns_log["ts_"] - dns_log["ts"])
    return dns_log


def _ttls_fun_dns(ttls):
    """
    Parameters
    ----------
    ttls : string
        String of lists with ttls times

    Returns
    -------
    ttls mean
        list of the values

    """
    if ttls == "-":
        value = [-1.0]
    elif "," in ttls:
        value = list(map(float, ttls.split(",")))
    else:
        value = [float(ttls)]
    return value

#from project_paths import NID_PATH; from Zeek.Preprocessing.utils import bro_reader
#bro_df = bro_reader(NID_PATH + "CIC-IDS-2017/BRO/1_Raw/Friday-WorkingHours/dns.log")
#dns_log_new = preprocessing_dns(bro_df)
