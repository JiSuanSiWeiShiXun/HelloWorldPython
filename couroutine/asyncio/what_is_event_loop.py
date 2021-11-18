# coding=utf-8

import asyncio
from concurrent import futures


def blocking_io():
    with open("text", "rb") as f:
        return f.read(100)


def cpu_bound():
    return sum(i * i for i in range(10 ** 7))


async def main():
    loop = asyncio.get_running_loop()

    # Run in default loop's executor
    result = await loop.run_in_executor(None, blocking_io)
    print(f"default thread pool {result}")

    # Run in custom thread pool
    with futures.ThreadPoolExecutor() as executor:
        result = await loop.run_in_executor(executor, blocking_io)
        print(f"custom thread pool {result}")

    # Run in custom process pool
    with futures.ProcessPoolExecutor() as executor:
        result = await loop.run_in_executor(executor, blocking_io)
        print(f"custom process pool {result}")

    print("你好")

if __name__ == "__main__":
    asyncio.run(main())
    print("你好")
