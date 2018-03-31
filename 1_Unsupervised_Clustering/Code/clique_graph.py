#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import numpy as np
import heapq
import matplotlib.pyplot as plt

class CliqueGraph:

    def __init__(self, links_file, beta=0.5, gamma=0.9, lamb=1.0, t=1.0, test=False):
        self.beta = beta
        self.gamma = gamma
        self.lamb = lamb
        self.t = t

        self.article_to_id = {}
        self.id_to_article = {}

        self.cluster_sets = [[]]
        self.node_name = []
        self.hierarchy_level = 0

        self.build_article_dictionay(links_file, test)
        self.build_links(links_file, test)

        self.node_label = [[set() for i in range(self.n_nodes)]]
        self.contribution = np.zeros(self.n_nodes)
        self.clique_size = []
        self.cluster_size = [1 for i in range(self.n_nodes)]

    def build_article_dictionay(self, link_file, test):
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
        self.n_nodes = len(self.article_to_id)
        self.node_name.append(range(self.n_nodes))

    def build_links(self, links_file, test):
        self.edge_set = {}
        self.intra_edge = np.zeros(self.n_nodes)
        self.edge_number = np.zeros(self.n_nodes)
        for entry in links_file.find():
            target_article = entry[u'cited_doi']
            source_article = entry[u'citing_doi']
            if target_article in self.article_to_id and source_article in self.article_to_id:
                target_id = self.article_to_id[target_article]
                source_id = self.article_to_id[source_article]
                self.edge_set[(source_id, target_id)]=1.0
                self.edge_number[source_id] += 1

    def modularity(self):
        TotN = np.sum(self.edge_number)
        intra = np.sum(self.intra_edge)
        edges = self.edge_number
        Q = intra/TotN - np.inner(edges/TotN, edges/TotN)
        return Q

    def create_new_clique(self):
        self.cluster_sets[self.hierarchy_level].append(set())
        self.contribution.fill(0.0)
        self.clique_size.append(0)
        return len(self.cluster_sets[self.hierarchy_level])-1

    def add_node_to_clique(self, clique_idx, node):
        self.cluster_sets[self.hierarchy_level][clique_idx].add(node)
        self.node_label[self.hierarchy_level][node].add(clique_idx)
        delta_edges = self.update_edges(clique_idx, node)
        self.clique_size[clique_idx] += 1
        return delta_edges

    def update_edges(self, clique, node):
        self.contribution[node] = float("-inf")
        delta_edges = 0.0
        for link, weight in self.edge_set.iteritems() :
            if link[0]==node:
                self.contribution[link[1]] += weight
                if clique in self.node_label[self.hierarchy_level][link[1]]:
                    delta_edges += 1.0
            if link[1]==node:
                self.contribution[link[0]] += weight
                if clique in self.node_label[self.hierarchy_level][link[0]]:
                    delta_edges += 1.0
        return delta_edges

    def find_best_node_to_clique(self, clique):
        node = np.argmax(self.contribution/self.clique_size[clique]) 
        return node, self.contribution[node]/self.clique_size[clique]

    def get_alpha(self, edge, n):
        alpha_n = 1.0-1.0/(2.0*self.lamb*(n+self.t))
        d_C = edge/n/(n-1.0)
        return alpha_n*d_C

    def grow_clique(self, link):
        clique = self.create_new_clique()
        intra_edge = 0.0
        not_collected = range(self.n_nodes)

        intra_edge += self.add_node_to_clique(clique, link[0][0])
        not_collected.remove(link[0][0])

        intra_edge += self.add_node_to_clique(clique, link[0][1])
        not_collected.remove(link[0][1])

        while not_collected:
            node, contribution = self.find_best_node_to_clique(clique)
            threshold = self.get_alpha(intra_edge, len(self.cluster_sets[self.hierarchy_level][clique]))
            if contribution >= threshold:
                intra_edge += self.add_node_to_clique(clique, node)
                not_collected.remove(node)
            else:
                break

    def get_intersect(self):
        intersect = [[0 for i in self.clique_size] for j in self.clique_size]
        for node in range(self.n_nodes):
            for i in self.node_label[self.hierarchy_level][node]:
                for j in self.node_label[self.hierarchy_level][node]:
                    if i < j:
                        intersect[i][j] += 1
        return intersect

    def merge_two_cliques(self, head, tail, intersect):
        self.clique_size.append(self.clique_size[head]+self.clique_size[tail])
        del self.clique_size[tail]
        del self.clique_size[head]

        self.cluster_sets[self.hierarchy_level].append(self.cluster_sets[self.hierarchy_level][head].union(self.cluster_sets[self.hierarchy_level][tail]))
        del self.cluster_sets[self.hierarchy_level][tail]
        del self.cluster_sets[self.hierarchy_level][head]

        cluster_label = len(self.cluster_sets[self.hierarchy_level])-1
        for i in range(len(intersect)):
            if i!= head and i!= tail:
                intersect[i].append(intersect[i][head]+intersect[head][i]+intersect[i][tail]+intersect[tail][i])
                del intersect[i][tail]
                del intersect[i][head]
        intersect.append([0 for i in self.clique_size])

        del intersect[tail]
        del intersect[head]
        return intersect

    def merge_clique(self):
        head = 0
        tail = 1
        num_clique = len(self.clique_size)
        intersect = self.get_intersect()
        while tail < num_clique:
            minsize = self.clique_size[head] if self.clique_size[head] < self.clique_size[tail] else self.clique_size[tail]
            if intersect[head][tail] > self.beta*minsize:
                self.merge_two_cliques(head, tail, intersect)
                num_clique -= 1
                tail = tail-2 if tail-2 > 1 else 1
            else:
                head += 1
                if head < tail:
                    continue
            tail += 1
            head = 0

    def assign_new_nodes(self):
        new_n_nodes = len(self.clique_size)
        for c in range(new_n_nodes):
            for i in iter(self.cluster_sets[self.hierarchy_level-1][c]):
                if len(self.node_label[self.hierarchy_level-1][i])==1:
                    self.node_name[self.hierarchy_level].append(i)
                    break
            if c != len(self.node_name[self.hierarchy_level])-1:
                self.node_name[self.hierarchy_level].append(next(iter(self.cluster_sets[self.hierarchy_level-1][c])))
        for node in range(self.n_nodes):
            if len(self.node_label[self.hierarchy_level-1][node])==0:
                new_n_nodes += 1
                self.node_name[self.hierarchy_level].append(node)
        return new_n_nodes

    def construct_new_graph(self):
        self.hierarchy_level += 1
        self.cluster_sets.append([])
        self.node_name.append([])

        new_nodes = self.assign_new_nodes()
        new_edge_set = [[0.0 for i in range(new_nodes)] for  j in range(new_nodes)]
        self.node_label[self.hierarchy_level-1] = [set() for i in range(self.n_nodes)]
        for node1 in range(new_nodes):
            if node1 < len(self.clique_size):
                list1 = self.cluster_sets[self.hierarchy_level-1][node1]
                for u in list1:
                    new_edge_set[node1][node1] += self.intra_edge[u]
                    self.node_label[self.hierarchy_level-1][u].add(self.node_name[self.hierarchy_level][node1])
            else:
                list1 = [node1]
                new_edge_set[node1][node1] += self.intra_edge[node1]
                self.node_label[self.hierarchy_level-1][self.node_name[self.hierarchy_level][node1]].add(self.node_name[self.hierarchy_level][node1])
            self.cluster_size[node1] = len(list1)

            for node2 in range(new_nodes):
                if node2 < len(self.clique_size):
                    list2 = self.cluster_sets[self.hierarchy_level-1][node2]
                else:
                    list2 = [node2]

                for u in list1:
                    for v in list2:
                        weight = self.edge_set.get((u, v), 0)
                        new_edge_set[node1][node2] += weight

        self.n_nodes = new_nodes
        heap = []
        self.edge_set = {}
        self.intra_edge = np.zeros(new_nodes)
        self.edge_number = np.zeros(new_nodes)
        for u in range(new_nodes):
            self.intra_edge[u] = new_edge_set[u][u]
            self.edge_number[u] = new_edge_set[u][u]
            for v in range(new_nodes):
                if u!=v and new_edge_set[u][v]!=0:
                    self.edge_set[(u, v)]=new_edge_set[u][v]
                    self.edge_number[u] += new_edge_set[u][v]

        self.clique_size = []
        self.node_label.append([set() for i in range(self.n_nodes)])
