#!/usr/bin/env python

"""
This module contains the proprocessing steps of the conn.log file.
TCP and UDP are seperated as they have many non-overlapping features.
"""

# Author: Etienne van de Bijl
# License: BSD 3 clause

import numpy as np
from Zeek.Preprocessing.utils import common_used_practice

COMMON_SERVICE_TCP = ["http", "krb_tcp", "dce_rpc", "ssl", "ftp-data", "ftp",
                      "ssh", "pop3", "smtp", "imap", "irc", "rfb"]
COMMON_SERVICE_UDP = ["dns", "krb", "dhcp"]

def preprocessing_conn(conn_log):
    """
    This function starts the preprocessing of the conn.log file.

    Parameters
    ----------
    conn_log : pandas dataframe
        DESCRIPTION.

    Returns
    -------
    tcp_log : pandas dataframe
        Log information regarding tcp traffic.
    udp_log : pandas dataframe
        Log information regarding udp traffic.

    """
    conn_log = _cleaning_conn(conn_log)
    udp_log = _udp_connections(conn_log)
    tcp_log = _tcp_connections(conn_log)
    return tcp_log, udp_log

# =============================================================================
# Cleaning
# =============================================================================

def _cleaning_conn(conn_log):
    """
    Here the first steps on the cleaning conn.log are done. This consists of
    taking care of time and packets/bytes.

    Parameters
    ----------
    conn_log : pandas dataframe
        Conn.log of the BRO/Zeek tool.

    Returns
    -------
    conn_log : pandas dataframe
        Cleaned file.

    """
    conn_log.drop("tunnel_parents", 1, inplace=True)

    for col in ["resp_bytes", "orig_bytes", "orig_pkts", "resp_pkts"]:
        if conn_log[col].dtype != "int64":
            conn_log[col] = conn_log[col].replace({'-':"0"})
        conn_log[col] = conn_log[col].astype(float)

    conn_log["ts_"] = conn_log["ts"] + conn_log["duration"]

    conn_log["orig_bpp"] = np.where(conn_log["orig_pkts"] > 0,
                                    conn_log["orig_bytes"] / conn_log["orig_pkts"], 0)
    conn_log["resp_bpp"] = np.where(conn_log["resp_pkts"] > 0,
                                    conn_log["resp_bytes"] / conn_log["resp_pkts"], 0)
    conn_log["PCR"] = np.where((conn_log["orig_bytes"] + conn_log["resp_bytes"]) > 0,
                               (conn_log["orig_bytes"] - conn_log["resp_bytes"]) / \
                               (conn_log["orig_bytes"] + conn_log["resp_bytes"]), 0)
    return conn_log

# =============================================================================
# UDP Connections
# =============================================================================
def _udp_connections(conn_log):
    """
    Udp connections are processed here. State and history are not relevant
    as udp does not know states.

    Parameters
    ----------
    conn_log : pandas dataframe
        Log file of network traffic.

    Returns
    -------
    udp_log : pandas dataframe
        UDP log file with all relevant features.

    """
    udp_log = conn_log[conn_log["proto"] == "udp"]
    udp_log["orig_active"] = udp_log["conn_state"].isin(["SF", "S0"]) #Active state
    udp_log["resp_active"] = udp_log["conn_state"].isin(["SF", "SHR"]) #Active state

    udp_log.drop(["proto", "conn_state", "missed_bytes", "history"], 1, inplace=True)

    udp_log["IPv6"] = udp_log["id.orig_h"].str.contains(":") #Smart temporal variable
    for endp in ["orig", "resp"]:
        udp_log[endp + "_min_size"] = (udp_log[endp + "_ip_bytes"] - \
                                       udp_log[endp + "_bytes"]) / \
                                       udp_log[endp + "_pkts"]
        udp_log[endp + "_min_size"] = ((udp_log[endp + "_min_size"] == 28) &
                                       (~udp_log["IPv6"])) | \
                                       ((udp_log[endp + "_min_size"] == 48) &
                                        (udp_log["IPv6"]))
        udp_log.loc[udp_log[endp + "_pkts"] == 0, endp + "_min_size"] = True

    udp_log.drop(["orig_ip_bytes", "resp_ip_bytes", "IPv6"], 1, inplace=True)

    udp_log = common_used_practice(udp_log, "service", COMMON_SERVICE_UDP)
    return udp_log

