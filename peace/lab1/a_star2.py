

class Node():

    def __init__(self, parent=None, state=None):
        self.g = 0
        self.h = 0
        self.f = 0
        self.parent = parent
        self.state = state

    def __eq__(self, other):
        return self.state == other.state

    def count_g(self, node):
        if self.state[0] == self.parent.state[0] or self.state[1] == self.parent.state[1]:
            self.g = node.g + 10
        else:
            self.g = node.g + 14

    def count_h(self, end):
        self.h = (abs(self.state[0] - end.state[0]) + abs(self.state[1] - end.state[1])) * 10

    def count_f(self):
        self.f = self.g + self.h


def A(maze, start, end):

    open_list = []
    closed_list = []

    open_list.append(start)

    while open_list:

        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        open_list.pop(current_index)
        closed_list.append(current_node)

        if current_node == end:
            path = []
            current = current_node
            while current is not None:
                path.append(current.state)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            node_position = (current_node.state[0] + new_position[0], current_node.state[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 1:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.count_g(current_node)
            child.count_h(end)
            child.count_f()

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)


def draw_maze(matrix, path):
    wall = b'\xdb'.decode('cp437')
    space = ' '
    n = 3
    print(wall * n * (len(matrix[0]) + 2))
    for i in range(len(matrix)):
        print(wall * n, end='')
        for j in range(len(matrix[0])):
            if matrix[i][j] == 0:
                print(wall * n, end='')
            else:
                if (i, j) in path:
                    print(f'{j}{i} ', end='')
                else:
                    print(space * n, end='')
        print(wall * n)

    print(wall * n * (len(matrix[0]) + 2))


def main(begin, end):
    mat = [[1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
           [1, 0, 1, 0, 0, 1, 1, 1, 1, 1],
           [1, 0, 1, 1, 0, 1, 1, 1, 1, 1],
           [1, 0, 0, 1, 0, 1, 0, 1, 1, 1],
           [1, 1, 1, 1, 0, 0, 0, 1, 1, 1],
           [0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
           [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
           [0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
           [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
           [0, 0, 0, 1, 1, 1, 1, 1, 1, 1]]
    mat = [[1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

    start = Node(None, begin)
    end_ = Node(None, end)

    path = A(mat, start, end_)
    print(path)

    draw_maze(mat, path)


if __name__ == '__main__':
    main((0, 0), (7, 6))
