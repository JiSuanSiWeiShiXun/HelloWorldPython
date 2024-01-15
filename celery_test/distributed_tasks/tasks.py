# coding=utf-8
'''
@File    :   tasks.py
@Time    :   2024/01/15 17:28:20
@Author  :   youling 
@Contact :   xiezhihong@kingsoft.com
@Desc    :   None
'''
from typing import Any
from datetime import datetime

from .celery import app

@app.tasks
def echo(obj: Any):
    print(f"[echo] [{datetime.now()}] {obj}")
