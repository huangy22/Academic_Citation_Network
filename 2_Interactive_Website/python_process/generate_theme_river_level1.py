#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import csv
import json
import pprint
from pymongo import MongoClient
import numpy as np
import collections
from datetime import datetime

client = MongoClient()
db = client.aps
cluster_articles = db["cluster_articles"]
clusters = db["article_clusters"]

data_dict = collections.OrderedDict()
for entry in cluster_articles.find():
    if "level1" in entry["_id"]:
        level1_id = entry["_id"]["level1"]
        level1_name = clusters.find_one({"_id": level1_id, "level": 1})["name"]
        
        value = entry["number_of_articles"]
        month = entry["_id"]["month"]
        year = entry["_id"]["year"]

        if level1_name not in data_dict:
            data_dict[level1_name] = {}
        if year+" "+month in data_dict[level1_name]:
            data_dict[level1_name][year+" "+month] += value
        else:
            data_dict[level1_name][year+" "+month] = value

times = data_dict[27601].keys()
times = sorted(times)

titles = {}
titles[u'27601'] = u"Condensed Matter Theory"
titles[u'4752'] = u"Optics, Electronic and Magnetic Devices"
titles[u'24952'] = u"Condensed Matter Materials"
titles[u'13363'] = u"Physics of Gases, Plasmas"
titles[u'10901'] = u"Nuclear Physics"
titles[u'8192'] = u"Superconductivity"
titles[u'2525'] = u"Classical Mechanics, Fluid Dynamics"
titles[u'15087'] = u"Biophysics, Physical Chemistry"
titles[u'16935'] = u"Low-Dimensional Structures"
titles[u'25951'] = u"Astronomy and Astrophysics"
titles[u'6862'] = u"Soft Condensed Matter"
titles[u'18844'] = u"Plasmas and Electric Discharges"
titles[u'3613'] = u"Interdisciplinary Applications of Physics"

data = []
for name in data_dict:
    value = []
    for time in times:
        year= time.split(" ")[0]
        month= time.split(" ")[1]
        d = datetime.strptime("01."+month+"."+year+" 00:00:00", "%d.%m.%Y %H:%M:%S").strftime('%s')
        mili = int(d)*1000

        if time in data_dict[name]:
            value.append([mili, data_dict[name][time]])
        else:
            value.append([mili, 0])

    data.append({"key": titles[str(name)], "values": value, "number": name})

# Writes the json output to the file
file("../data/level1/theme_river.json", 'w').write(json.dumps(data))

