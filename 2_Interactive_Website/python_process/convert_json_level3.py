#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import csv
import json
import pprint
import glob

node_files = glob.glob("../machine_learning_data/level3/*_article_labels.csv")
link_files = glob.glob("../machine_learning_data/level3/*_article_links.csv")

for i in range(len(node_files)):
    node_file = node_files[i]
    link_file = link_files[i]

    cluster1_name = node_file.split("_")[2]
    cluster1_name = cluster1_name.split("/")[-1]

    cluster2_name = node_file.split("_")[3]

    papers = []
    groups = []
    f = open(node_file, 'r')
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
        cited_times = [0 for i in papers]
        for row in reader:
            cited_times[papers.index(row[1])] += 1
    finally:
            f.close()

    if len(papers)>500:
        threshold = 7
    else:
        threshold = 2

    for times, paper, group in zip(cited_times, papers, groups):
        if times < threshold:
            papers.remove(paper)
            groups.remove(group)
            cited_times.remove(times)

    links = []
    f = open(link_file, 'r')
    try:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row[0] in papers and row[1] in papers:
                link = {"source": papers.index(row[0]), "target": papers.index(row[1]), "value": 1}
                links.append(link)
    finally:
            f.close()

    graph = {"links": links, "nodes": [{"name": papers[i], "group": groups[i]} for i in range(len(papers))]}

    # Writes the json output to the file
    file("../data/level3/"+cluster1_name+"_"+cluster2_name+"_citation_network.json", 'w').write(json.dumps(graph))
