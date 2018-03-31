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

result = IO.LoadDict("../machine_learning_data/whole/Modularity_Maximization_Results.txt")

client = MongoClient()
db = client.aps
network = db["tot_network"]
articles = db["tot_articles"]
citation_clusters = db["article_clusters"]
graph = ModularityGraph(network)

title_dict = {}
for entry in articles.find():
    title_dict[entry[u'articleId']] = entry[u'title'][u'value']

cluster_links = []
for key, value in result["Adjacent Matrix"].iteritems():
    if citation_clusters.find_one({"name": result["Cluster Names"][key[0]]}) and citation_clusters.find_one({"name": result["Cluster Names"][key[1]]}):
        cluster0 = citation_clusters.find_one({"name": result["Cluster Names"][key[0]]})["_id"]
        cluster1 = citation_clusters.find_one({"name": result["Cluster Names"][key[1]]})["_id"]
        cluster_links.append({"level": 1, "value": value, "source": cluster0, "target": cluster1})
citation_links = db["article_cluster_links"]
citation_links.insert_many(cluster_links)

#title_dict = {}
#for entry in articles.find():
    #title_dict[entry[u'articleId']] = entry[u'title'][u'value']

#indices = np.argsort(np.array(result["Cluster Sizes"]))[::-1][:10]

#with open("top_cited_papers.txt", "w") as writer:
    #for i in indices:
        #writer.write("####################################################################\n")
        #writer.write("cluster name:"+str(result["Cluster Names"][i])+"cluster size: "+str(result["Cluster Sizes"][i])+"\n")
        #nodes = []
        #node_cited_number = []
        #for node in range(len(result["Node Labels"])):
            #if result["Node Labels"][node]==result["Cluster Names"][i]:
                #nodes.append(node)
                #node_cited_number.append(np.sum(graph.adj_matrix[:,node]))

        #node_ids = np.argsort(np.array(node_cited_number))[::-1][:10]
        #writer.write("Top ten most cited papers in the cluster:\n")
        #for node in node_ids:
            #writer.write(graph.id_to_article[nodes[node]]+", "+title_dict[graph.id_to_article[nodes[node]]].encode('ascii', 'ignore')+", cited number:"+str(node_cited_number[node])+"\n\n")

#print result["Node Labels"][graph.article_to_id["10.1103/PhysRevLett.107.150601"]]
