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
affiliations = db["tot_affiliations"]
clusters = db["article_clusters"]

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
for entry in affiliations.find():
    if "level1_cluster" in entry and "level2_cluster" in entry:
        level1_id = entry["level1_cluster"]
        level1_name = clusters.find_one({"_id": level1_id, "level": 1})["name"]

        level2_id = entry["level2_cluster"]
        level2_name = clusters.find_one({"_id": level2_id, "level": 2})["name"]

        name = entry["affiliation"]
        value = entry["weight"]
        data.append({"level1_name": titles[str(level1_name)], "level1": level1_name, "level2": level2_name, "values": value, "name": name})

# Writes the json output to the file
file("../data/level1/affiliations.json", 'w').write(json.dumps(data))

