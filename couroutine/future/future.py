# coding=utf-8
from concurrent import futures
import time

MAX_WORKERS = 20
NUMBER_LIST = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def waste_time(x):
    # 这个写法真的是毫无意义，只为浪费时间
    # 每次迭代i会从__next__()返回的迭代器中得到新值n，随后又被赋值为n+1；
    # 最终i的值为range范围的极大值+1；
    for i in range(0, 10000000):
        i = i + 1
    print(i * x)


if __name__ == "__main__":
    # 顺序执行
    s = time.time()
    for num in NUMBER_LIST:
        waste_time(num)
    print(f"sequential program spent {time.time() - s} s.")

    # 线程池
    s = time.time()
    executor = futures.ThreadPoolExecutor()
    executor.map(waste_time, NUMBER_LIST)
    print(f"multi-thread program spent {time.time() - s} s.")

    # 进程池
    s = time.time()
    executor = futures.ProcessPoolExecutor()
    executor.map(waste_time, NUMBER_LIST)
    print(f"multi_process program spent {time.time() - s} s")
