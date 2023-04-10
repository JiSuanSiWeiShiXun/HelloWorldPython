# coding=utf-8
import argparse
import sys

parser = argparse.ArgumentParser(description='这是对程序的描述')
# 命令行参数不支持用`-`分隔的参数名称 如file-name
parser.add_argument('-f', '--file_name', required=True, help='文件名')
parser.add_argument('-n', '--number', type=int, help='数字')
# store_true用于指定bool类型，指定后代表设置为true，否则默认为false
parser.add_argument('-v', '--verbose', action='store_true', help='详细信息')
parser.add_argument('-x', default="hooray", help="无法描述的选项")

args = parser.parse_args()
print(type(args))
print(isinstance(args, type))

# 获取完整的命令
command = ' '.join(sys.argv)
