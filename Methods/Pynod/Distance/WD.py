from Methods.Pynod.Distance.utils import get_weight
import networkx as nx
import numpy as np

''' 
Algorithm:      Weight Distance
                
Title:          Anomaly Detection in Time Series of Graphs using ARMA Processes
Authors:        Brandon Pincombe
Year:           2005
url article:    http://www.asor.org.au/publication/files/dec2005/Bra-paper.pdf

Graph support:
Directed:       Yes
Undirected:     Yes
Weighted:       Yes
Unweighted:     Yes

Assumptions:
                None
'''

def wd(G, H, weight = None): 
    F = nx.compose(G,H)
    if F.number_of_edges() == 0:
        return 0
    d = 0
    for u,v in F.edges():
        w_G = get_weight(G, u, v, weight)
        w_H = get_weight(H, u, v, weight)
        if max(w_G,w_H) > 0:
            d += np.abs(w_G - w_H) / max(w_G,w_H)
    return d /  F.number_of_edges()





