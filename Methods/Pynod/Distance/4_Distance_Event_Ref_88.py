from paths_data import *
from graph_distance_functions import *
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

paths_vertices = paths_df[((paths_df["Analyser"]=="BRO_ZEEK") & (paths_df["File"].str.contains("vertices")))]["Path"].values
paths_edges = paths_df[((paths_df["Analyser"]=="BRO_ZEEK") & (paths_df["File"].str.contains("edges")))]["Path"].values

functions_unweight_undir = {"MCS_Edge_Distance":MCS_Edge_Distance,
                            "MCS_Vertex_Distance":MCS_Vertex_Distance,
                            "Graph_Edit_Distance":Graph_Edit_Distance,
                            "Modality_Distance":Modality_Distance,
                            "Diameter_Distance":Diameter_Distance,
                            "VEO_Overlap":VEO_Overlap,
                            "DeltaCON":DeltaCON}


def undirected_unweighted_network_measures(G, H):
    G = G.to_undirected()
    H = H.to_undirected()
    stats = dict()
    for measure,fn in functions_unweight_undir.items():
        d_GH = fn(G,H)
        stats[measure] = d_GH
    return stats

functions_weight_undir =  {"Weight_Distance":Weight_Distance,
                           "Entropy_Distance":Entropy_Distance,
                           "Umeyama_distance":Umeyama_Distance,
                           "MCS_Weight_Distance":MCS_Weight_Distance}

def undirected_weighted_network_measures(G, H, w):
    G = G.to_undirected()
    H = H.to_undirected()
    stats = dict()
    for measure,fn in functions_weight_undir.items():
        d_GH = fn(G,H,w)
        stats[measure] = d_GH
    return stats

functions_weight_dir = {"Vector_Similarity":Vector_Similarity}

def directed_weighted_network_measures(G, H, w):
    stats = dict()
    for measure,fn in functions_weight_dir.items():
        d_GH = fn(G,H,w)
        stats[measure] = d_GH
    return stats

def construct_graph(df_edges, t, nodes, w):
    df_edges = df_edges[df_edges["t"]==t]
    G = nx.from_pandas_edgelist(df_edges, 'Source', 'Target', [w], create_using=nx.DiGraph())
    G.add_nodes_from(nodes)
    return G

def graph_difference_iterator(df_edges, df_nodes, weight):
    nodes = df_nodes["ID"].unique().tolist() + ["Internet"] #Need to check this
    times = list(df_edges.sort_values(["t"])["t"].unique())       
    
    G_current = construct_graph(df_edges, times[0], nodes, weight) 
    
    data = []
    for t in range(1,len(times)): 
        G_next = construct_graph(df_edges, times[t], nodes, weight) 
        
        instance = dict()
        instance["t"] = times[t]

        dist = undirected_unweighted_network_measures(G_current, G_next)
        instance.update(dist)     
        
        dist = undirected_weighted_network_measures(G_current, G_next, weight)
        instance.update(dist)     
        
        dist = directed_weighted_network_measures(G_current, G_next, weight)
        instance.update(dist)     

        data.append(instance)
        
        G_current = G_next
    return data

def read_path(path):
    df = pd.read_csv(path)
    df["t"] = pd.to_datetime(df["t"])   
    return df

def main():
    files = len(paths_vertices)
    for i in range(files):
        df_nodes = read_path(paths_vertices[i])
        df_edges = read_path(paths_edges[i])

        results = graph_difference_iterator(df_edges, df_nodes, "orig_bytes")
    
        df_results = pd.DataFrame(results)
        df_results.to_csv(paths_edges[i].replace("_edges","_Distance_Event"), index=False)

main()






