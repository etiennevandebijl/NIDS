import networkx as nx

'''
Algorithm:      Network Edit distance

Title:          Detection of abnormal change in dynamic networks
Authors:        Peter Shoubridge, Miro Kraetzl and David Ray
Year:           1999
url:            https://sci-hub.tw/10.1109/IDC.1999.754216

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

def ned(G, H):
    F = nx.compose(G,H)
    n_G, n_H, n_F = G.number_of_nodes(), H.number_of_nodes(), F.number_of_nodes()
    m_G, m_H, m_F = G.number_of_edges(), H.number_of_edges(), F.number_of_edges()
    return (2 * n_F - n_G - n_H) + (2 * m_F - m_G - m_H)
