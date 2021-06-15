import numpy as np

''' 
Algorithm:      Entropy Distance
                
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

def ed(G, H, weight = None):
    E_H = entropy_edges(H, weight)
    E_G = entropy_edges(G, weight)
    return np.abs(E_H - E_G) / max(E_H,E_G)  #This is new
    
def entropy_edges(G, weight = None):
    if weight == None:
        w_sum = G.size()
    else:
        w_sum = G.size(weight = weight)
        
    entr = 0
    for u,v in G.edges():
        if weight == None:
            w_ = 1 / w_sum
        else:
            w_ = G.get_edge_data(u,v)[weight] / w_sum
        
        if w_ > 0:
            entr = entr + (w_ * np.log(1 / w_)) #This is changed
    return entr        
            
