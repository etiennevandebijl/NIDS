import networkx as nx
import numpy as np

'''
Algorithm:          DeltaCon

Title:              DeltaCon: A Principled Massive-Graph Similarity Function
Authors:            Danai Koutra, Joshue T. Vogelstein and Christos Faloutsos
Year:               2013
Url article:        https://arxiv.org/pdf/1304.4657.pdf

Graph Support
Direct:             Yes
Indirect:           Yes
Unweighted Edges:   Yes
Weighted Edges:     Yes

Assumptions:
                    This method assumes that the same nodes exists in both G and H
'''

def deltacon(G,H):
    G.add_nodes_from(H.nodes) #This is scetchy
    H.add_nodes_from(G.nodes) #This is scetchy
    
    S_G = FaBP(G)
    S_H = FaBP(H)
    sim = 1 / (1 + np.linalg.norm(S_G - S_H))
    return sim

def FaBP(G):
    A = nx.adjacency_matrix(G).todense().astype(float)
    D = np.diagflat(A.sum(axis= 1))
    
    eps = 1 / (1 + np.amax(np.array(D)))
    
    L = eps**2 * D - eps* A
    
    I = np.identity(A.shape[0])   
    S = np.linalg.inv(I + L)  
    return S


