# coding=utf-8
"""
研究装饰器的执行时机：
1. 装饰器在导入模块时立即执行，完成对被修饰函数的替换
2. 而最里面那一层闭包需要在调用被修饰函数时才会执行，并且调用被修饰函数时，装饰器外层逻辑不再执行
"""
from functools import wraps

registry = []
def register(param=None):
    def wrapper(func):

        @wraps(func)
        def closure(*args, **kwargs):
            # 最里面这个closure()要在调用被修饰函数时才会执行，```func(xx)```
            print("calling closure %s, param %s" % (func.__name__, param))
            return func(*args, **kwargs)
        
        # 装饰器在导入模块时立即执行
        print("running register(%s)" % func.__name__)
        registry.append(func)
        return closure
    
    return wrapper

@register()
def f1():
    print("running f1")

@register()
def f2():
    print("running f2")

def f3():
    print("running f3")


if __name__ == "__main__":
    print("running main()")
    print("registry ->", registry)
    f1()
    f2()
    f3()
    print("registry ->", registry)