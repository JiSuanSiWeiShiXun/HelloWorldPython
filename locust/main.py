# coding=utf-8
'''
@File    :   main.py
@Time    :   2024/02/19 14:22:55
@Author  :   youling 
@Contact :   xiezhihong@kingsoft.com
@Desc    :   locust main file
'''
import sys
import logging

import gevent
from locust import HttpUser, TaskSet, SequentialTaskSet, task, constant
from locust.exception import StopUser
# from locust.speeder import register_speeder, wait_speeder


# register_speeder("start", 20)

class SequenceTasks(SequentialTaskSet):
    wait_time = constant(3)

    def on_start(self):
        logging.info("sequenceTasks start")
    
    def on_end(self):
        logging.info("sequenceTasks end")

    @task
    def step1(self):
        logging.info("step one")
        resp = self.client.get("/ping")
        logging.debug("[resp]", resp.text)

    @task
    def step2(self):
        logging.info("step two: interrupt")
        raise StopUser()


class Tasks(TaskSet):
    wait_time = constant(1)

    def on_start(self):
        logging.info("tasks start")
    
    def on_end(self):
        logging.info("tasks end")

    @task
    def stop(self):
        logging.info("interrupt")
        # self.interrupt(reschedule=False)
        raise StopUser()

    @task(10)
    def ping(self):
        resp = self.client.get("/ping")
        print("[resp]", resp.text)


class LoggedInUser(HttpUser):
    wait_time = constant(5)
    tasks = {
        Tasks: 1,
        SequenceTasks: 0,
    }

    # @task
    # def my_task(self):
    #     logging.info("user task")


if __name__ == "__main__":
    import locust.main

    logging.basicConfig(level=logging.DEBUG)
    # logging.basicConfig(level=logging.INFO)
    # logging.basicConfig(level=logging.ERROR)
    sys.argv.extend(["-f", __file__, "-H", "http://10.11.89.55:6789", "-r", "1", "-u", "1", '--web-host', "127.0.0.1", '--web-port', "9090", "--headless"])
    print(" ".join(sys.argv))
    locust.main.main()
