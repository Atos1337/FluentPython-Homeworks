import timeit
from multiprocessing import Process
from threading import Thread


def fib(n: int) -> list[int]:
    ans: list[int] = [0, 1]

    for i in range(n - 2):
        ans.append(ans[-1] + ans[-2])

    return ans[0:n]


def sync():
    for _ in range(10):
        fib(10000)


def threads():
    ts = []
    for _ in range(10):
        ts.append(Thread(target=fib, args=(10000,)))

    for t in ts:
        t.start()

    for t in ts:
        t.join()


def multiprocess():
    ps = []
    for _ in range(10):
        ps.append(Process(target=fib, args=(10000,)))

    for p in ps:
        p.start()

    for p in ps:
        p.join()


if __name__ == "__main__":
    with open("artifacts/easy.txt", 'w') as file:
        print(f"Sync time: {timeit.timeit(sync, number=1)}", file=file)
        print(f"Thread time: {timeit.timeit(threads, number=1)}", file=file)
        print(f"Process time: {timeit.timeit(multiprocess, number=1)}", file=file)
