# coding=utf-8
"""
通过协程以动画形式显示文本式旋转指针
"""

import asyncio
import itertools
import sys
import time


async def supervisor():
    spinner = asyncio.ensure_future(spin("thinking!"))
    # print(f"spinner(Task) object: {spinner}")
    result = await slow_function()
    spinner.cancel()
    return result


async def spin(msg):
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))
        try:
            await asyncio.sleep(.1)
        except asyncio.CancelledError:
            break
    write(' ' * len(status) + '\x08' * len(status))


async def slow_function():
    # 假装等待I/O一会儿
    await asyncio.sleep(3)
    return 42

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(supervisor())
    loop.close()
    print(f"Answer: {result}")

