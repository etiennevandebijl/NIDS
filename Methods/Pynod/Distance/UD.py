from Methods.Pynod.Distance.utils import get_weight
import networkx as nx
import numpy as np

''' 
Algorithm:      Umeyama Distance
                
Title:          Novel Approaches in Modelling Dynamics of Networked Surveillance Environment
Authors:        P. Dickinson and M. Kraetzl
Year:           2003
url article:    https://sci-hub.tw/10.1109/ICIF.2003.177461

Graph support:
Directed:       Yes
Undirected:     Yes
Weighted:       Yes
Unweighted:     Yes

Assumptions:
                None
'''

def ud(G, H, weight = None):
    F = nx.compose(G,H)
    d = 0
    for u,v in F.edges():
        w_G = get_weight(G, u, v, weight)
        w_H = get_weight(H, u, v, weight)
        d += (w_G - w_H)**2
    return d




   