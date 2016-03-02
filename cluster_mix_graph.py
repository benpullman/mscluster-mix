import networkx as nx
import sys
from collections import Counter

class Cluster:
    def __init__(self,a_edges,b_edges):
        self.a_edges = a_edges
        self.b_edges = b_edges

def generate_identification(filename):
    identifcation = {}
    cluster_number = {}
    with open(filename) as f:
        for line in f:
            e = line.replace("\n","").rsplit(",")
            identifcation[e[0]] = e[1]
            cluster_number[e[0]] = int(e[2])
    return identifcation, cluster_number

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

def cc_weights(cc):
    weights = []
    for e in cc.edges():
        edge_weight = float(cc[e[0]][e[1]]['weight'])
        if edge_weight < 1:
            weights.append(edge_weight)
    return weights

def avg_cc_weight(cc):
    weights = cc_weights(cc)
    weight_result = 0
    try:
        weight_result = sum(weights)/len(weights)
    except:
        pass
    return weight_result

def cluster_ids(cc,ids):
    id_set = []
    for n in cc.nodes():
        try:
            id_set.append(ids[n])
        except:
            pass
    return {s for s in id_set}

def mix(cc,ids):
    c_ids = cluster_ids(cc,ids)
    if 'PEPTIDE' in c_ids:
        return len(c_ids) > 2
    else:
        return len(c_ids) > 1

def an_id(cc,ids):
    c_ids = cluster_ids(cc,ids)
    if 'PEPTIDE' in c_ids:
        return len(c_ids)>1
    else:
        return True

def all_id(cc,ids):
    c_ids = cluster_ids(cc,ids)
    return not 'PEPTIDE' in c_ids

# def link_edges(a_clusters,b_clusters):
#     clusters = [];


def seperate_mixtures(graph):
    mix_graphs = {}
    m = 0
    s = 0
    p = 0
    sp = 0
    e = 0
    for cluster in nx.connected_component_subgraphs(graph):
        clust = cluster_ids(cluster,ids)
        if len(clust)==1 and 'PEPTIDE' in clust:
            s += 1
        elif len(clust)==1 and not 'PEPTIDE' in clust:
            p += 1
        elif len(clust)==2 and 'PEPTIDE' in clust:
            sp += 1
        elif mix(cluster,ids):
            key = [n for n in sorted(cluster.nodes())][0]
            mix_graphs[key] = cluster
            m += 1
            # if avg_cc_weight(cluster) < .7:
            #     for edge in cluster.edges():
            #         print(edge[0] + " " + edge[1] + ": " + cluster[edge[0]][edge[1]]['weight'])
        else:
            e += 1
    # print("Not id'd: " + str(s))
    # print("Mixtures: " + str(m))
    # print("Pure: " + str(p))
    # print("Maybe pure: " + str(sp))
    # print("Error: " + str(e))
    return mix_graphs

def split_cluster(a_graph,b_graph,e1,e2):
    new_b_graphs=nx.Graph()
    a_graph.remove_edge(e1,e2)
    a_graph.remove_edge(e2,e1)
    new_a_graphs = nx.connected_component_subgraphs(a_graph)
    for a in new_a_graphs:
        for n1 in a:
            for n2 in a:
                if n1 != n2:
                    new_b_graphs.add_edge(n1,n2,weight=b_graph[n1][n2]['weight'])
    return nx.connected_component_subgraphs(new_b_graphs), nx.connected_component_subgraphs(new_a_graphs)


a_graph = generate_a_edges(sys.argv[1])
b_graph = generate_b_edges(sys.argv[2])
ids, cluster_number = generate_identification(sys.argv[3])


# for n in a_graph.nodes():
#     try:
#         m += 1
#         print(ids[n])
#     except:
#         s += 1



mixture_a = seperate_mixtures(a_graph)
mixture_b = seperate_mixtures(b_graph)

for a in mixture_a:
    for n in mixture_a[a].nodes():
        try:
            print(cluster_number[n])
        except:
            pass
    print("----")
# print(ids)
