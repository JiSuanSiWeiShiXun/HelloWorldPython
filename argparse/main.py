# coding=utf-8
"""
使用argparse 和 pyinstaller编译项目为二进制文件
"""
import sys
import argparse

from args import args, command
from pkg.pkg import hello_world


if __name__ == "__main__":
    if args.verbose:
        print("详细信息已启用")
    file_name = args.file_name
    number = args.number
    verbose = args.verbose
    x = args.x

    print("-f", file_name)
    print("-n", number)
    print("-v", verbose)
    print("-x", x)
    print("[command]", command)
    hello_world()
