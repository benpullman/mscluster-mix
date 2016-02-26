import networkx as nx
import sys

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

a_graph = generate_a_edges(sys.argv[1])
b_graph = generate_b_edges(sys.argv[2])
ids = generate_identification(sys.argv[3])
