import math
import numpy as np
from scipy.optimize import linprog



def can_be_improved(tableau):
    z = tableau[-1]
    return any(x > 0 for x in z[:-1])


def propose_solution(tableau):
    columns = np.array(tableau).T
    solutions = []
    for column in columns[:-1]:
        solution = 0
        if is_basic_solution(column):
            one_index = column.tolist().index(1)
            solution = columns[-1][one_index]
        solutions.append(solution)

    return solutions


def is_basic_solution(column):
    return sum(column) == 1 and len([el for el in column if el == 0]) == len(column) - 1


def pivot_step(tableau, pivot_position):
    new_tableau = [[] for _ in tableau]

    i, j = pivot_position
    pivot_value = tableau[i][j]
    new_tableau[i] = np.array(tableau[i]) / pivot_value

    for eq_i, eq in enumerate(tableau):
        if eq_i != i:
            multiplier = np.array(new_tableau[i]) * tableau[eq_i][j]
            new_tableau[eq_i] = np.array(tableau[eq_i]) - multiplier

    return new_tableau


def get_pivot(tabl):
    z = tabl[-1]
    column = next(i for i, x in enumerate(z[:-1]) if x > 0)

    restrictions = []
    for eq in tabl[:-1]:
        el = eq[column]
        restrictions.append(math.inf if el <= 0 else eq[-1] / el)

    row = restrictions.index(min(restrictions))
    return row, column


def to_table(c, a, b):
    xb = [eq + [x] for eq, x in zip(a, b)]
    z = c + [0]
    return xb + [z]


def simplex(z_coefficient, matrix, b):
    table_form = to_table(z_coefficient, matrix, b)

    while can_be_improved(table_form):
        pivot = get_pivot(table_form)
        table_form = pivot_step(table_form, pivot)

    return propose_solution(table_form)


def get_f_value(c, x):
    res = 0
    for i in range(len(c)):
        res += c[i] * x[i]
    return res


c1 = [-2, 0, 1, -1, -2]

A1 = [[2, 0, 1, 0, 1],
      [2, 0, 0, 1, 0],
      [5, 1, 1, 0, 3], ]

b1 = [5, 3, 8]

result = simplex(c1, A1, b1)


for idx, x_value in enumerate(result):
    print(f'x_{idx} = {x_value}')

print(f'f={get_f_value(c1, result)}')
