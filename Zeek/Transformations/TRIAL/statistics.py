

NO_FEATURE_COLS = ["uid","Label","ts","ts_","id.orig_h","id.resp_h","id.orig_p","id.resp_p"]


def statistics_cols(df, filename):
    features = [c for c in df.columns if not c in NO_FEATURE_COLS ]
    if "conn" in filename :
        adjust_cols =  [c for c in features if (("bytes" in c) | ("pkts" in c))] #Need to check this, but this seems oke!
        max_cols = [c for c in features if ( ("bytes" in c) | ("pkts" in c) | ("bpp" in c) )] + ["time_active"]
        sum_cols = [c for c in features if c != "duration" ]  + ["time_active"]
    
    return sum_cols, max_cols, adjust_cols


#Example
#from project_paths import get_data_folder
#from BRO.utils import read_preprocessed
#DATASET = "CIC-IDS-2017"
#input_path = get_data_folder(DATASET, "BRO", "3_Aggregated")
#filename = "ssl.csv"
#df = read_preprocessed(input_path + filename)
#statistics_cols(df, filename)
