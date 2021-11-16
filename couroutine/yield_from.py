# coding=utf-8
"""
子生成器的yield返回给 外部调用的 for循环（__next__()函数）
最后子生成器函数调用结束，返回yield from语句
"""


# 子生成器
def test(n):
    i = 0
    while i < n:
        yield i
        i += 1


# 委派生成器
def test_yield_from(n):
    print("test_yield_from start")
    yield from test(n)  # 如果yield from后跟着一个非生成函数呢
    print("test_yield_from end")


for i in test_yield_from(3):
    print(i)