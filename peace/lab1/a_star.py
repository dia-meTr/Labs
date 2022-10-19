from copy import deepcopy
from collections import deque

closed = list()
open = list()


def contains(lis, node):
    for el in lis:
        if el.state == node.state:
            return True
    return False


target = [[0, 1, 2],
          [3, 4, 5],
          [6, 7, 8]]

# example =   [[1, 2, 5], [3, 0, 8], [6, 4, 7]]
example = [[1, 6, 4],
           [3, 2, 0],
           [8, 7, 5]]
# example = [[6, 2, 0], [5, 1, 3], [7, 4, 8]]
example = [[1, 3, 4],
           [0, 6, 2],
           [5, 7, 8]]


class Node:
    def __init__(self, state, parent_way):
        self.state = state
        self.to_end = self.H1()
        self.from_start = parent_way + 1
        self.childrens = []

    def is_target(self):
        if self.state == target:
            return True

        return False

    def children(self):
        childrens = []

        for i in range(0, 3):
            for j in range(0, 3):
                if self.state[i][j] == 0:
                    row = i
                    collumn = j
                    break

        self.left(row, collumn)
        self.right(row, collumn)
        self.up(row, collumn)
        self.down(row, collumn)

    def left(self, row, collumn):

        child = deepcopy(self.state)

        if collumn - 1 >= 0:
            child[row][collumn] = child[row][collumn - 1]
            child[row][collumn - 1] = 0

            self.childrens.append(Node(child, self.from_start))

            # all_nodes += 1

    def right(self, row, collumn):

        child = deepcopy(self.state)

        if collumn + 1 < 3:
            child[row][collumn] = child[row][collumn + 1]
            child[row][collumn + 1] = 0

            self.childrens.append(Node(child, self.from_start))

            # all_nodes += 1

    def up(self, row, collumn):

        child = deepcopy(self.state)

        if row - 1 >= 0:
            child[row][collumn] = child[row - 1][collumn]
            child[row - 1][collumn] = 0

            self.childrens.append(Node(child, self.from_start))

            # all_nodes += 1

    def down(self, row, collumn):

        child = deepcopy(self.state)

        if row + 1 < 3:
            child[row][collumn] = child[row + 1][collumn]
            child[row + 1][collumn] = 0

            self.childrens.append(Node(child, self.from_start))

            # all_nodes += 1

    def H1(self):
        count = 0

        for i in range(0, 3):
            for j in range(0, 3):
                if target[i][j] != self.state[i][j]:
                    count += 1

        return count

    def A(self):
        cur = open[0]
        while (open):
            cur = min(open, key=lambda x: x.to_end + cur.from_start)
            if contains(closed, cur):
                open.remove(cur)
                continue

            if cur.state == target: return cur.from_start

            open.remove(cur)
            closed.append(cur)

            cur.children()

            for el in cur.childrens:
                if not contains(open, el):
                    open.append(el)


if __name__ == '__main__':
    all_nodes = 1
    nodes_in_memory = 0

    temp = Node(example, -1)

    print(temp.state)

    open.append(temp)

    print(temp.A())

    print(len(open) + len(closed))

    for el in open:
        print(el.state)