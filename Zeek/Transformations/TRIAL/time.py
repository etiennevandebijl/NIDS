import pandas as pd; from tqdm import tqdm 
from BRO.Discretization.edge import edge_iterator
import warnings; warnings.filterwarnings("ignore")

def _percentage_active(df, start, end):
    df.loc[df['ts_'] > end, 'ts_'] = end
    df["time_active"] = (df["ts_"] - df["ts"])
    df.loc[df['ts'] < start, 'ts'] = start
    df["pct_act"] = (df["ts_"] - df["ts"]).values / df["duration"].values
    df["pct_act"] = df["pct_act"].fillna(value=1)
    
    adjust_cols = [c for c in df.columns if "bytes" in c or "pkts" in c]
    df[adjust_cols].multiply(df["pct_act"], axis="index")
    return df.drop(["pct_act"],1)

def time_iterator(df):
    t_start = df["ts"].dt.round("min").min()
    t_end =  df["ts"].dt.round("min").max()
    time_epochs = pd.date_range(t_start, t_end, freq = "1min")
    
    pd_list_df_edges = []
    for i in tqdm(range(len(time_epochs)-1)):
        t_i = time_epochs[i]; t_j = time_epochs[i+1]
        
        if "ts_" in df.columns:
            df_t_i = df[(( df["ts_"] > t_i) & (df["ts"]<= t_j))] 
            
            if "bytes" in df.columns: 
                df_t_i = _percentage_active(df_t_i, t_i, t_j)
        else:
            df_t_i = df[(( df["ts"] > t_i) & (df["ts"]<= t_j))] 
        
        if df_t_i.shape[0] > 0:
            df_t_i_edge = edge_iterator(df_t_i, t_i)
            pd_list_df_edges.append(df_t_i_edge)
    return pd.concat(pd_list_df_edges)

# Example
#from project_paths import get_data_folder
#from BRO.utils import read_preprocessed
#DATASET = "CIC-IDS-2017"
#input_path = get_data_folder(DATASET, "BRO", "2_Preprocessed")
#df = read_preprocessed(input_path + "Friday-WorkingHours/ftp.csv")

#df_new = time_iterator(df)



