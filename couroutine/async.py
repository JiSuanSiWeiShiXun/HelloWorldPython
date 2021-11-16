# coding=utf-8

import asyncio


async def compute(x, y):
    print(f"compute {x} + {y} ...")
    await asyncio.sleep(1.0)   # 这个子生成器怎么还在yield from —— sleep函数里调用了await？ eventLoop里延迟了1s后继续执行
    return x + y


async def print_sum(x, y):
    result = await compute(x, y)
    print(f"{x}+{y}={result}")


loop = asyncio.get_event_loop()
print("start")
loop.run_until_complete(print_sum(1, 2))
print("end")
loop.close()

