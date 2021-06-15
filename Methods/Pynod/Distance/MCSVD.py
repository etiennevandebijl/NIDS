from Methods.Pynod.Distance.utils import maximum_common_subgraph

''' 
Algorithm:      MSC Vector Distance
                
Title:          Anomaly Detection in Time Series of Graphs using ARMA Processes
Authors:        Brandon Pincombe
Year:           2005
url article:    http://www.asor.org.au/publication/files/dec2005/Bra-paper.pdf

Graph support:
Directed:       Yes
Undirected:     Yes
Weighted:       No
Unweighted:     Yes

Assumptions:
                None
'''

def mcsvd(G, H):
    MCS = maximum_common_subgraph(G,H)
    d = 1 - (MCS.number_of_nodes() / max(G.number_of_nodes(),H.number_of_nodes()) )
    return d