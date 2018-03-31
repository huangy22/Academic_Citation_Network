#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
from pymongo import MongoClient
import numpy as np
import operator

client = MongoClient()
db = client.aps
authors_db = db["authors_more_than_20"]
affiliations = db["tot_affiliations"]

for affiliation in affiliations.find():
    authors = affiliation["authors"]
    clusters = {}
    weight = {}
    for author_id in authors:
        if authors_db.find_one({"_id": author_id["id"]}):
            author = authors_db.find_one({"_id": author_id["id"]})
            level1 = author["level1_cluster"]
            level2 = author["level2_cluster"]
            if (level1, level2) in clusters:
                clusters[(level1, level2)] += 1
                weight[(level1, level2)] += author["publications"]
            else:
                clusters[(level1, level2)] = 1
                weight[(level1, level2)] = author["publications"]

    if len(clusters) >0:
        cluster_dict = []
        for (level1, level2), value in clusters.iteritems():
            cluster_dict.append({"level1_cluster": level1, "level2_cluster": level2, "num_author": value, "weight": weight[(level1, level2)]})
        affiliations.update({"_id": affiliation["_id"]}, {'$set': {"cluster_weights": cluster_dict}})
