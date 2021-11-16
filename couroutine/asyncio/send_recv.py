# coding=utf-8
import asyncio


async def recv():
    while True:
        await asyncio.sleep(1)
        print("假装收包")


def send():
    print("hello")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(recv())

    send()
    loop.run_forever()
