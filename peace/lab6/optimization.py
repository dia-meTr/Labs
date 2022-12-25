import copy
import numpy as np


def target_function(point):
    x, y, z = point
    return -5 * x * (y ** 2) * z + 2 * (x ** 2) * y - 3 * x * (y ** 4) + x * (z ** 2)


def nelder_mead(f, x_start,
                step=0.1, no_improve_thr=60,
                no_improv_break=4, iterations=100,
                alpha=1., gamma=2.5, beta=-0.5, sigma=0.5):

    # init
    dim = len(x_start)
    prev_best = f(x_start)
    no_improv = 0
    res = [[x_start, prev_best]]

    for i in range(dim):
        x = copy.copy(x_start)
        x[i] = x[i] + step
        score = f(x)
        res.append([x, score])

    # simplex iter
    iters = 0
    while 1:
        # order
        res.sort(key=lambda x: x[1])
        best = res[0][1]

        # break after max_iter
        if iterations and iters >= iterations:
            return res[0][0], res[0][1], iters
        iters += 1

        # break after no_improv_break iterations with no improvement
        print(f'{iters}. ...best so far:{best}')

        if best < prev_best - no_improve_thr:
            no_improv = 0
            prev_best = best
        else:
            no_improv += 1

        if no_improv >= no_improv_break:
            return res[0][0], res[0][1], iters

        # centroid
        x0 = [0.] * dim
        for tup in res[:-1]:
            for i, c in enumerate(tup[0]):
                x0[i] += c / (len(res)-1)

        # reflection
        xr = x0 + alpha*(x0 - res[-1][0])
        rscore = f(xr)
        if res[0][1] <= rscore < res[-2][1]:
            del res[-1]
            res.append([xr, rscore])
            continue

        # expansion
        if rscore < res[0][1]:
            xe = x0 + gamma*(x0 - res[-1][0])
            escore = f(xe)
            if escore < rscore:
                del res[-1]
                res.append([xe, escore])
                continue
            else:
                del res[-1]
                res.append([xr, rscore])
                continue

        # contraction
        xc = x0 + beta * (x0 - res[-1][0])
        cscore = f(xc)
        if cscore < res[-1][1]:
            del res[-1]
            res.append([xc, cscore])
            continue

        # reduction
        x1 = res[0][0]
        nres = []
        for tup in res:
            redx = x1 + sigma*(tup[0] - x1)
            score = f(redx)
            nres.append([redx, score])
        res = nres


if __name__ == "__main__":
    distance = 1.
    alpha = 1.
    gamma = 2.6
    beta = 0.5
    sigma = 0.5

    point, function_value, iterations = nelder_mead(
        f=target_function,
        x_start=np.array((0., 1., 2.)),
        alpha=alpha,
        gamma=gamma,
        beta=beta,
        sigma=sigma,
        step=distance,
        iterations=0
    )

    print(f"Minimum value: F({round(point[0], 2)}, {round(point[1], 2)}, {round(point[2], 2)}) = {function_value}")
    print(f"Iterations: {iterations}")
