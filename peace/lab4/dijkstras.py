import matplotlib.pyplot as plt
import networkx as nx
from queue import Queue
import numpy as np

DG = nx.DiGraph()
q = Queue()


def add_edges():
    DG.add_weighted_edges_from([(1, 4, 6), (1, 6, 1)])
    DG.add_weighted_edges_from([(2, 1, 1), (2, 3, 3), (2, 4, 3)])
    DG.add_weighted_edges_from([(3, 1, 3), (3, 6, 2)])
    DG.add_weighted_edges_from([(4, 1, 5), (4, 3, 3)])
    DG.add_weighted_edges_from([(5, 6, 5), (5, 7, 6), (5, 8, 3)])
    DG.add_weighted_edges_from([(6, 2, 1), (6, 3, 3), (6, 7, 2)])
    DG.add_weighted_edges_from([(7, 3, 3), (7, 6, 1)])
    DG.add_weighted_edges_from([(8, 3, 2), (8, 4, 3), (8, 7, 4)])
    for i in range(8):
        DG.nodes[i + 1]['way'] = float('inf')
        DG.nodes[i + 1]['is_visited'] = 0


def algho(start_node=None):
    if start_node is None:
        start_node = min(DG.nodes, key=lambda x: DG.degree(x) - len(list(DG.neighbors(x))))

    q.put(start_node)
    DG.nodes[start_node]['way'] = 0

    while not q.empty():
        current_node = q.get()
        neighbors_list = DG.neighbors(current_node)

        for x in neighbors_list:
            if DG.nodes[x]['is_visited'] == 1:
                continue

            q.put(x)

            if DG.nodes[x]['way'] > DG.nodes[current_node]['way'] + DG.edges[current_node, x]['weight']:
                DG.nodes[x]['way'] = DG.nodes[current_node]['way'] + DG.edges[current_node, x]['weight']

        DG.nodes[current_node]['is_visited'] = 1

    for i in range(8):
        print(f'Way from {start_node} to {i+1} = {DG.nodes[i+1]["way"]} ')


add_edges()
algho()

subax1 = plt.subplot(121)
nx.draw(DG, with_labels=True, font_weight='bold')
plt.show()


