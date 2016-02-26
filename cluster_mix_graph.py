import networkx as nx

def generate_identification(filename):
    identifcation = {}
    with open(filename) as f:
        for line in f:
            e = line.replace("\n","").rsplit(",")
            identifcation[e[0]] = e[1]
    return identifcation

def generate_a_edges(filename):
    G=nx.Graph()
    with open(filename) as f:
        for line in f:
            e = line.replace("\n","").rsplit(",")
            G.add_edge(e[0],e[1])
    return G

def generate_b_edges(filename):
    G=nx.Graph()
    with open(filename) as f:
        for line in f:
            e = line.replace("\n","").rsplit(",")
            G.add_edge(e[0],e[1],weight=e[2])
    return G

a_graph = generate_a_edges("cluster_data/cc_clusters.csv")
b_graph = generate_b_edges("cluster_data/cluster_similarities.csv")
ids = generate_identification("cluster_data/spectrum_ids.csv")
