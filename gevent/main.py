# coding=utf-8
import gevent
import time


def foo():
    time.sleep(1)
    print('Running in foo')
    gevent.sleep(0)
    print('Explicit context switch to foo again')


def bar():
    time.sleep(2)
    print('Explicit context to bar')
    gevent.sleep(0)
    print('Implicit context switch back to bar')


if __name__ == "__main__":
    gevent.spawn(foo)
    gevent.spawn(bar)
    print(1)
    time.sleep(5)
