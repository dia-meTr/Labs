
def print_hi(name):
    matrix = [[0, 0, 0],
              [0, 0, 0],
              [0, 0, 0]]

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            print(matrix[i][j], end='')
            if j != len(matrix[i]) - 1:
                print(' | ', end='')
        if i != len(matrix) - 1:
            print('\n---------')


class Field:
    def __init__(self):
        self.matrix = [[0, 0, 0],
                       [0, 0, 0],
                       [0, 0, 0]]

    def draw(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                print(self.matrix[i][j], end='')
                if j != len(self.matrix[i]) - 1:
                    print(' | ', end='')
            if i != len(self.matrix) - 1:
                print('\n---------')

    def human_step(self, x, y):
        self.matrix[y][x] = 1
        self.draw()


    def comp_step(self):
        pass


if __name__ == '__main__':
    print_hi('PyCharm')
