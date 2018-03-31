#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import csv
import json
import pprint

with open('./citation_network.json') as json_data:
#with open('./theme_river.json') as json_data:
    data = json.load(json_data)
    json_data.close()
    pprint.pprint(data)

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

colors= {}
#"#3366cc", "#dc3912", "#ff9900", "#109618", "#990099", "#0099c6", "#dd4477", "#66aa00", "#b82e2e", "#316395", "#994499", "#22aa99", "#aaaa11", "#6633cc", "#e67300", "#8b0707", "#651067", "#329262", "#5574a6", "#3b3eac"
colors[u'27601'] = '#3366cc'
colors[u'4752'] = '#dc3912'

colors[u'24952'] = '#ff9900'
colors[u'13363'] = '#109618'

colors[u'10901'] = '#990099'
colors[u'8192'] = '#dd4477'
colors[u'2525'] = '#66aa00'
colors[u'15087'] = '#b82e2e'
colors[u'16935'] = '#316395'
colors[u'25951'] = '#994499'
colors[u'6862'] = '#22aa99'
colors[u'18844'] = '#aaaa11'
colors[u'3613'] = '#6633cc'

for node in data["nodes"]:
    node[u"title"]  = titles[node["name"]]
    node[u"color"]  = colors[node["name"]]

file("./citation_network.json", 'w').write(json.dumps(data))