# =============================================================================
# TCP Connections
# =============================================================================

def _tcp_connections(conn_log):
    """
    Function to work on the tcp connections of conn log.

    Parameters
    ----------
    conn_log : pandas dataframe
        Log file of the TCP traffic.

    Returns
    -------
    tcp_log : pandas dataframe
        TCP info dataset.

    """
    tcp_log = conn_log[conn_log["proto"] == "tcp"]
    tcp_log = _tcp_state_features(tcp_log)

    tcp_log = tcp_log.drop(["proto", "conn_state", "history"], 1)
    tcp_log = common_used_practice(tcp_log, "service", COMMON_SERVICE_TCP)
    return tcp_log

def _tcp_state_features(tcp_log):
    """
    Function to built TCP state features.

    Parameters
    ----------
    tcp_log : pandas dataframe
        Conn log with only TCP traffic.

    Returns
    -------
    tcp_log : pandas dataframe
        Added some nice TCP state features.

    """
    tcp_log["history"] = tcp_log["history"].str.replace(r'\^', "")
    tcp_log["history"] = tcp_log["history"].str.replace("hS", "Sh")
    tcp_log["history"] = tcp_log["history"].str.replace("Hs", "Sh")
    tcp_log["history"] = tcp_log["history"].str.replace("SAh", "ShA") #Still there

    # Handshake features
    tcp_log["S0"] = ~tcp_log.history.str.contains("S")
    tcp_log["S1"] = tcp_log["history"] == "S"                                           #S0
    tcp_log["S2"] = tcp_log["history"] == "Sh"                                          #S1
    tcp_log["S3"] = tcp_log["history"].str.startswith("ShA") #Complete handshake

    tcp_log["REJ1"] = tcp_log["history"] == "Sr"                                        #REJ
    tcp_log["REJ2O"] = tcp_log["history"] == "ShR"                                      #RSTO 
    tcp_log["REJ2R"] = tcp_log["history"] == "Shr"

    handshake_features = ["S1", "S2", "S3", "REJ1", "REJ2O", "REJ2R"]
    tcp_log["WEIRD"] = ((tcp_log["history"].str.contains("S")) &
                        (~tcp_log[handshake_features].any(axis='columns')))

    #Flags
    for flag in ["r", "R", "f", "F"]:
        tcp_log[flag] = tcp_log["history"].str.contains(flag)                           #Check if there are certain flags

    for flag in ['d', 'D',"T", "t","c", "C", "g", "G", "w", "W", "i", "I", "q", "Q"]: 
        tcp_log[flag] = tcp_log["history"].str.count(flag)     

    tcp_log["OPEN"] = (~tcp_log[["r", "R", "f", "F"]].any(axis='columns') &
                       tcp_log[["S3", "WEIRD"]].any(axis='columns'))

    #Termination
    tcp_log["CLSO"] = (tcp_log["F"] & ~tcp_log[["r", "R", "f"]].any(axis='columns'))
    tcp_log["CLSR"] = (tcp_log["f"] & ~tcp_log[["r", "R", "F"]].any(axis='columns'))

    tcp_log["TERM"] = (tcp_log["F"] & tcp_log["f"])

    tcp_log["RSTR"] = (~tcp_log["TERM"] & tcp_log["r"] &
                       (~tcp_log["R"] | (tcp_log.history.str.find("r") <
                                         tcp_log.history.str.find("R"))))

    tcp_log["RSTO"] = (~tcp_log["TERM"] & tcp_log["R"] &
                       (~tcp_log["r"] | (tcp_log.history.str.find("R") <
                                         tcp_log.history.str.find("r"))))

    tcp_log.drop(["f", "F", "r", "R"], 1, inplace=True)
    return tcp_log

#from project_paths import NID_PATH; from BRO.Preprocessing.utils import bro_reader
#bro_df = bro_reader(NID_PATH + "CIC-IDS-2017/BRO/1_Raw/Tuesday-WorkingHours/conn.log")
#df_TCP, df_UDP = preprocessing_conn(bro_df)
