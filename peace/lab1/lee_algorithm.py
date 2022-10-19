from collections import deque


class Cell:  # клас клітинки з її координатами
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Node: # клас вузла
    def __init__(self, pt: Cell, dist: int, parent):
        self.pt = pt  # координати клітини з вузлом
        self.dist = dist  # відстань від початку шляху
        self.parent = parent # батьківський вузол


def is_valid(row: int, col: int): # перевірка валідності координатів
    return (row >= 0) and (row < rows) and (col >= 0) and (col < cols)


def lee(mat, src: Cell, dest: Cell): # за вхідні дані приймаються координати початку та кінця алгоритму
    if mat[src.x][src.y] != 1 or mat[dest.y][dest.x] != 1: # перевірка чи не знаходиться початок та кінець шляху у стіні
        print(mat[src.x][src.y])
        print(mat[dest.x][dest.y])
        return -1

    visited = [[False for i in range(cols)] # створюємо матрицю відвіданих клітинок
               for j in range(rows)]

    visited[src.x][src.y] = True # початок шляху позначити відвіданим

    q = deque() # створюємо чергу для BFS

    s = Node(src, 0, None) # робимо вузол для початку шляху
    q.append(s) # та додаємо його до черги

    while q: # Доки черга не пуста продовжуємо цикл

        curr = q.popleft() # Дістаємо з черги елемент і далі працюємо з ним

        pt = curr.pt # координати поточного вузла
        if pt.x == dest.x and pt.y == dest.y: # перевірка чи поточний вузол не цільовий
            return curr # повертаємо поточний вузол з функції

        for i in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # цикл по 4 напрямках від поточного вузла
            row = pt.y + i[0] # координати сусіда поточного вузла
            col = pt.x + i[1]

            # Enqueue valid adjacent cell that is not visited
            if (is_valid(row, col) and
                    mat[row][col] == 1 and
                    not visited[row][col]): # перевірка чи ця клітинка не належить до стіни і чи вона ще не відвідана
                visited[row][col] = True # Позначаємо вищезгаданого сусіда як відвіданого
                Adjcell = Node(Cell(col, row),
                               curr.dist + 1, curr) # створюємо вузол для нього
                q.append(Adjcell) # і додаємо до черги

    return -1 # Якщо шлях не знайдено, повертаємо -1


def draw_maze(matrix, path): # малюємо лабіринт і знайдений шлях
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
                if (j, i) in path:
                    print(f'{j}{i} ', end='')
                else:
                    print(space * n, end='')
        print(wall * n)

    print(wall * n * (len(matrix[0]) + 2))

mat = [[1, 1, 1, 1, 0, 1, 1, 1, 1, 1], # матриця лабіринту
            [1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]


rows = len(mat)
cols = len(mat[0])

# визначаємо цільову і початкову клітинку
source = Cell(0, 0)
dest = Cell(7, 6)

path_node = lee(mat, source, dest) # запускаємо алгоритм Лі

if path_node.dist != -1: # Якщо довжина шляху не рівно -1(тобто шлях був знайдений)
    print("Length of the Shortest Path is", path_node.dist)
    path = [] # список для всіх координатів шляху
    while path_node:
        path.append((path_node.pt.x, path_node.pt.y)) # Додаємо до списку координати поточного вузла
        path_node = path_node.parent # робимо поточним батьківський вузол поточного
    path.reverse() # перевертаємо список
    print(path)
    draw_maze(mat, path) # малюємо лабіринт
else:
    print("Shortest Path doesn't exist")
