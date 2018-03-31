#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import numpy as np
import matplotlib.pyplot as plt

class ModularityGraph:

    def __init__(self):
        self.article_to_id = {}
        self.id_to_article = {}
        self.links = set()
        self.clusters = []
        self.cluster_links = set()
        self.n_clusters = 0

    def build_test(self, links_file):
        self.build_article_dictionay(links_file, True)
        self.build_links(links_file)
        self.build_adj_matrix()
        self.init_singleton_clusters()

    def build_whole(self, links_file):
        self.article_to_id = {}
        self.id_to_article = {}
        self.links = set()
        self.clusters = []
        self.cluster_links = set()
        self.n_clusters = 0

        self.build_article_dictionay(links_file, False)
        self.build_links(links_file)
        self.build_adj_matrix()
        self.init_singleton_clusters()

    def build_level2(self, article_file, links_file, cluster_name):
        self.article_to_id = {}
        self.id_to_article = {}
        self.links = set()
        self.clusters = []
        self.cluster_links = set()
        self.n_clusters = 0

        self.build_article_dictionay_level2(article_file, cluster_name)
        self.build_links(links_file)

        self.build_adj_matrix()
        self.init_singleton_clusters()

    def n_links(self):
        return len(self.links)

    def n_nodes(self):
        return len(self.article_to_id)

    def build_article_dictionay(self, link_file, test=False):
        article_id = 0
        for entry in link_file.find():
            target = entry[u'cited_doi']
            source = entry[u'citing_doi']

            if source not in self.article_to_id:
                source_id = article_id
                if not test or article_id < 2000:
                    self.id_to_article[source_id] = source
                    self.article_to_id[source] = source_id
                    article_id += 1

            if target not in self.article_to_id:
                target_id = article_id
                if not test or article_id < 2000:
                    self.id_to_article[target_id] = target
                    self.article_to_id[target] = target_id
                    article_id += 1

    def build_links(self, links_file):
        for entry in links_file.find():
            target_article = entry[u'cited_doi']
            source_article = entry[u'citing_doi']
            if target_article in self.article_to_id and source_article in self.article_to_id:
                target_id = self.article_to_id[target_article]
                source_id = self.article_to_id[source_article]
                self.links.add((source_id, target_id))

    def build_article_dictionay_level2(self, article_file, cluster_name):
        article_id = 0
        for entry in article_file.find():
            if "level1_cluster" in entry and entry['level1_cluster']==cluster_name:
                article = entry['articleId']
                if article not in self.article_to_id:
                    self.id_to_article[article_id] = article
                    self.article_to_id[article] = article_id
                    article_id += 1

    def build_adj_matrix(self):
        n_nodes = self.n_nodes()
        self.adj_matrix = np.zeros((n_nodes, n_nodes))
        n_nodes = len(self.article_to_id)
        for pair in list(self.links):
            self.adj_matrix[pair[0], pair[1]] = 1.0

    def init_singleton_clusters(self):
        n_nodes = self.n_nodes()
        self.node_labels = np.zeros(n_nodes)
        for i in range(n_nodes):
            self.node_labels[i] = i
            cluster = {"name": i, "nodes": [i], "is_empty": False}
            self.clusters.append(cluster)
        self.edge_number = np.sum(self.adj_matrix, axis=1)
        self.inter_edge_matrix = np.copy(self.adj_matrix)
        self.cluster_links = self.links.copy()
        self.n_clusters = n_nodes
        self.gradient = np.full((n_nodes, n_nodes), float("-inf"))
        _ = np.outer(self.edge_number, self.edge_number, self.gradient)
        TotN = self.n_links()
        self.gradient *= -2.0/TotN
        for i, j in self.cluster_links:
            self.gradient[i, j] += self.inter_edge_matrix[i, j]
            self.gradient[j, i] += self.inter_edge_matrix[i, j]

    def modularity(self):
        TotN = self.n_links()
        matrix = self.inter_edge_matrix
        edges = self.edge_number
        Q = np.trace(matrix/TotN) - np.inner(edges/TotN, edges/TotN)
        return Q

    def update_delta_modularity(self, index1, index2):
        TotN = self.n_links()
        _ = np.multiply(-2.0/TotN*self.edge_number[index1], self.edge_number, self.gradient[index1,:])
        self.gradient[index1, :] += self.inter_edge_matrix[index1, :] 
        self.gradient[index1, :] += self.inter_edge_matrix[:, index1]
        self.gradient[index2, :] = 0.0

        self.gradient[:, index1] = self.gradient[index1, :]
        self.gradient[:, index2] = self.gradient[index2, :]

    def merge_clusters(self, index1, index2):
        if index1==index2:
            print "merge error"
        cluster1 = self.clusters[index1]
        cluster2 = self.clusters[index2]

        cluster1["nodes"] += cluster2["nodes"]
        cluster2["is_empty"] = True

        for i in cluster2["nodes"]:
            self.node_labels[i] = cluster1["name"]
        cluster2["nodes"] = []

        self.n_clusters -= 1

        self.edge_number[index1] += self.edge_number[index2]
        self.edge_number[index2] = 0

        for i in range(self.inter_edge_matrix.shape[0]):
            if i != index1 and i != index2:
                if (index2, i) in self.cluster_links:
                    self.inter_edge_matrix[index1, i] += self.inter_edge_matrix[index2, i]
                    self.cluster_links.add((index1, i))
                if (i, index2) in self.cluster_links:
                    self.inter_edge_matrix[i, index1] += self.inter_edge_matrix[i, index2]
                    self.cluster_links.add((i, index1))
            self.cluster_links.discard((i, index2))
            self.cluster_links.discard((index2, i))

        self.inter_edge_matrix[index1, index1] += self.inter_edge_matrix[index1, index2]
        self.inter_edge_matrix[index1, index1] += self.inter_edge_matrix[index2, index1]+self.inter_edge_matrix[index2, index2]
        self.inter_edge_matrix[index2, :] = 0
        self.inter_edge_matrix[:, index2] = 0

        self.update_delta_modularity(index1, index2)

    def find_clusters_to_merge(self):
        index1, index2 = 0, 0
        max_value = float("-inf")
        if self.cluster_links:
            for i, j in self.cluster_links:
                if self.gradient[i, j] > max_value:
                    max_value = self.gradient[i, j]
                    index1, index2 = i, j
        return index1, index2, self.gradient[index1, index2]
