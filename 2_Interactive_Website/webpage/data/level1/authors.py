#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import csv
import json
import pprint

with open('./authors.json') as json_data:
    data = json.load(json_data)
    json_data.close()
    #pprint.pprint(data)

colors= {}
#"#3366cc", "#dc3912", "#ff9900", "#109618", "#990099", "#0099c6", "#dd4477", "#66aa00", "#b82e2e", "#316395", "#994499", "#22aa99", "#aaaa11", "#6633cc", "#e67300", "#8b0707", "#651067", "#329262", "#5574a6", "#3b3eac"
colors[27601] = '#3366cc'
colors[4752] = '#dc3912'
colors[24952] = '#ff9900'
colors[13363] = '#109618'
colors[10901] = '#990099'
colors[8192] = '#dd4477'
colors[2525] = '#66aa00'
colors[15087] = '#b82e2e'
colors[16935] = '#316395'
colors[25951] = '#994499'
colors[6862] = '#22aa99'
colors[18844] = '#aaaa11'
colors[3613] = '#6633cc'

index = {}
index[27601] = 0 
index[4752] = 1
index[24952] = 2
index[13363] = 3
index[10901] = 4
index[8192] = 5
index[2525] = 6
index[15087] = 7
index[16935] = 8
index[25951] = 9
index[6862] = 10
index[18844] = 11
index[3613] = 12

size = [0 for i in range(13)]

new_data = []
for node in data:
    node[u"color"]  = colors[node["level1"]]
    node[u"index1"] = index[node["level1"]]
    if size[index[node["level1"]]] < 100:
        new_data.append(node)
        size[index[node["level1"]]] += 1

file("./authors_top.json", 'w').write(json.dumps(new_data))


