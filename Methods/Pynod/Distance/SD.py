import networkx as nx
import numpy as np
import scipy 

''' 
Algorithm:      Spectral Distance
                
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
                k must be smaller than the number of nodes
'''

def sd(G, H, weight = None, k = 20):
    
    if k > max(G.number_of_nodes(),H.number_of_nodes()) - 1:
        k = max(G.number_of_nodes(),H.number_of_nodes()) - 1
        print("K to large")
    
    eigenvalues_G = laplace_matrix_eigenvalues(G, weight, k)
    eigenvalues_H = laplace_matrix_eigenvalues(H, weight, k)
    d = np.sum((eigenvalues_G - eigenvalues_H)**2) / min(np.sum(eigenvalues_G**2),np.sum(eigenvalues_H**2))
    return np.sqrt(d)

def laplace_matrix_eigenvalues(G, weight = None, k = 20):
    A = nx.adjacency_matrix(G, weight = weight).todense().astype(float)
    D = np.identity(A.shape[0]) * A.sum(1)
    L = D - A
    eigenvalues, eigenvectors = scipy.sparse.linalg.eigs(L, k=k, which='LM')
    return eigenvalues
