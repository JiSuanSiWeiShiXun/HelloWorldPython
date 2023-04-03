# coding=utf-8
"""
用pygdbmi库操作gdb解析coredump文件, 支持的GDB版本: gdb 7.6+ has been tested. Older versions may work as well.
测试使用的GDB版本: GNU gdb (Debian 10.1-1.7) 10.1.90.20210103-git
"""
from pygdbmi.gdbcontroller import GdbController
from pygdbmi.constants import GdbTimeoutError
from pprint import pprint

def pygdb(game_exec_path: str,
          symbol_path: str, 
          coredump_path: str) -> str:
    coredump_path = "./147-coredump/core.6953"
    game_exec_path = "./147-coredump/GameServer"
    stack = ""
    try:
        gdbmi = GdbController(command=["gdb", game_exec_path, "-c", coredump_path], \
                            time_to_check_for_additional_output_sec=10)
        print("xxx", gdbmi.command)
        symbol_load_res = gdbmi.get_gdb_response(timeout_sec=60)
        print(symbol_load_res)
        print("*"*50)

        response = gdbmi.write("-bt full", timeout_sec=60)
        # pprint(response)
        for info in response:
            stack += info["payload"] + "\n"
        print(stack)
        return stack
    except Exception as e:
        print(f"loading symbol failed for {e}")

if __name__ == "__main__":
    pygdb()
