from scipy.stats import skew, kurtosis
from scipy.spatial import distance
import networkx as nx
import numpy as np
import pandas as pd

'''
Title:          NetSimile: A Scalable Approach to Size-Independent Network Similarity
Authors:        Michele Berlingerio, Danai Koutra, Tina Eliassi-Rad, Christos Falousos
Year:           2012
Url article:    http://arxiv.org/pdf/1209.2684.pdf

inspiration code: https://github.com/kristyspatel/Netsimile/blob/master/Netsimile.py

Directed:       Yes
Weighted:       No
Unweighted:     Yes
'''

def netsimile(G,H):
    F_G = get_features(G)
    S_G = aggregator(F_G)    
    F_H = get_features(H)
    S_H = aggregator(F_H)
    return np.abs(distance.canberra(S_G, S_H))

def get_features(G):
    f_G = []
    
    for i in G.nodes():
        d_i = G.degree[i]
        c_i = nx.clustering(G,i)
        
        d_N_i = np.mean([G.degree[j] for j in G.neighbors(i)])
        c_N_i = np.mean([nx.clustering(G,j) for j in G.neighbors(i)])

        egonet_i = nx.ego_graph(G,i)
        m_ego_i = egonet_i.number_of_edges()
        
        eoegoi = 0
        negoi = set()
        for n1, n2 in nx.edge_boundary(G, egonet_i.nodes()):
            eoegoi += 1
            negoi.add(n2)
        negoi = len(negoi)
        f_G.append([d_i,c_i,d_N_i,c_N_i,m_ego_i,eoegoi,negoi])
    return pd.DataFrame(f_G).T.fillna(0)

def aggregator(F_G):
    S_G = []
    for index, feat in F_G.iterrows():
        S_G.append([np.median(feat),np.mean(feat),np.std(feat),kurtosis(feat),skew(feat)])
    if len(S_G) == 0:
        return [0]
    return np.array(S_G).flatten()

#Example
#G = nx.gnp_random_graph(10, 0.2)
#H = nx.gnp_random_graph(8, 0.5)
#netsimile(G,H)


    
    
    
    
    