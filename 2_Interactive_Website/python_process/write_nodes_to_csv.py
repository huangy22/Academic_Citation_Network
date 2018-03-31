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
import glob

np.set_printoptions(threshold=np.inf)

client = MongoClient()
db = client.aps

network = db["tot_network"]
articles = db["tot_articles"]
article_clusters = db["article_clusters"]
links = db["article_cluster_links"]

files = glob.glob("../machine_learning_data/level2/*level2*.txt")

for filename in files:

    result = IO.LoadDict(filename)
    level1_cluster_name = filename.split("_")[3]
    level1_cluster = article_clusters.find_one({"level": 1, "name": int(level1_cluster_name)})

    with open("../machine_learning_data/level2/"+str(level1_cluster_name)+"_cluster_labels.csv", "w") as writer:
        writer.write("name,group,size\n")
        for i in range(len(result["Cluster Names"])):
            cluster_label = result["Cluster Names"][i]
            cluster_size = result["Cluster Sizes"][i]
            writer.write(str(cluster_label)+","+str(i)+","+str(cluster_size)+"\n")

    with open("../machine_learning_data/level2/"+str(level1_cluster_name)+"_cluster_links.csv", "w") as writer:
        writer.write("citing_cluster,cited_cluster\n")
        for key, value in result["Adjacent Matrix"].iteritems():
            writer.write(str(key[0])+","+str(key[1])+","+str(value)+"\n")

    #graph = ModularityGraph()
    #graph.build_level2(articles, network, level1_cluster["_id"])

    #clusters = []
    #indices = np.argsort(result["Cluster Sizes"])[::-1]
    #for i in indices:
        #if result["Cluster Sizes"][i] >= 20:
            #cluster_name = result["Cluster Names"][i]

            #with open("../machine_learning_data/"+level1_cluster_name+"_"+str(result["Cluster Names"][i])+"_article_labels.csv", "w") as writer:
                #writer.write("article_doi,group\n")
                #for article in result["Node Labels"]:
                    #if article.values()[0] == cluster_name:
                        #writer.write(article.keys()[0]+","+str(article.values()[0])+"\n")

            #with open("../machine_learning_data/"+level1_cluster_name+"_"+str(result["Cluster Names"][i])+"_article_links.csv", "w") as writer:
                #writer.write("citing_doi,cited_doi\n")
                #for i,j in graph.links:
                    #if result["Node Labels"][i].values()[0] == cluster_name and result["Node Labels"][j].values()[0] == cluster_name:
                        #writer.write(graph.id_to_article[i]+","+graph.id_to_article[j]+"\n")

