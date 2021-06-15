import networkx as nx

''' 
Algorithm:      Vertex/Edge Overlap 
                
Title:          Web graph similarity for anomaly detection
Authors:        Panagiotis Papadimitriou, Ali Dasdan and Hector Garcia-Molina
Year:           2010
url article:    https://link.springer.com/content/pdf/10.1007/s13174-010-0003-x.pdf

Graph support:
Directed:       Yes
Undirected:     Yes
Weighted:       No (not taken into account)
Unweighted:     Yes

Assumptions:
                None
'''

def veo(G,H):
    F = nx.compose(G,H) #This is G union F
    n_G, n_H, n_F = G.number_of_nodes(), H.number_of_nodes(), F.number_of_nodes()
    m_G, m_H, m_F = G.number_of_edges(), H.number_of_edges(), F.number_of_edges()
    sim_VEO = 2 * ( (n_G + n_H - n_F) + (m_G + m_H - m_F) )  / (n_G + n_H + m_G + m_H)
    return 1 - sim_VEO