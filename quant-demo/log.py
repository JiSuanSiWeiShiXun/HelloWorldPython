# coding=utf-8
'''
@File    :   log.py
@Time    :   2024/03/15 11:04:17
@Author  :   youling 
@Contact :   xiezhihong@kingsoft.com
@Desc    :   None
'''
import os
import sys

from loguru import logger

# 控制是否输出到文件
to_file = True
log_dir = os.path.join(os.getcwd(), "logs")
os.makedirs(log_dir, exist_ok=True)
file_path = os.path.join(log_dir, "{time:YYYY-MM-DD_HH}.log") if to_file else None

# 设置日志格式
log_format = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> [<level>{level:4}</level>] <blue>[{name}|{file}.{function}:{line}]</blue> {message}"

# 添加处理器
logger.remove()
logger.add(sys.stdout, format=log_format, diagnose=False, backtrace=False)
if to_file:
    logger.add(file_path, format=log_format, diagnose=False, backtrace=False, rotation="50 MB", retention="1 day")

# # 使用日志
# def log_info(package, module, line, message):
#     logger.bind(package=package, module=module, line=line).info(message)
# # 示例
# log_info("my_package", "my_module", 123, "loginfo")

# logger.debug("hello world~")
# logger.info("hello world~")
# logger.warning("hello world~")
# logger.error("hello world~")