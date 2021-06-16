#!/usr/bin/env python

"""
This module can be used to translate ip addresses to the according host and to
identify whether host belong to the local network.
"""

# Author: Etienne van de Bijl
# License: BSD 3 clause

import pandas as pd

from project_paths import DATA_PATH


def local_ip_addresses(network_info):
    """Retrieve local IP adresses.

    Converts dataframe with info to the local IP addresses.

    Parameters
    ----------
    network_info : pandas dataframe
        Info regarding the network of concern.

    Returns
    -------
    list
       List of local network IP addresses.

    """
    lcl_network = network_info[network_info["Label"] == "Network"]
    local_ip = lcl_network[["IPv4_private", "IPv4_public", "IPv6"]].values.ravel()
    return [ip for ip in local_ip if not pd.isnull(ip)]


def convert_ipv4(network_info):
    """Create dict to convert public to private IPv4."""
    ipv4_data = network_info[["IPv4_private", "IPv4_public"]].dropna()
    ipv4_dict = ipv4_data.set_index('IPv4_private')['IPv4_public'].to_dict()
    return ipv4_dict


def network_preprocessing(log_file, experiment_name):
    """
    Processing of network info. We exclude IPv6 connections.

    Parameters
    ----------
    log_file : pandas dataframe
        A log file to convert all network info.

    experiment_name : string
        Experiment of concern.

    Returns
    -------
    log_file : pandas dataframe
        Updated network info.

    """
    try:
        network_info = pd.read_csv(DATA_PATH + experiment_name +
                                   "/Experiment setup/Network_info_scheme.csv",
                                   sep=";")
    except FileNotFoundError:
        print("Network info scheme does not exist")
        return log_file

    local_ip = local_ip_addresses(network_info)
    ipv4_dict = convert_ipv4(network_info)

    for endpoint in ["orig", "resp"]:
        feature = "id." + endpoint + "_h"

        log_file = log_file[~log_file[feature].str.contains(":")]
        log_file["local_"+endpoint] = log_file[feature].isin(local_ip)

        for private_ip, public_ip in ipv4_dict.items():
            log_file.loc[log_file[feature] == public_ip, feature] = private_ip
    return log_file

# from Zeek.Preprocessing.utils import merge_bro_log_files
# from project_paths import get_data_folder
# conn_log = merge_bro_log_files(get_data_folder("CIC-IDS-2017", "BRO", "1_Raw"), "conn")
# conn_log = network_preprocessing(conn_log, "CIC-IDS-2017")
