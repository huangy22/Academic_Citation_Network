#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import csv
import json
import pprint
from pymongo import MongoClient
import numpy as np
import glob
import collections
from datetime import datetime

client = MongoClient()
db = client.aps
cluster_articles = db["cluster_articles"]
clusters = db["article_clusters"]

data_dict = {}
times = set()
for entry in cluster_articles.find():
    level1_id = entry["_id"]["level1"]
    level2_id = entry["_id"]["level2"]

    level1_name = clusters.find_one({"_id": level1_id})["name"]
    if clusters.find_one({"_id": level2_id}):
        level2_name = clusters.find_one({"_id": level2_id})["name"]
        value = entry["number_of_articles"]
        month = entry["_id"]["month"]
        year = entry["_id"]["year"]
        if level1_name not in data_dict:
            data_dict[level1_name] = collections.OrderedDict()
            data_dict[level1_name][level2_name] = {}
        elif level2_name not in data_dict[level1_name]:
                data_dict[level1_name][level2_name] = {}
        data_dict[level1_name][level2_name][year+" "+month] = value
        times.add(year+ " "+month)

times = sorted(list(times))
level1 = [10901, 13363, 15087, 16935, 18844, 24952, 2525, 25951, 27601, 3613, 4752, 6862, 8192]

for level1 in data_dict:
    data = []
    index = 1
    for level2 in data_dict[level1]:
        value = []
        for time in times:
            year= time.split(" ")[0]
            month= time.split(" ")[1]
            d = datetime.strptime("01."+month+"."+year+" 00:00:00", "%d.%m.%Y %H:%M:%S").strftime('%s')
            mili = int(d)*1000

            if time in data_dict[level1][level2]:
                value.append([mili, data_dict[level1][level2][time]])
            else:
                value.append([mili, 0])

        data.append({"key": index, "values": value, "level1": level1, "number": level2})
        index += 1

    # Writes the json output to the file
    file("../data/level2/"+str(level1)+"_theme_river.json", 'w').write(json.dumps(data))

