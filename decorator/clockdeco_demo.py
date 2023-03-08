# coding=utf-8
import time
import logging
from clockdeco import clock, clockV2

# @clock
@clockV2
def to_be_decorated(name="someone", age="25"):
    return(f"{name} aged {age} worth not even a penny.")

@clock
def snooze(p):
    time.sleep(p)

@clock
def factorial(n):
    return 1 if n==1 else n*factorial(n-1)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    print("*"*40, "Calling snooze")
    snooze(.234)
    print("*"*40, "Calling fatorial")
    factorial(6)
    print("*"*40, "Calling to_be_decorated")
    to_be_decorated(age="35")