from BRO.learning_utils import format_ML
import numpy as np
import pandas as pd

def edge_iterator(df, timestamp):

    grouped_by_edge = df.groupby(['id.orig_h', 'id.resp_h'])

    results = []
    for edge, group in grouped_by_edge:
        
        edge_aggr_stats = dict({"id.orig_h":edge[0],"id.resp_h":edge[1],"ts":timestamp,"count":group.shape[0]})
        
        X, _, feature_names, _ = format_ML(group, mc = False)
        
        sum_dict = dict(zip([c for c in feature_names], np.sum(X, axis = 0)))
        #min_dict = dict(zip([c+"_min" for c in feature_names], np.min(X, axis = 0)))
        #max_dict = dict(zip([c+"_max" for c in feature_names], np.max(X, axis = 0)))
        
        edge_aggr_stats.update(sum_dict)
        #edge_aggr_stats.update(min_dict)
        #edge_aggr_stats.update(max_dict)
        
        label_dict = group.Label.value_counts().to_dict()
        edge_aggr_stats.update(label_dict)   
        
        results.append(edge_aggr_stats)
    return pd.DataFrame(results)

#Example
#from project_paths import get_data_folder
#from BRO.utils import read_preprocessed
#DATASET = "CIC-IDS-2017"
#input_path = get_data_folder(DATASET, "BRO", "2_Preprocessed")
#df = read_preprocessed(input_path + "Friday-WorkingHours/tcp.csv")

#edge_df = edge_iterator(df, "ja")
