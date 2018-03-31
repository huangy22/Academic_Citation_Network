#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import csv
import json
import pprint

folder = "test_2000/"
article_file = "../Data/"+folder+"article_labels.csv"
link_file = "../Data/"+folder+"links.csv"

papers = []
groups = []
f = open(article_file, 'r')
try:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        papers.append(row[0])
        groups.append(row[1])
finally:
        f.close()

links = []
f = open(link_file, 'r')
try:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        link = {"source": papers.index(row[1]), "target": papers.index(row[0]), "value": 1}
        links.append(link)
finally:
        f.close()

graph = {"links": links, "nodes": [{"name": papers[i], "group": groups[i]} for i in range(len(papers))]}

# Writes the json output to the file
file("./citation_network_2000.json", 'w').write(json.dumps(graph))
