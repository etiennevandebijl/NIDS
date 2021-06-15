from project_paths import get_results_folder
import warnings; warnings.filterwarnings("ignore")
import pandas as pd
import glob

COLUMNS = ["TCP","UDP","DNS","HTTP","FTP","SSH","SSL"]

DATASET = "CIC-IDS-2017"
VERSION = "5_Graph"
input_path = get_results_folder(DATASET, "BRO", VERSION, "")      

files_glob = [f for f in glob.glob(input_path + "**/metric_comparison.csv", recursive = True)]

file_info = []
for f in files_glob:
    tags = f.split("\\")
    protocol = tags[1]
    time = tags[2]
    delta = tags[3]
    file_info.append([protocol, time, delta, f])
df_files = pd.DataFrame(file_info, columns = ["Protocol","Time","Delta","Path"])

# =============================================================================
# ALL
# =============================================================================
time = "60min"
delta = "Delta1"

df_select = df_files[df_files["Time"] == time]
df_select = df_select[df_select["Delta"] == delta]

df_list = []
stats = {}
stats_P = {}

score = "F1_score-id-P"
for p, group in df_select.groupby(["Protocol"]):
    pd_list = []
    for index, row in group.iterrows():
        df = pd.read_csv(row["Path"], sep = ";", decimal = ",").fillna(0)
        pd_list.append(df)
    
    if len(pd_list) > 0:
        df_p = pd.concat(pd_list)        
        df_p["Anomaly Ratio"] = df_p["P"]/df_p["n"]       
        df_p = df_p[["Metric",score,"Anomaly Ratio","Baseline","P","n"]]
        df_p = df_p[~df_p["Metric"].str.contains("Weight")]
        df_p.index = df_p["Metric"]
        stats_P[p] = df_p[["Anomaly Ratio","Baseline","P","n"]].mean()
        stats[p] = df_p.drop(["Metric"],1)

pd_list = []
protocols = []
for proto, df in stats.items():
    protocols.append(proto)
    pd_list.append(df[score])
df_new = pd.concat(pd_list,1)
df_new.columns = [c.upper() for c in protocols]
df_new = df_new[[c for c in COLUMNS if c in df_new.columns]]
df_new = df_new.round(5)

df_new["Metrics"] = [m.split("-",1)[0] for m in df_new.index.values]
df_new["Weight"] = [m.split("-",1)[1]  if "-" in m else "" for m in df_new.index.values]

df_unweighted = df_new[df_new["Weight"]==""]
df_unweighted = df_unweighted.drop(["Metrics","Weight"],1)
df_weighted = df_new[df_new["Weight"]!=""]
df_weighted = df_weighted.sort_values(["Metrics","Weight"])
df_weighted.index = df_weighted["Metrics"]
df_weighted = df_weighted[["Weight"] + COLUMNS]


df_stats = pd.DataFrame(stats_P)
df_stats.columns = [c.upper() for c in protocols]
df_stats = df_stats[[c for c in COLUMNS if c in df_stats.columns]]
df_stats = df_stats.round(5)

