import networkx as nx

#https://stackoverflow.com/questions/43108481/maximum-common-subgraph-in-a-directed-graph
def maximum_common_subgraph(G, H):
    matching_graph=nx.Graph()
    
    for u,v, attr in H.edges(data=True):
        if G.has_edge(u,v) :
            matching_graph.add_edge(u, v, weight = 1)
    
    graphs = [matching_graph.subgraph(c) for c in nx.connected_components(matching_graph)]

    mcs_length = 0
    mcs_graph  = nx.Graph()
    for i, graph in enumerate(graphs):
        if len(graph.nodes()) > mcs_length:
            mcs_length = len(graph.nodes())
            mcs_graph = graph
    return mcs_graph

def get_weight(G, u, v, weight = None):
    w = 0
    if G.has_edge(u,v):
        if weight == None:
            w = 1
        else:
            w = G.get_edge_data(u,v)[weight]
    return w