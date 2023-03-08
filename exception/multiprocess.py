# coding=utf-8
import json
import logging
import multiprocessing
import time

import requests

def get_cst(pid):
    logging.debug(f"process[{pid}] starts")
    time.sleep(10)
    # requests 多进程不安全，可能会导致读写错误，资源竞争
    resp = requests.get("https://worldtimeapi.org/api/timezone/Asia/Shanghai")
    time_info = json.loads(resp.content)
    logging.info(f"process[{pid}] gets utc: {time_info}")

def square(pid, num):
    logging.debug(f"process[{pid}] starts")
    time.sleep(3)
    logging.debug(f"process")
    return num*num

def concurrent_get_cst():
    with multiprocessing.Pool(processes=2) as pool:
        # 立即启动两个子进程，但交给子进程执行的函数逻辑，阻塞/同步执行
        # for i in range(2):
        #     pool.map(get_cst, [i]) 
        pool.map(get_cst, [1, 2])
        pool.join()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    concurrent_get_cst()
