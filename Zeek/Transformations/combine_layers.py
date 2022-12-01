#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Script to merge transport layer with application layer protocols."""

__author__ = "Etienne van de Bijl"
__copyright__ = "Copyright 2021, CWI"
__license__ = "GPL"
__email__ = "evdb@cwi.nl"
__status__ = "Production"

import os

from project_paths import get_data_folder
from Zeek.utils import read_preprocessed, fix_col_order, \
    statistics_dataset, print_progress

ON_COLS = ["uid", "id.orig_h", "id.orig_p", "id.resp_h", "id.resp_p",
           "local_orig", "local_resp", "Label"]


def process_merge(df_n, df_a, protocol_name, output_path):
    """Merge two layers."""
    df_merge = df_a.merge(df_n, how="left", on=ON_COLS)
    df_merge = fix_col_order(df_merge)
    df_merge = df_merge.dropna()
    df_merge.to_csv(output_path + protocol_name + ".csv", index=False)
    statistics_dataset(df_merge, output_path, protocol_name)


def combine_layers(experiment):
    """Iterate through protocols to combine layers."""
    input_path = get_data_folder(experiment, 'Zeek', "2_Preprocessed")
    output_path = get_data_folder(experiment, 'Zeek', "2_Preprocessed")

    combinations = {"tcp": ["http", "ssh", "ssl", "ftp"], "udp": ["dns"]}

    for network_protocol, application_list in combinations.items():
        print_progress(experiment, "2_Preprocessed", network_protocol.upper())

        file_path_n = input_path + network_protocol + '.csv'
        if os.path.exists(file_path_n):
            df_n = read_preprocessed(file_path_n)
            df_n = df_n.drop(["ts", "ts_", "duration"] +
                             [c for c in df_n.columns if "service" in c], 1)

            for app_proto in application_list:
                print_progress(experiment, "2_Preprocessed",
                               app_proto.upper())
                file_path_a = input_path + app_proto + '.csv'
                if os.path.exists(file_path_a):
                    df_a = read_preprocessed(file_path_a)

                    process_merge(df_n, df_a, app_proto + "-" +
                                  network_protocol, output_path)


if __name__ == "__main__":
    # combine_layers("UNSW-NB15")
    # combine_layers("ISCX-IDS-2012")
    combine_layers("CIC-IDS-2017")
    # combine_layers("CIC-IDS-2018")
    print("Done")
