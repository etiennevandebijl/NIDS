from Methods.Pynod.Distance.utils import maximum_common_subgraph
from Methods.Pynod.Distance.WD import wd

''' 
Algorithm:      MCS Weight Distance
                
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

def mcswd(G, H, weight = None):
    MCS = maximum_common_subgraph(G,H)
    remove_G = [e for e in G.edges if not e in MCS.edges] #remove edges which are not in MCS
    remove_H = [e for e in H.edges if not e in MCS.edges] #remove edges which are not in MCS
    G_ = G.copy()
    H_ = H.copy()
    G_.remove_edges_from(remove_G)
    H_.remove_edges_from(remove_H)
    return wd(G_, H_, weight)
    
