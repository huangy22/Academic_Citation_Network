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
article_clusters = db["article_clusters"]
links = db["article_cluster_links"]

files = glob.glob("../machine_learning_data/*level2*.txt")

node_cited_dict = {}
for entry in network.find():
    key = entry[u'cited_doi']
    if key in node_cited_dict:
        node_cited_dict[key] += 1
    else:
        node_cited_dict[key] = 1

title_dict = {}
for entry in articles.find():
    title_dict[entry[u'articleId']] = entry[u'title'][u'value']

for filename in files:

    result = IO.LoadDict(filename)
    level1_cluster_name = filename.split("_")[3]
    level1_cluster = article_clusters.find_one({"level": 1, "name": int(level1_cluster_name)})

    graph = ModularityGraph()
    graph.build_level2(articles, network, level1_cluster["_id"])

    clusters = []
    indices = np.argsort(result["Cluster Sizes"])[::-1]
    for i in indices:
        if result["Cluster Sizes"][i] >= 20:
            nodes = []
            node_cited_number = []
            for node in range(len(result["Node Labels"])):
                article_id = result["Node Labels"][node].keys()[0]
                if result["Node Labels"][node][article_id]== result["Cluster Names"][i]:
                    if article_id in node_cited_dict:
                        nodes.append(node)
                        node_cited_number.append(node_cited_dict[article_id])
                    else:
                        nodes.append(node)
                        node_cited_number.append(0)
            node_ids = np.argsort(np.array(node_cited_number))[::-1][:10]
            article_list = []
            for node in node_ids:
                article_list.append({"articleId": graph.id_to_article[nodes[node]], "title": title_dict[graph.id_to_article[nodes[node]]].encode('ascii', 'ignore'), "cited_number": node_cited_number[node]})
            clusters.append({"level": 2, "level1_cluster": level1_cluster["_id"], "name": result["Cluster Names"][i], "size": result["Cluster Sizes"][i], "total_edge_number": result["Cluster Edge Sizes"][i], "top_ten_articles": article_list})

    article_clusters.insert_many(clusters)

    for i in range(len(result["Node Labels"])):
        article_id = result["Node Labels"][i].keys()[0]
        cluster = article_clusters.find_one({"level": 2, "name": result["Node Labels"][i][article_id]})
        article = articles.find_one({"articleId": article_id})
        if cluster:
            articles.update({"_id": article["_id"]}, {"$set": {"level2_cluster": cluster["_id"]}})
