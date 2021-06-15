from project_paths import get_data_folder
from BRO.network import transform_to_one_ipv4
from BRO.utils import read_preprocessed
import warnings; warnings.filterwarnings("ignore")
import pandas as pd
import glob

from BRO.Discretization.time import time_iterator
from BRO.Discretization.output import store_dataframe

#def remove_host_IP(df, dataset):
#    local = get_local_IPS(dataset)
#    print(len(df["id.resp_h"].unique()))
#    df["id.resp_h"] = np.where(df["id.resp_h"].isin(local),df["id.resp_h"],df["id.resp_h"].str.rpartition('.')[0].str.rpartition('.')[0])
#    df["id.orig_h"] = np.where(df["id.orig_h"].isin(local),df["id.orig_h"],df["id.orig_h"].str.rpartition('.')[0].str.rpartition('.')[0])
#    print(len(df["id.resp_h"].unique()))
#    return df

def discretize_bro_files(input_path, output_path):
    files = [f for f in glob.glob(input_path + "**/tcp.csv", recursive=True)]
    
    for fi in files:
        file_name = fi.split("\\")[-1].replace(".csv",""); print(file_name)
        
        df = read_preprocessed(fi)
        df = transform_to_one_ipv4(df, DATASET)
       # df = remove_host_IP(df, DATASET)
        
        labels = df["Label"].unique().tolist()
        
        grouped_dates = df.groupby(df["ts"].dt.date)

        pd_edges_list = []
        for date, df_date in grouped_dates:
            df_edge = time_iterator(df_date)
            pd_edges_list.append(df_edge)
        df_edges = pd.concat(pd_edges_list)
        store_dataframe(output_path, df_edges, file_name, "_edge", labels)
        #return df_edges

# =============================================================================
# The fun part is here
# =============================================================================
DATASET = "CIC-IDS-2017"
input_path = get_data_folder(DATASET, "BRO", "3_Aggregated")
output_path = get_data_folder(DATASET, "BRO", "4_Discretized")
df_edges = discretize_bro_files(input_path, output_path)







