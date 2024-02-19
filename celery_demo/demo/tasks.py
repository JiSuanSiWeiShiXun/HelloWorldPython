# coding=utf-8
'''
@File    :   tasks.py
@Time    :   2024/01/15 17:28:20
@Author  :   youling 
@Contact :   xiezhihong@kingsoft.com
@Desc    :   None
'''
import json
import time
import urllib.request
from typing import Any
from datetime import datetime

from .celery import app
from .sign import tc_build_sign

import requests


@app.task
def echo(obj: Any):
    print(f"[echo] [{datetime.now()}] {obj}")

@app.task
def https_task():
    url = "https://www.baidu.com"
    resp = requests.get(url)
    print(resp.text)

@app.task
def search_yy_log_analysis_data(
        st: str,
        et: str,
        service_ip: str, 
        service_type: str, 
        node: str = None, 
        service_id: str = None,
    ):
    """获取月影日志分析数据"""
    # URL查询参数为空
    query = ''

    # HTTP POST body
    data = {
        "st": st,
        "et": et,
        "serviceIp": service_ip,
        "serviceType": service_type,
        # "serviceId": "publish_03_gs1_201010001",
        # "node": "SceneInfo",
    }
    if node:
        data["node"] = node
    if service_id:
        data["serviceId"] = service_id
    body = json.dumps(data)

    # 时间戳
    tonce = str(int(time.time()))

    # 构造签名
    key = "test_center"
    secret = "123e4567e89b12d3a4564266141740"
    sign = tc_build_sign(secret, tonce, query, body)

    # GPM接口地址
    project = "app_200001406"
    url = f"https://tech-dev.seasungame.com/log_search/api_v2/{project}/yy/log_analysis"

    # 签名参数通过HTTP header传递
    headers = {
        'Content-Type': 'application/json',
        'xsjtc-sign-ver': 'v1',
        'xsjtc-sign-tonce': tonce,
        'xsjtc-sign-key': key,
        'xsjtc-sign': sign,
    }

    if body is not None:
        body = body.encode('utf-8')

    print(f"[url] {url}")
    print(f"[data] {data}")
    # 发送HTTP请求
    req = urllib.request.Request(url, data=body, headers=headers, method='POST')
    with urllib.request.urlopen(req) as response:
        content = response.read()
        print(f"[{response.getcode()}] {content.decode()}")

