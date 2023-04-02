# coding=utf-8
"""
一个参数化的装饰器
"""
import logging
from functools import wraps

def use_logging(level):
    """decorator"""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if level == "warn":
                logging.warning("%s is running", fn.__name__)
            return fn(*args, **kwargs)
        return wrapper
    return decorator

@use_logging(level="warn")
def foo(name="foo"):
    """a random function"""
    print(f"i'm not {name}")

if __name__ == "__main__":
    foo()
