from BRO.utils import  fix_col_order
import numpy as np

def store_dataframe(output_path, df, file_name, item, labels):
    label_cols = [c for c in df.columns if c in labels]
    df_labels = df[label_cols].fillna(0).astype(bool).astype(int)
    df_labels["BENIGN"] = np.where((df_labels["BENIGN"] == 1) & (df_labels.sum(1) == 1),1,0 )
    
    df["Label"] = df_labels.idxmax(axis=1)
    df = df.drop(label_cols,1)
    
    if (file_name == "tcp" or file_name == "udp"):
        df = _reset_statistics(df)
    df = fix_col_order(df)
    df.to_csv(output_path + file_name + item + ".csv", index=False)
    
def _reset_statistics(df):
    df["PCR"] = (df["orig_bytes"] - df["resp_bytes"]) / (df["orig_bytes"] + df["resp_bytes"]) #Recalculate
    df = df.fillna(0)
    df["orig_bpp"] = np.where(df["orig_pkts"] > 0, df["orig_bytes"] / df["orig_pkts"], 0)
    df["resp_bpp"] = np.where(df["resp_pkts"] > 0, df["resp_bytes"] / df["resp_pkts"], 0)
    return df