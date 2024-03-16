# coding=utf-8
'''
@File    :   main.py
@Time    :   2024/03/15 10:57:41
@Author  :   youling 
@Contact :   youling15122511@gmail.com
@Desc    :   None
'''

import rqdatac
from loguru import logger

if __name__ == "__main__":
    rqdatac.init(username="user_512811", password="Whiplash31415926")
    logger.info(rqdatac.info())
    logger.debug(rqdatac.user.get_quota())
