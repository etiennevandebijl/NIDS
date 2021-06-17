#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module to preprocess the http.log file of Zeek."""

__author__ = "Etienne van de Bijl"
__copyright__ = "Copyright 2021, CWI"
__license__ = "GPL"
__email__ = "evdb@cwi.nl"
__status__ = "Production"

from urllib.parse import urlparse
import numpy as np

from Zeek.Preprocessing.utils import common_used_practice

# https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods
COMMON_HTTP_METHODS = ["GET", "HEAD", "POST", "PUT", "DELETE",
                       "CONNECT", "OPTIONS", "TRACE", "PATCH"]

COMMON_MIME_TYPES = ["application", "audio", "example", "font",
                     "image", "model", "text", "video"]

COMPONENTS = {1: "netloc", 2: "path", 3: "params", 4: "query", 5: "fragment"}
RESERVED_CHARACTERS = [r"\#", r"\?", r"\&", r"\;", r"\/", r"\+", r"\=", r"\."]

IGNORED_VARS = ["password", "username", "user_agent", "proxied", "tags",
                "orig_filenames", "orig_fuids", "resp_filenames", "resp_fuids",
                "info_msg", "status_msg", "origin"]


def preprocessing_http(http_log):
    """Preprocess http.log of Zeek.

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
    for col in ["orig_mime_types", "resp_mime_types"]:
        http_log[col] = http_log[col].str.split('/', expand=True)[0]

    http_log["version"] = http_log["version"].str.replace("-",
                                                          "-1").astype(float)

    http_log = common_used_practice(http_log, "method", COMMON_HTTP_METHODS)
    http_log = common_used_practice(http_log, "orig_mime_types",
                                    COMMON_MIME_TYPES)
    http_log = common_used_practice(http_log, "resp_mime_types",
                                    COMMON_MIME_TYPES)

    http_log = _count_info_uri_http(http_log, "uri")
    http_log = _count_info_uri_http(http_log, "host")
    http_log = _count_info_uri_http(http_log, "referrer")

    http_log["info_code"] = http_log["info_code"].astype(str)
    http_log["1xx_code"] = http_log["info_code"].str.startswith("1")
    http_log["status_code"] = http_log["status_code"].astype(str)
    for i in range(2, 6):
        http_log[str(i) +
                 "xx_code"] = http_log["status_code"].str.startswith(str(i))
    http_log = http_log.drop(["status_code", "info_code"], 1)
    return http_log


def _count_info_uri_http(http_log, feature):
    """Gather statistics from URI/URL.

    Count items in uri/url.

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
        http_log[name] = http_log[feature].apply(lambda x:
                                                 uri_component(x, index))

        http_log[name+"_len"] = http_log[name].str.len()
        http_log[name+"_unique_char"] = http_log[name].apply(lambda x:
                                                             len("".join(set(x))))
        http_log[name+"_res_char_n"] = http_log[name].apply(func)
        http_log = http_log.drop([name], 1)
    return http_log.drop([feature], 1)


def func(url):
    """Count number of reserved characters."""
    return len([c for c in set(url) if not c.isalnum()])


def uri_component(url, index):
    """Parse uri component."""
    try:
        return urlparse(url)[index]
    except ValueError:
        return ""

# from project_paths import DATA_PATH
# from Zeek.Preprocessing.utils import zeek_reader
# zeek_http_log = zeek_reader(DATA_PATH + "CIC-IDS-2017/BRO/1_Raw/" +
#                             "Friday-WorkingHours/http.log")
# df_HTTP = preprocessing_http(zeek_http_log)
