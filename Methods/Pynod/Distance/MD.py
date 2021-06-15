import networkx as nx
import numpy as np
import scipy 

''' 
Algorithm:      Modality Distance
                
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
                Assumes that the number of nodes is the same
'''

def md(G, H, weight = None):
    G.add_nodes_from(H.nodes) #This is scetchy
    H.add_nodes_from(G.nodes) #This is scetchy
    
    vec1 = perron_vector(G)
    vec2 = perron_vector(H)
    return np.linalg.norm(vec1-vec2)

def perron_vector(G, weight = None):
    A = nx.adjacency_matrix(G, weight = weight).todense().astype(float)
    val, vec = scipy.sparse.linalg.eigs(A, k=1, which='LM')
    return vec