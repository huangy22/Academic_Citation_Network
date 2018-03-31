#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import csv
import json
import pprint
import glob
import numpy as np

node_files = glob.glob("../machine_learning_data/level2/*_cluster_labels.csv")
link_files = glob.glob("../machine_learning_data/level2/*_cluster_links.csv")

for i in range(len(node_files)):
    node_file = node_files[i]
    link_file = link_files[i]

    cluster_name = node_file.split("_")[2]
    cluster_name = cluster_name.split("/")[-1]

    clusters = []
    groups = []
    sizes = []
    f = open(node_file, 'r')
    try:
        reader = csv.reader(f)
        next(reader)
        node_idx = {}
        idx = 0
        line_number = 0
        for row in reader:
            if int(row[2]) > 40:
                node_idx[line_number] = idx
                idx += 1
                clusters.append(row[0])
                groups.append(row[1])
                sizes.append(int(row[2]))
            line_number += 1
    finally:
            f.close()

    groups = [groups[i] for i in np.argsort(sizes)[::-1]]
    clusters = [clusters[i] for i in np.argsort(sizes)[::-1]]
    position = 0
    indices = {}
    for i in np.argsort(sizes)[::-1]:
        indices[i] = position
        position += 1

    sizes = np.sort(sizes)[::-1]

    links = []
    f = open(link_file, 'r')
    try:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if int(row[0]) in node_idx and int(row[1]) in node_idx:
                link = {"source": indices[node_idx[int(row[0])]], "target": indices[node_idx[int(row[1])]], "value": float(row[2])}
                links.append(link)
    finally:
            f.close()
            
    graph = {"links": links, "nodes": [{"name": clusters[i], "group": groups[i], "size": sizes[i], "index": i} for i in range(len(sizes))]}
    indices = {}
    for i in range(len(sizes)):
        indices[clusters[i]] = i
    print cluster_name

    # Writes the json output to the file
    file("../data/level2/"+cluster_name+"_citation_network.json", 'w').write(json.dumps(graph))
