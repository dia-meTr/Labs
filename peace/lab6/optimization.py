import numpy as np


def target_function(point):
    x, y, z = point
    return -5 * x * (y ** 2) * z + 2 * (x ** 2) * y - 3 * x * (y ** 4) + x * (z ** 2)


def nelder_optimizer(f, initial, no_improve_thr=10, alpha=1., gamma=2., beta=0.5, sigma=0.5, t=1., iterations=100):
    v1 = initial
    v2 = initial + np.array((t, 0, 0))
    v3 = initial + np.array((0, t, 0))

    target_optimal = initial
    prev_best = f(initial)
    no_improv = 0

    i = 0
    while True:
        weighted_points = [(v1, f(v1)), (v2, f(v2)), (v3, f(v3))]
        points = sorted(weighted_points, key=lambda x: x[1])

        target_optimal = points[0][0]
        g = points[1][0]
        w = points[2][0]
        middle = (g + target_optimal) / 2
        xr = middle + alpha * (middle - w)

        if iterations and i >= iterations:
            return target_optimal, f(target_optimal), i
        i += 1

        if f(target_optimal) < prev_best - no_improve_thr:
            no_improv = 0
            prev_best = f(target_optimal)
        else:
            no_improv += 1

        if no_improv >= 10:
            return target_optimal, f(target_optimal), i

        if f(xr) < f(g):
            w = xr
        else:
            if f(xr) < f(w):
                w = xr
            c = (w + middle) / 2
            if f(c) < f(w):
                w = c

        if f(xr) < f(target_optimal):
            xe = middle + gamma * (xr - middle)
            if f(xe) < f(xr):
                w = xe
            else:
                w = xr

        if f(xr) > f(g):
            xc = middle + beta * (w - middle)

            if f(xc) < f(w):
                w = xc

        v1 = w
        v2 = v1 + sigma * (g - v1)
        v3 = v1 + sigma * (target_optimal - v1)

    # return target_optimal, f(target_optimal)


if __name__ == "__main__":
    distance = 1.
    alpha = 1.
    gamma = 2.5
    beta = 0.5
    sigma = 0.5

    point, function_value = nelder_optimizer(
        f=target_function,
        initial=np.array((0., 1., 2.)),
        alpha=alpha,
        gamma=gamma,
        beta=beta,
        sigma=sigma,
        t=distance,
        iterations=0
    )

    print(f"Optimal point: ({round(point[0])}, {round(point[1], 2)}, {round(point[2], 2)})")
    print(f"Minimum value: F({round(point[0])}, {round(point[1], 2)}, {round(point[2], 2)}) = {round(function_value, 2)}")
    print(f"Iterations: 100")

