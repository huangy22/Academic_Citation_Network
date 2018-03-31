#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import csv
import json
import pprint

folder = "whole/"
node_file = "../Data/"+folder+"cluster_labels.csv"
link_file = "../Data/"+folder+"links.csv"

clusters = []
groups = []
sizes = []
f = open(node_file, 'r')
try:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        clusters.append(row[0])
        groups.append(row[1])
        sizes.append(row[2])
finally:
        f.close()

links = []
f = open(link_file, 'r')
try:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        link = {"source": int(row[1]), "target": int(row[0]), "value": float(row[2])}
        links.append(link)
finally:
        f.close()

graph = {"links": links, "nodes": [{"name": clusters[i], "group": groups[i], "size": sizes[i]} for i in range(len(clusters))]}

# Writes the json output to the file
file("./citation.json", 'w').write(json.dumps(graph))
