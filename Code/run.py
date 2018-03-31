#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from pymongo import MongoClient
import numpy as np
import random
import algorithms
from modularity_graph import *
from clique_graph import *
import plotting
import json
import IO
import time
import copy

np.set_printoptions(threshold=np.inf)

# Connect to mongodb to get the citation network
client = MongoClient()

db = client.aps_ml
network = db["tot_network"]

# Modularity Maximization clustering algorithms
print "###############################################################"
print "Modularity Maximization Clustering Algorithms for 2000 articles"

t0 = time.time()
graph = ModularityGraph(network, test=True)

#initialization of the hyperparameter list
N_list = [900, 800, 700, 600, 500, 400, 300, 200, 100, 50]

#initialization of measurements
modularity_score = [0 for i in N_list]
cluster_number = [0 for i in N_list]
cluster_labels = [[] for i in N_list]
node_labels = [[] for i in N_list]
cluster_edges = [[] for i in N_list]
cluster_sizes = [[] for i in N_list]
adjacent_matrix = [{} for i in N_list]

for i in range(len(N_list)):
    n_clus = algorithms.modularity_clustering(graph, num_clusters=N_list[i])

    modularity_score[i] = graph.modularity()
    print "Cluster Number:", n_clus, ", Modularity is:", modularity_score[i]
    cluster_number[i] = n_clus

    indices= [0 for j in range(graph.n_nodes())]
    index = 0
    for c in range(graph.n_nodes()):
        if graph.clusters[c]["is_empty"]==False:
            cluster_labels[i].append(graph.clusters[c]["name"])
            cluster_sizes[i].append(len(graph.clusters[c]["nodes"]))
            cluster_edges[i].append(graph.edge_number[c])
            indices[c] = index
            index += 1

    node_labels[i] = np.copy(graph.node_labels)
    for u, v in graph.cluster_links:
        adjacent_matrix[i][(indices[u], indices[v])] = graph.inter_edge_matrix[u, v]

opt = np.argmax(np.array(modularity_score))

t1 = time.time()
total = t1-t0
print "Computational Time for Modularity Maximization: ", total

print "Printing and Saving Results..."
plotting.plot_line(N_list, modularity_score)
plotting.plot_histogram(cluster_sizes[opt], methodname="Modularity_Maximization")

result = {"Modularity": modularity_score[opt], "Cluster Number": cluster_number[opt], "Cluster Sizes": cluster_sizes[opt], "Cluster Names":
        cluster_labels[opt], "Node Labels": node_labels[opt], "Cluster Edge Sizes": cluster_edges[opt], "Adjacent Matrix": adjacent_matrix[opt]}
IO.SaveDict("./Data/test_2000/Modularity_Maximization_Results.txt", "w", result)

with open("./Data/test_2000/article_labels.csv", "w") as writer:
    writer.write("article_doi,group\n")
    for i in graph.id_to_article:
        writer.write(graph.id_to_article[i]+","+str(node_labels[opt][i])+"\n")

with open("./Data/test_2000/links.csv", "w") as writer:
    writer.write("citing_doi,cited_doi\n")
    for i,j in graph.links:
        writer.write(graph.id_to_article[i]+","+graph.id_to_article[j]+"\n")

# Non-binary Hierarchical clustering algorithms
print "###############################################################"
print "Non-binary Hierarchical Clustering Algorithms for 2000 articles"

t0 = time.time()

#initialization of the hyperparameter list
beta_list = [0.1, 0.3, 0.5, 0.7, 0.9]
hierarchy_list = [1, 2, 3, 4, 5]

#initialization of measurements
modularity_score = [0 for i in beta_list]
cluster_number = [0 for i in beta_list]
cluster_labels = [[] for i in beta_list]
node_labels = [[] for i in beta_list]
cluster_edges = [[] for i in beta_list]
cluster_sizes = [[] for i in beta_list]
adjacent_matrix = [[] for i in beta_list]

