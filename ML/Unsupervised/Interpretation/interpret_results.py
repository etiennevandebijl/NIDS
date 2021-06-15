from project_paths import get_results_folder
import pandas as pd
import glob

COLUMNS = ["TCP","UDP","DNS","HTTP","FTP","SSH","SSL"]

input_path = get_results_folder("CIC-IDS-2017", "BRO", "3_Downsampled", "Unsupervised")      

# =============================================================================
# Benign vs Malicious
# =============================================================================

pd_list = []
stats_protocol = {}
for fi in glob.glob(input_path + "**/Benign vs Malicious/model_comparison.csv", recursive = True):
    p = fi.split("\\")[1]
    df = pd.read_csv(fi, sep = ";", decimal = ",", index_col = 0).fillna(0)
    intrusion_ratio = (df["P"] / df["n"]).values[0]
    baseline = (2 * df["P"] / (df["P"] + df["n"])).values[0]
    df["Recall-idxmax"] = df["Recall-idxmax"] / df["n"]
    df = df[["Recall-idxmax","F1_score-max","F1_score-id-P"]]
    df["Protocol"] = p.upper()
    pd_list.append(df)
    stats_protocol[p] = [intrusion_ratio,baseline]
    
df_stats = pd.DataFrame(stats_protocol)
df_stats.index = ["Intrusion Ratio","Baseline"]
df_scores = pd.concat(pd_list)

F1_max     = pd.pivot(df_scores, columns = "Protocol", values = "F1_score-max")

F1_P        = pd.pivot(df_scores, columns = "Protocol", values = "F1_score-id-P")
F1_P        = F1_P[[c for c in COLUMNS if c in F1_P]]

Recall_100 = pd.pivot(df_scores, columns = "Protocol", values = "Recall-idxmax")
Recall_100 = Recall_100[[c for c in COLUMNS if c in Recall_100]]
Recall_100 = (Recall_100 * 100).round(3).astype(str)  + "%"










