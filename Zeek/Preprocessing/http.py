#!/usr/bin/env python

"""
This module is used to proprocess http.log
"""

# Author: Etienne van de Bijl
# License: BSD 3 clause

from urllib.parse import urlparse
import numpy as np

from Zeek.Preprocessing.utils import common_used_practice

#https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods
COMMON_HTTP_METHODS = ["GET", "HEAD", "POST", "PUT", "DELETE", "CONNECT",
                       "OPTIONS", "TRACE", "PATCH"]

COMMON_MIME_TYPES = ["application", "audio", "example", "font", "image",
                     "model", "text", "video"]

COMPONENTS = {1:"netloc", 2:"path", 3:"params", 4:"query", 5:"fragment"}
RESERVED_CHARACTERS = [r"\#", r"\?", r"\&", r"\;", r"\/", r"\+", r"\=", r"\."]

IGNORED_VARS = ["password", "username", "user_agent", "proxied", "tags",
                "orig_filenames", "orig_fuids", "resp_filenames", "resp_fuids",
                "info_msg", "status_msg", "origin"]

def preprocessing_http(http_log):
    """
    Function which proprocesses the HTTP log file.

    Parameters
    ----------
    http_log : pandas dataframe
        HTTP log file.

    Returns
    -------
    http_log : pandas dataframe
        Preprocessed HTTP file.

    """
    http_log['missing_values'] = (http_log == "-").sum(axis=1)
    http_log = http_log.drop(IGNORED_VARS, 1)

    http_log["uri"] = np.where(http_log["uri"].str[:2] == "//",
                               http_log["uri"].str[1:], http_log["uri"])
    http_log["orig_mime_types"] = http_log["orig_mime_types"].str.split('/',
                                                                        expand=True)[0]
    http_log["resp_mime_types"] = http_log["resp_mime_types"].str.split('/',
                                                                        expand=True)[0]

    http_log["version"] = http_log["version"].str.replace("-", "-1").astype(float)

    http_log = common_used_practice(http_log, "method", COMMON_HTTP_METHODS)
    http_log = common_used_practice(http_log, "orig_mime_types", COMMON_MIME_TYPES)
    http_log = common_used_practice(http_log, "resp_mime_types", COMMON_MIME_TYPES)

    http_log = _interpret_uri_http(http_log, "uri")
    http_log = _interpret_uri_http(http_log, "host")
    http_log = _interpret_uri_http(http_log, "referrer")

    http_log["1xx_code"] = http_log["info_code"].astype(str).str.startswith("1")
    http_log["status_code"] = http_log["status_code"].astype(str)
    for i in range(2, 6):
        http_log[str(i) + "xx_code"] = http_log["status_code"].str.startswith(str(i))
    http_log = http_log.drop(["status_code", "info_code"], 1)
    return http_log

def _interpret_uri_http(http_log, feature):
    """
    count items in uri/url.

    Parameters
    ----------
    http_log : pandas dataframe
        HTTP log dataset.

    feature : string
        feature with uri/url component.

    Returns
    -------
    http_log
        new added features.

    """
    for index, value in COMPONENTS.items():
        name = feature + "_" + value
        http_log[name] = http_log[feature].apply(lambda x: uri_component(x, index))

        http_log[name+"_len"] = http_log[name].str.len()
        http_log[name+"_unique_char"] = http_log[name].apply(lambda x: len("".join(set(x))))
        http_log[name+"_res_char_n"] = http_log[name].apply(func)
        http_log = http_log.drop([name], 1)
    return http_log.drop([feature], 1)

def func(url):
    """
    Parameters
    ----------
    url : string
        A url

    Returns
    -------
    int
        Number of reserved characters

    """
    return len([c for c in set(url) if not c.isalnum()])

def uri_component(url, index):
    """
    Get the index url part.

    Parameters
    ----------
    url : string
        Uri/url

    i : integer
        integer to get some part of the uri.

    Returns
    -------
    TYPE
        .

    """
    try:
        return urlparse(url)[index]
    except ValueError:
        return ""

#from project_paths import NID_PATH; from BRO.Preprocessing.utils import bro_reader
#bro_df = bro_reader(NID_PATH + "CIC-IDS-2017/BRO/1_Raw/Friday-WorkingHours/http.log")
#http_log_new = preprocessing_http(bro_df)
