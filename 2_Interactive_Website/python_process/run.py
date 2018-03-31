#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from pymongo import MongoClient
import numpy as np
import random
import algorithms
from modularity_graph import *
import plotting
import json
import IO
import time
import copy

np.set_printoptions(threshold=np.inf)

# Connect to mongodb to get the citation network
client = MongoClient()

db = client.aps
articles = db["tot_articles"]
clusters = db["article_clusters"]
links = db["tot_network"]

# Modularity Maximization clustering algorithms
for cluster in clusters.find({"level":1}):

    graph = ModularityGraph()
    graph.build_level2(articles, links, cluster["_id"])

    print cluster["name"], cluster["size"]

    #initialization of the hyperparameter list
    N_list = [100, 50, 40, 30, 20, 10]

    #initialization of measurements
    modularity_score = [0 for i in N_list]
    cluster_number = [0 for i in N_list]
    cluster_labels = [[] for i in N_list]
    node_labels = [[] for i in N_list]
    cluster_edges = [[] for i in N_list]
    cluster_sizes = [[] for i in N_list]
    adjacent_matrix = [{} for i in N_list]

    for i in range(len(N_list)):
        if N_list[i] < cluster["size"]:
            n_clus = algorithms.modularity_clustering(graph, num_clusters=N_list[i])

            modularity_score[i] = graph.modularity()
            print "Cluster Number:", n_clus, ", Modularity is:", modularity_score[i]
            cluster_number[i] = n_clus

            indices= [0 for j in range(graph.n_nodes())]
            index = 0
            for c in range(graph.n_nodes()):
                node_labels[i].append({graph.id_to_article[c]: graph.node_labels[c]})
                if graph.clusters[c]["is_empty"]==False:
                    cluster_labels[i].append(graph.clusters[c]["name"])
                    cluster_sizes[i].append(len(graph.clusters[c]["nodes"]))
                    cluster_edges[i].append(graph.edge_number[c])
                    indices[c] = index
                    index += 1
            print node_labels[i]

            for u, v in graph.cluster_links:
                adjacent_matrix[i][(indices[u], indices[v])] = graph.inter_edge_matrix[u, v]

    opt = np.argmax(np.array(modularity_score))

    print "maximal modularity", modularity_score[opt], "number of clusters", cluster_number[opt]

    print "Saving Results..."
    #plotting.plot_line(N_list, modularity_score)
    #plotting.plot_histogram(cluster_sizes[opt], methodname="Modularity_Maximization")

    result = {"Modularity": modularity_score[opt], "Cluster Number": cluster_number[opt], "Cluster Sizes": cluster_sizes[opt], "Cluster Names":
            cluster_labels[opt], "Node Labels": node_labels[opt], "Cluster Edge Sizes": cluster_edges[opt], "Adjacent Matrix": adjacent_matrix[opt]}
    IO.SaveDict("../machine_learning_data/level2_"+str(cluster["name"])+"_"+str(cluster["size"])+"_Results.txt", "w", result)

    #with open("./Data/test_2000/article_labels.csv", "w") as writer:
        #writer.write("article_doi,group\n")
        #for i in graph.id_to_article:
            #writer.write(graph.id_to_article[i]+","+str(node_labels[opt][i])+"\n")

    #with open("./Data/test_2000/links.csv", "w") as writer:
        #writer.write("citing_doi,cited_doi\n")
        #for i,j in graph.links:
            #writer.write(graph.id_to_article[i]+","+graph.id_to_article[j]+"\n")

    #with open("./Data/whole/cluster_labels.csv", "w") as writer:
        #writer.write("name,group,size\n")
        #for i in range(len(result["Cluster Names"])):
            #cluster_label = result["Cluster Names"][i]
            #cluster_size = result["Cluster Sizes"][i]
            #writer.write(str(cluster_label)+","+str(i)+","+str(cluster_size)+"\n")

    #with open("./Data/whole/links.csv", "w") as writer:
        #writer.write("citing_cluster,cited_cluster\n")
        #for key, value in result["Adjacent Matrix"].iteritems():
            #writer.write(str(key[0])+","+str(key[1])+","+str(value)+"\n")
