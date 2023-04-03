import time

while True:
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    print(f"[local time] {time_str}\n")
    time.sleep(30)