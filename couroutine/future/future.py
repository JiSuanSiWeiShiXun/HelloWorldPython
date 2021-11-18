# coding=utf-8
"""
多线程/多进程 作为执行单元，执行I/O阻塞的
"""
from concurrent import futures
import time
import os

MAX_WORKERS = 5
NUMBER_LIST = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def waste_time(x):
    # print("pid: ", os.getpid())
    # 这个写法真的是毫无意义，只为浪费时间
    # 每次迭代i会从__next__()返回的迭代器中得到新值n，随后又被赋值为n+1；
    # 最终i的值为range范围的极大值+1；
    for i in range(0, 10000000):
        i = i + 1
    ret = i * x
    return ret


if __name__ == "__main__":
    # 顺序执行
    s = time.time()
    for num in NUMBER_LIST:
        waste_time(num)
    print(f"sequential program spent {time.time() - s} s.")

    # 线程池
    s = time.time()
    executor = futures.ThreadPoolExecutor()
    future_list = [executor.submit(waste_time, arg) for arg in NUMBER_LIST]
    for future in futures.as_completed(future_list):
        print(future.result())
    print(f"multi-thread program spent {time.time() - s} s.")

    # 进程池
    future_list = []
    s = time.time()
    executor = futures.ProcessPoolExecutor(max_workers=MAX_WORKERS)
    for num in NUMBER_LIST:
        future_list.append(executor.submit(waste_time, num))    # 返回Future()
    for future in futures.as_completed(future_list, timeout=10):
        print(future.result(), type(future.result()))
    print(f"multi_process program spent {time.time() - s} s")
