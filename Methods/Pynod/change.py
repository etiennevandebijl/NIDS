# -*- coding: utf-8 -*-

import pandas as pd
from tqdm import tqdm
import networkx as nx
import numpy as np

from Methods.Pynod.Distance.MCSED import mcsed
from Methods.Pynod.Distance.MCSVD import mcsvd
from Methods.Pynod.Distance.VEO import veo
from Methods.Pynod.Distance.NED import ned

from Methods.Pynod.Distance.MCSWD import mcswd
from Methods.Pynod.Distance.WD import wd
from Methods.Pynod.Distance.ED import ed
from Methods.Pynod.Distance.UD import ud

no_weight_dist_functions = {"MCSED": mcsed, "MCSVD":  mcsvd, "NED": ned, "VEO": veo} 
#NETSIMILE, GD, DELTACON
weighted_dist_functions = {"WD": wd, "ED": ed, "UD": ud, "MCSWD": mcswd}
#SD and MD
    
def distance_graphs(G, H, function_dict, weigthed = False, weight = None):
    dist_dict = {}
    
    for name, func in function_dict.items():
        if max(G.number_of_edges(), H.number_of_edges()) == 0:
            if weigthed:
                dist_dict[name + "-" + weight] = 0
            else:
                dist_dict[name] = 0                
        else:
            if weigthed:
                dist_dict[name + "-"  + weight] = func(G, H, weight)
            else:
                dist_dict[name] = func(G, H)
    return dist_dict

def graphs_time(df, weights, freq):
    ts_list = []
    G_list = []
    labels = []

    for _, df_day in df.groupby([df["ts"].dt.date]):
        t_start = df_day["ts"].dt.round("min").min()
        t_end = df_day["ts"].dt.round("min").max()
        epochs = pd.date_range(t_start, t_end, freq=freq)

        for ts in epochs:
            df_day_ts = df_day[df_day["ts"] == ts]

            if df_day_ts.shape[0] > 0:
                labels.append(df_day_ts["Label"].any())
                G_i = nx.from_pandas_edgelist(df_day_ts, 'Source', 'Target',
                                              edge_attr=weights, create_using=nx.DiGraph())
            else:
                labels.append(False)
                G_i = nx.Graph()
            G_list.append(G_i)
            ts_list.append(ts)
    return ts_list, G_list, labels

def distances_Event_Change(df, delta, freq, weighted=False):
    weights = [w for w in df.columns.tolist() if not w in ["Source", "Target",
                                                           "ts", "Label"]]
    ts_list, G_list, labels = graphs_time(df, weights, freq)
    
    d_list = []

    for j in tqdm(range(1, len(G_list))):
        dist_list = []
        for i in range(max(j-delta, 0), j+1):
            G = G_list[i]
            H = G_list[j]

            dist = {}
            if not weighted:
                dist = distance_graphs(G, H, no_weight_dist_functions)
            else:
                for w in weights:
                    dist_w = distance_graphs(G, H, weighted_dist_functions, 
                                                  True, w)
                    dist = {**dist, **dist_w}
            dist_list.append(dist)
        
        dist_list_j = pd.DataFrame(dist_list).mean(0).to_frame().T
        d_list.append(dist_list_j)
    labels = np.array([int(i) for i in labels[1:]]) #move 1 to the right as we want to label the transition
    ts_list = ts_list[1:]
    return ts_list, pd.concat(d_list), labels







