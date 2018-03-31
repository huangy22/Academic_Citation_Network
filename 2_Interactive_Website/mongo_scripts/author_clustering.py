#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
from pymongo import MongoClient
import numpy as np
import operator

client = MongoClient()
db = client.aps
tot_articles = db["tot_articles"]
authors = db["authors_more_than_20"]

for author in authors.find():
    articles = author["articles"]
    clusters = {}
    if "level1_cluster" not in author and "level2_cluster" not in author:
        for article_id in articles:
            article = tot_articles.find_one({"_id": article_id})
            if "level1_cluster" in article and "level2_cluster" in article:
                level1 = article["level1_cluster"]
                level2 = article["level2_cluster"]
                if (level1, level2) in clusters:
                    clusters[(level1, level2)] += 1
                else:
                    clusters[(level1, level2)] = 1
        if len(clusters) >0:
            level1, level2 = max(clusters.iteritems(), key=operator.itemgetter(1))[0]
            authors.update({"_id": author["_id"]}, {'$set': {"level1_cluster": level1, "level2_cluster": level2}})
