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
authors = db["authors_more_than_20"]
clusters = db["article_clusters"]

level1 = [10901, 13363, 15087, 16935, 18844, 24952, 2525, 25951, 27601, 3613, 4752, 6862, 8192]

dict_index = {}
dict_index[10901] = {'1176': 10, '1805': 5, '907': 12, '993': 9, '1076': 8, '856': 7, '1073': 0, '574': 1, '1370': 3, '1480': 2, '1465': 6, '921': 4, '1295': 11}
dict_index[13363] = {'1186': 1, '1649': 6, '1191': 7, '2033': 0, '1521': 5, '2031': 3, '1390': 8, '1654': 4, '1749': 2}
dict_index[15087] = {'854': 0, '976': 5, '1175': 4, '1429': 3, '839': 10, '872': 8, '809': 6, '521': 7, '1118': 9, '1248': 1, '1448': 2}
dict_index[16935] = {'1069': 6, '1129': 2, '893': 3, '1121': 4, '863': 5, '1229': 1, '1261': 8, '1436': 7, '804': 0}
dict_index[18844] = {'619': 1, '465': 2, '159': 5, '413': 0, '234': 3, '358': 4}
dict_index[24952] = {'1772': 5, '1271': 0, '955': 4, '858': 3, '1648': 8, '1500': 7, '1596': 2, '1676': 1, '926': 6}
dict_index[2525] = {'1166': 5, '1302': 0, '624': 3, '1220': 2, '1225': 8, '1153': 7, '1066': 1, '1257': 4, '867': 11, '1361': 9, '1380': 10, '815': 6}
dict_index[25951] = {'882': 6, '598': 5, '875': 7, '1195': 3, '940': 4, '253': 2, '493': 0, '1000': 1}
dict_index[27601] = {'1139': 4, '3871': 5, '3694': 1, '3981': 7, '1500': 0, '2386': 3, '1289': 6, '1369': 2}
dict_index[3613] = {'258': 1, '471': 0, '412': 2}
dict_index[4752] = {'2616': 1, '1588': 6, '3200': 11, '2173': 5, '598': 3, '2233': 10, '2386': 9, '2782': 12, '2191': 0, '1077': 4, '2535': 8, '2691': 2, '2360': 7}
dict_index[6862] = {'176': 2, '416': 0, '533': 1, '437': 3}
dict_index[8192] = {'1165': 7, '1269': 3, '1216': 9, '1424': 4, '705': 1, '1179': 2, '1244': 5, '1229': 8, '1464': 0, '1253': 6}

for level1_name in level1:
    data = []
    for entry in authors.find():
        level1_id = entry["level1_cluster"]
        if level1_name == clusters.find_one({"_id": level1_id, "level": 1})["name"]:
            level2_id = entry["level2_cluster"]
            level2_name = clusters.find_one({"_id": level2_id, "level": 2})["name"]

            name = entry["author"]["name"]
            value = entry["publications"]
            data.append({"level1": level1_name, "level2": level2_name, "values": value, "name": name})

    # Writes the json output to the file
    file("../data/level2/"+str(level1_name)+"_authors.json", 'w').write(json.dumps(data))

