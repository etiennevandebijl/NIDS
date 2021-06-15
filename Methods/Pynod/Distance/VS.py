import networkx as nx
import numpy as np

''' 
Algorithm:      Vertex/Edge Vector Similarity 
                
Title:          Web graph similarity for anomaly detection
Authors:        Panagiotis Papadimitriou, Ali Dasdan and Hector Garcia-Molina
Year:           2010
url article:    https://link.springer.com/content/pdf/10.1007/s13174-010-0003-x.pdf

Graph support:
Directed:       Yes
Undirected:     Yes
Weighted:       Yes
Unweighted:     Yes

Assumptions:
                None
'''

def vs(G, H, weight):
    #Expects G and H are of class DiGraph
    F = nx.compose(G,H)
    q = q_u(F,G,H)
    amax = -np.inf
    d = 0
    for u,v in F.edges():
        g1 = gamma(G, u, v, q, weight)
        g2 = gamma(H, u, v, q, weight)
        amax = max(amax,g1,g2)
        d += np.abs(g1-g2)
    sim_VS = 1 - (d / amax) / F.number_of_edges()
    return sim_VS
     
def gamma(G, u, v, q, w):
    #Expects G is of class DiGraph
    if not G.has_edge(u,v):
        return 0
    if G[u][v][w] == 0:
        return 0
    gamma = q[u] * G[u][v][w] / G.out_degree(weight=w)[u]
    return gamma

def q_u(F,G,H):
    #To figure out
    q = dict()
    for u in F.nodes():
        q[u] = 1
    return q




