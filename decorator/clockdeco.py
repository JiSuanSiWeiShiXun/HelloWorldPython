# coding=utf-8
import functools
import logging
import time 

# 如此实现的函数作为装饰器使用的时候，相当于将被修饰的函数func 替换成了 内部的闭包clocked
# 这样实现的装饰器有一些缺点：1.不支持关键字参数，2.将原函数func的__name__ 和 __doc__属性覆盖了
def clock(func):
    def clocked(*args):
        # 在被修饰函数执行前做的事
        t0 = time.perf_counter()
        result = func(*args)
        # 在被修饰函数执行后，增加的逻辑
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_str = ", ".join(repr(arg) for arg in args)
        logging.debug(f"[{round(elapsed, 8)}] {name}({arg_str}) -> {result}")
        return result
    return clocked

# 改进clock
# 用**kwargs支持关键字参数
# 用functools.wraps()防止原函数的属性覆盖
def clockV2(func):
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_lst = []
        if args:
            arg_lst.append(", ".join(repr(arg) for arg in args))
        if kwargs:
            pairs = [f"{k}={w}" for k, w in sorted(kwargs.items())]
            arg_lst.append(", ".join(pairs))
        arg_lst = ", ".join(arg_lst)
        logging.debug(f"[{round(elapsed, 8)}] {name}({arg_lst}) -> {result}")
        return result
    return clocked

