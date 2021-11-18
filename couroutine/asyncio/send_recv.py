# coding=utf-8
import asyncio
import concurrent.futures
import time
import socket


def recv_thread():
    """
    单独开启一个线程用于收包，貌似就不需要asyncio的event loop了
    :return:
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.get_event_loop().run_until_complete(recv())


async def recv():
    while True:
        print("假装收包")
        await asyncio.sleep(1)


async def wait_for_data():
    test_server = ("localhost", 9999)
    loop = asyncio.get_running_loop()

    reader, writer = await asyncio.open_connection(test_server[0], test_server[1])
    loop.call_soon(writer.write, "abc".encode())

    data = await reader.read(100)
    print(f"Receive data {data.decode()}")


def main():
    asyncio.wait(recv)
    for i in range(100):
        time.sleep(1)
        print("main func")


if __name__ == "__main__":
    main()
