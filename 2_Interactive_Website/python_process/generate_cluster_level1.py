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

for i in range(len(result["Node Labels"])):
    article_id = graph.id_to_article[i]
    cluster = citation_clusters.find_one({"name": result["Node Labels"][i]})
    article = articles.find_one({"articleId": article_id})
    if cluster:
        articles.update({"_id": article["_id"]}, {"$set": {"level1_cluster": cluster["_id"]}})

title_dict = {}
for entry in articles.find():
    title_dict[entry[u'articleId']] = entry[u'title'][u'value']

clusters = []
for i in range(len(result["Cluster Names"])):
    nodes = []
    node_cited_number = []
    for node in range(len(result["Node Labels"])):
        if result["Node Labels"][node]==result["Cluster Names"][i]:
            nodes.append(node)
            node_cited_number.append(np.sum(graph.adj_matrix[:,node]))

    if len(node_cited_number)>=10:
        node_ids = np.argsort(np.array(node_cited_number))[::-1][:10]
    else:
        node_ids = np.argsort(np.array(node_cited_number))[::-1]
    article_list = []
    for node in node_ids:
        article_list.append({"articleId": graph.id_to_article[nodes[node]], "title": title_dict[graph.id_to_article[nodes[node]]].encode('ascii', 'ignore'), "cited_number": node_cited_number[node]})
    clusters.append({"level": 1, "name": result["Cluster Names"][i], "size": result["Cluster Sizes"][i], "total_edge_number": result["Cluster Edge Sizes"][i], "top_ten_articles": article_list})

