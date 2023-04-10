# coding=utf-8
"""
使用argparse 和 pyinstaller编译项目为二进制文件
"""
import argparse

parser = argparse.ArgumentParser(description='这是对程序的描述')
parser.add_argument('-f', '--file', help='文件名')
parser.add_argument('-n', '--number', type=int, help='数字')
parser.add_argument('-v', '--verbose', action='store_true', help='详细信息')

args = parser.parse_args()

if __name__ == "__main__":
    if args.verbose:
        print("详细信息已启用")
    print(args.file)
