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
import glob

np.set_printoptions(threshold=np.inf)

client = MongoClient()
db = client.aps

network = db["tot_network"]
articles = db["tot_articles"]
citation_clusters = db["article_clusters"]
citation_links = db["article_cluster_links"]

graph = ModularityGraph()
graph.build_whole(network)

files = glob.glob("../machine_learning_data/*level2*.txt")
for filename in files:

    result = IO.LoadDict(filename)
    level1_cluster_name = int(filename.split("_")[3])

    cluster_links = []
    for key, value in result["Adjacent Matrix"].iteritems():
        if citation_clusters.find_one({"level":2, "name": result["Cluster Names"][key[0]]}) and citation_clusters.find_one({"level":2, "name": result["Cluster Names"][key[1]]}):
            cluster0 = citation_clusters.find_one({"level":2, "name": result["Cluster Names"][key[0]]})["_id"]
            cluster1 = citation_clusters.find_one({"level":2, "name": result["Cluster Names"][key[1]]})["_id"]
            cluster_links.append({"level": 2, "level1_cluster": citation_clusters.find_one({"level": 1, "name": level1_cluster_name})["_id"], "value": value, "source": cluster0, "target": cluster1})
    citation_links.insert_many(cluster_links)
