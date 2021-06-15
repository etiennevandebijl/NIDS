import networkx as nx
import numpy as np

''' 
Title:              Anomaly Detection in Time Series of Grpahs using ARMA Processes
Author:             Brandom Pincombe
Year:               2005
url article:        http://www.asor.org.au/publication/files/dec2005/Bra-paper.pdf

Title:              Using graph diameter for change detection in dynamic networks
Authors:            M.E. Gaston, M. Kraetzl and W.D. Wallis
Year:               2006
url article:        https://pdfs.semanticscholar.org/5de5/2a2457272fc0e6af64b45c821129160f54e9.pdf
Journal             Australasian journal of combinatorics

Graph Support
Direct:             No  (connected_component_subgraphs not possible for directed graphs)
Indirect:           Yes
Unweighted Edges:   Yes
Weighted Edges:     Yes

Assumptions:
                    The diameter function requires the network to be strongly connected.                

Notes:
1)  Not only the difference can be calculated between the graphs, diameter D can also be used as robustness of the graph. 
2)  Both weighted and unweighted should work here. When unweighted, it looks at difference in network topology and if weighted
    it looks at change in edge traffic. 
3)  Here we take the average of all eccentricities instead of the maximum. This is also an option.
'''

def gd(G, H, weight = None):
    D_G = graph_diameter(G, weight)
    D_H = graph_diameter(H, weight)
    diff = np.absolute(D_G - D_H)
    return diff

def graph_diameter(G, weight = None):
    diam = 0    
    graphs = list(nx.connected_component_subgraphs(G.to_undirected())) #Not possible for directed graphs
    for i, graph in enumerate(graphs):
        if len(graph.nodes) > 1:
           for v in graph.nodes():
               if weight == None:
                   diam = diam + nx.eccentricity(graph,v)
               else:
                   diam = diam + nx.eccentricity(graph,v, sp=nx.single_source_dijkstra_path_length(weight=weight))
    return diam / G.number_of_nodes()

