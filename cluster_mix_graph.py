import networkx as nx
import sys
from collections import Counter
import pickle

class Cluster:
    def __init__(self,number,a_graph,b_graph):
        self.number = number
        self.a_graph = a_graph
        self.b_graph = b_graph
    def nodes(self):
        return self.a_graph.nodes()
    def a_edges(self):
        return self.a_graph.edges()
    def b_edges(self):
        return self.b_graph.edges()
    def split_at(self,e1,e2,l):
        try:
            self.a_graph.remove_edge(e1,e2)
        except:
            try:
                self.a_graph.remove_edge(e2,e1)
            except:
                return []
        new_a_graphs = nx.connected_component_subgraphs(self.a_graph)
        new_clusters = []
        for i,a in enumerate(new_a_graphs):
            b = nx.Graph()
            for n1 in a:
                for n2 in a:
                    if n1 != n2:
                        b.add_edge(n1,n2,weight=self.b_graph[n1][n2]['weight'])
                        b.add_edge(n2,n1,weight=self.b_graph[n2][n1]['weight'])
            new_clusters.append(Cluster(str(self.number) + "." + chr(l + i + 97),a,b))
        return new_clusters
    def weight(self):
        return avg_cc_weight(self.b_graph)
    def id_as(self):
        return {ids[n] for n in self.nodes()}
    def lowest_weight(self):
        weight_edges = []
        for e in self.b_edges():
            edge_weight = float(self.b_graph[e[0]][e[1]]['weight'])
            weight_edges.append((edge_weight,e))
        weight_edges.sort(key=lambda x: x[0])
        if len(weight_edges) == 0:
            return 1
        else:
            return weight_edges[0]

def pickle_clusters(clusters,filename = "clusters.p"):
    with open(filename, "wb") as f:
        pickle.dump(clusters,f)

def load_clusters(filename = "clusters.p"):
    clusters = []
    with open(filename, "rb") as f:
        clusters = pickle.load(f)
    return clusters

def pickle_ids(ids,filename = "ids.p"):
    with open(filename, "wb") as f:
        pickle.dump(ids,f)

def load_ids(filename = "ids.p"):
    ids = {}
    with open(filename, "rb") as f:
        ids = pickle.load(f)
    return ids

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
    weight_result = 1
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

def link_edges(a_clusters,b_clusters):
    clusters = []
    for cluster_id in a_clusters:
        try:
            clusters.append(Cluster(cluster_id,a_clusters[cluster_id],b_clusters[cluster_id]))
        except:
            pass
    return clusters


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
            try:
                key = cluster_number[cluster.nodes()[0]]
                mix_graphs[key] = cluster
            except:
                pass
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

clusters = []
try:
    a_graph = generate_a_edges(sys.argv[1])
    b_graph = generate_b_edges(sys.argv[2])
    ids, cluster_number = generate_identification(sys.argv[3])
    mixture_a = seperate_mixtures(a_graph)
    mixture_b = seperate_mixtures(b_graph)
    clusters = link_edges(mixture_a,mixture_b)
    pickle_clusters(clusters)
    pickle_ids(ids)
except:
    clusters = load_clusters()
    ids = load_ids()

# for n in a_graph.nodes():
#     try:
#         m += 1
#         print(ids[n])
#     except:
#         s += 1


c = clusters[10]
# print(c.a_edges())
print(c.lowest_weight())
print(c.id_as())
for cluster in c.split_at(c.a_edges()[0][0], c.a_edges()[0][1]):
    print(cluster.id_as())
    # print(cluster.nodes())
    # print(cluster.b_edges())
    # print(cluster.weight())
    print(cluster.lowest_weight())



# print(ids)