for i in range(len(beta_list)):
    graph = CliqueGraph(network, beta=beta_list[i], test=True)

    modularity = [0 for h in hierarchy_list]
    for j in range(len(hierarchy_list)):
        algorithms.clique_clustering(graph, max_hierarchy=hierarchy_list[j])
        modularity[j] = graph.modularity()

    opt = np.argmax(np.array(modularity))  
    graph = CliqueGraph(network, beta=beta_list[i], test=True)
    algorithms.clique_clustering(graph, max_hierarchy=hierarchy_list[opt])

    modularity_score[i] = graph.modularity()
    print "Beta:", beta_list[i], ", Hierarchy level: ", graph.hierarchy_level, ", Cluster number:", graph.n_nodes, ", Modularity:", graph.modularity()
    cluster_number[i] = graph.n_nodes
    cluster_labels[i] = list(graph.node_name[graph.hierarchy_level])
    cluster_sizes[i] = list(graph.cluster_size)
    node_labels[i] = copy.deepcopy(graph.node_label[graph.hierarchy_level-1])
    cluster_edges[i] = list(graph.edge_number)
    adjacent_matrix[i] = copy.deepcopy(graph.edge_set)
opt = np.argmax(np.array(modularity_score))

t1 = time.time()
total = t1-t0
print "Computational Time for Non-binary Hierarchical Clustering: ", total

print "Printing and Saving Results..."
plotting.plot_line(beta_list, modularity_score, methodname="Nonbinary_Tree", paraname="Beta")
plotting.plot_histogram(cluster_sizes[opt], methodname="Nonbinary_Tree")

result = {"Modularity": modularity_score[opt], "Cluster Number": cluster_number[opt], "Cluster Sizes": cluster_sizes[opt], "Cluster Names":
        cluster_labels[opt], "Node Labels": node_labels[opt], "Cluster Edge Sizes": cluster_edges[opt], "Adjacent Matrix": adjacent_matrix[opt]}
IO.SaveDict("./Data/test_2000/Nonbinary_Tree_Results.txt", "w", result)


# Modularity Maximization clustering algorithms on the Whole Dataset
print "###############################################################"
print "Modularity Maximization Clustering Algorithms for the whole dataset"

t0 = time.time()
graph = ModularityGraph(network)

#initialization of the hyperparameter list
N_list = [15000, 10000, 5000, 2000, 1000, 900, 800, 500, 300]

#initialization of measurements
modularity_score = [0 for i in N_list]
cluster_number = [0 for i in N_list]
cluster_labels = [[] for i in N_list]
node_labels = [[] for i in N_list]
cluster_edges = [[] for i in N_list]
cluster_sizes = [[] for i in N_list]
adjacent_matrix = [{} for i in N_list]

for i in range(len(N_list)):
    n_clus = algorithms.modularity_clustering(graph, num_clusters=N_list[i])

    modularity_score[i] = graph.modularity()
    print "Cluster Number:", n_clus, ", Modularity is:", modularity_score[i]
    cluster_number[i] = n_clus

    indices= [0 for j in range(graph.n_nodes())]
    index = 0
    for c in range(graph.n_nodes()):
        if graph.clusters[c]["is_empty"]==False:
            cluster_labels[i].append(graph.clusters[c]["name"])
            cluster_sizes[i].append(len(graph.clusters[c]["nodes"]))
            cluster_edges[i].append(graph.edge_number[c])
            indices[c] = index
            index += 1

    node_labels[i] = np.copy(graph.node_labels)
    for u, v in graph.cluster_links:
        adjacent_matrix[i][(indices[u], indices[v])] = graph.inter_edge_matrix[u, v]
opt = np.argmax(np.array(modularity_score))

t1 = time.time()
total = t1-t0
print "Computational Time for Modularity Maximization: ", total

print "Printing and Saving Results..."
plotting.plot_line(N_list, modularity_score, label="whole")
plotting.plot_histogram(cluster_sizes[opt], methodname="Modularity_Maximization", label="whole")

result = {"Modularity": modularity_score[opt], "Cluster Number": cluster_number[opt], "Cluster Sizes": cluster_sizes[opt], "Cluster Names":
        cluster_labels[opt], "Node Labels": node_labels[opt], "Cluster Edge Sizes": cluster_edges[opt], "Adjacent Matrix": adjacent_matrix[opt]}
IO.SaveDict("./Data/whole/Modularity_Maximization_Results.txt", "w", result)

with open("./Data/whole/cluster_labels.csv", "w") as writer:
    writer.write("name,group,size\n")
    for i in range(len(result["Cluster Names"])):
        cluster_label = result["Cluster Names"][i]
        cluster_size = result["Cluster Sizes"][i]
        writer.write(str(cluster_label)+","+str(i)+","+str(cluster_size)+"\n")

with open("./Data/whole/links.csv", "w") as writer:
    writer.write("citing_cluster,cited_cluster\n")
    for key, value in result["Adjacent Matrix"].iteritems():
        writer.write(str(key[0])+","+str(key[1])+","+str(value)+"\n")
