#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import operator

def modularity_clustering(graph, num_clusters=100):
    n_nodes = graph.n_nodes()
    #mod = graph.modularity()
    while graph.n_clusters > num_clusters:
        index1, index2, gradient = graph.find_clusters_to_merge()
        if index1 == index2:
            break
        graph.merge_clusters(index1, index2)
        if graph.n_clusters%1000 ==0:
            print "Cluster number: ", graph.n_clusters
    return graph.n_clusters

def clique_clustering(graph, max_hierarchy=100):
    while graph.hierarchy_level < max_hierarchy:
        if len(graph.edge_set)==0:
            break
        sorted_edge = sorted(graph.edge_set.items(), key=operator.itemgetter(1))
        sorted_edge.reverse()
        
        w0 = graph.gamma*sorted_edge[0][1]
        for edge in sorted_edge:
            if len(graph.node_label[graph.hierarchy_level][edge[0][0]])!=0 and len(graph.node_label[graph.hierarchy_level][edge[0][1]])!=0:
                continue
            if edge[1] > w0:
                graph.grow_clique(edge)

        graph.merge_clique()
        graph.construct_new_graph()

    return graph.n_nodes
