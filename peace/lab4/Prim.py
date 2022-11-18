'''
1.2. Задано неорієнтований граф та час переходу від однієї вершини до іншої: 15=6,
16=1, 21=1, 23=3, 24=3, 31=3, 36=2, 41=5, 43=3, 56=5, 57=6, 58=3, 62=1, 63=3, 67=2, 65=2,
73=3, 76=1, 78=2, 83=2, 84=3, 87=4. Необхідно побудувати мінімальне остовне дерево за
допомогою алгоритму Пріма.
'''
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


class Graph():

    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)]
                      for row in range(vertices)]

    def printMST(self, parent):
        print("Edge \tWeight")
        for i in range(1, self.V):
            print(parent[i], "-", i, "\t", self.graph[i][parent[i]])

    def minKey(self, key, mstSet):

        min = float('inf')

        for v in range(self.V):
            if key[v] < min and mstSet[v] == False:
                min = key[v]
                min_index = v

        return min_index

    def primMST(self):

        key = [float('inf')] * self.V
        parent = [None] * self.V
        key[0] = 0
        mstSet = [False] * self.V

        parent[0] = -1

        for cout in range(self.V):

            u = self.minKey(key, mstSet)

            mstSet[u] = True

            for v in range(self.V):

                if self.graph[u][v] > 0 and mstSet[v] == False and key[v] > self.graph[u][v]:
                    key[v] = self.graph[u][v]
                    parent[v] = u

        self.printMST(parent)


if __name__ == '__main__':
    g = Graph(8)
    g.graph = [[0, 1, 3, 5, 0, 1, 0, 0],  # 21=1, 31=3, 41=5, 16=1,
               [1, 0, 3, 3, 0, 1, 0, 0],  # 21=1, 23=3, 24=3, 62=1,
               [3, 3, 0, 3, 0, 2, 3, 2],  # 31=3, 23=3, 43=3, 36=2, 73=3, 83=2,
               [5, 3, 3, 0, 0, 0, 0, 3],  # 41=5, 24=3, 43=3, 84=3,
               [0, 0, 0, 0, 0, 2, 6, 3],  # 65=2, 57=6, 58=3,
               [1, 1, 2, 0, 2, 0, 1, 0],  # 16=1, 62=1, 36=2, 65=2, 76=1,
               [0, 0, 3, 0, 6, 1, 0, 2],  # 73=3, 57=6, 76=1, 78=2,
               [0, 0, 2, 3, 3, 0, 2, 0]]  # 83=2, 84=3, 58=3, 78=2,

    A = np.array(g.graph)
    G = nx.from_numpy_array(A)

    subax1 = plt.subplot(121)
    nx.draw(G, with_labels=True, font_weight='bold')
    plt.show()

    g.primMST()
