import concurrent.futures
import datetime
import math
import multiprocessing
import sys
import timeit

import matplotlib.pyplot as plt


def one_step_thread(x):
    print(f"Integrate_thread from {x[0] * x[2]} to {(x[0] + 1) * x[2]} in {datetime.datetime.now()}")
    return x[1](x[3] + x[0] * x[2]) * x[2]

def one_step_process(x):
    print(f"Integrate_process from {x[0] * x[2]} to {(x[0] + 1) * x[2]} in {datetime.datetime.now()}")
    return x[1](x[3] + x[0] * x[2]) * x[2]

def integrate_thread(f, a, b, *, n_jobs=1, n_iter=1000):
    print(f"Begin integrate_thread with n_jobs={n_jobs} in {datetime.datetime.now()}")
    acc = 0
    step = (b - a) / n_iter

    futures = None
    with concurrent.futures.ThreadPoolExecutor(max_workers=n_jobs) as executor:
        futures = executor.map(one_step_thread, map(lambda i: (i, f, step, a), range(n_iter)))

    for f in futures:
        acc += f

    print()
    return acc


def integrate_process(f, a, b, *, n_jobs=1, n_iter=1000):
    print(f"Begin integrate_process with n_jobs={n_jobs} in {datetime.datetime.now()}")
    acc = 0
    step = (b - a) / n_iter

    futures = None
    with concurrent.futures.ProcessPoolExecutor(max_workers=n_jobs) as executor:
        futures = executor.map(one_step_process, map(lambda i: (i, f, step, a), range(n_iter)))

    for f in futures:
        acc += f

    print()
    return acc


def integrate(f, a, b, *, n_jobs=1, n_iter=1000):
    acc = 0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc


if __name__ == "__main__":
    sys.stdout = open("artifacts/medium-log.txt", 'w')
    ps = []
    ts = []
    s = []
    for i in range(multiprocessing.cpu_count() * 2):
        ps.append(
            timeit.timeit(lambda: integrate_process(math.cos, 0, math.pi / 2, n_jobs=i + 1), number=1)
        )
        ts.append(
            timeit.timeit(lambda: integrate_thread(math.cos, 0, math.pi / 2, n_jobs=i + 1), number=1)
        )
        s.append(
            timeit.timeit(lambda: integrate(math.cos, 0, math.pi / 2, n_jobs=i + 1), number=1)
        )

    x = list(map(lambda i: i + 1, range(16)))
    plt.plot(x, ps, label="Process")
    plt.plot(x, ts, label="Thread")
    plt.plot(x, s, label="Sync")
    plt.legend()
    plt.xlabel("Number of jobs")
    plt.ylabel("Time in seconds")
    plt.savefig("artifacts/medium-plot.png")
    sys.stdout.close()
