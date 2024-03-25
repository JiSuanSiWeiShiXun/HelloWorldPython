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
import tempfile
import urllib.request
import os
from typing import Any, List
from datetime import datetime
from dateutil.parser import parse

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
        service_type: str, 
        nodes: List[str] = [],
        service_ip: str = None, 
        service_id: str = None,
    ):
    """
    获取月影日志分析数据
    @param st: 开始时间
    @param et: 结束时间
    @service_ip: 服务IP
    @service_type: 服务类型
    @node: 选择需要获取的信息指标
    @service_id: 服务ID
    """
    query_reference = {
        "FPS": ["fps"],
        "LoadInfo": ["loaded"],
        "SceneInfo": ["playerCount", "npcCount"]
    }
    # URL查询参数为空
    query = ''
    with open("test.data", "w", encoding="utf-8") as f:
        # 获取月影数据，以metrics格式写入.data文件
        for node in nodes:
            # HTTP POST body
            data = {
                "st": st,
                "et": et,
                "serviceType": service_type,
                "node": [node],
                # "serviceId": "publish_03_gs1_201010001",
            }
            if service_id:
                data["serviceId"] = service_id
            if service_ip:
                data["serviceIp"] = service_ip
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
            resp: dict = {}
            # http请求，最多重试3次
            max_attempts = 3
            for attempt in range(max_attempts):
                try:
                    # 发送HTTP请求
                    req = urllib.request.Request(url, data=body, headers=headers, method='POST')
                    with urllib.request.urlopen(req) as response:
                        resp: bytes = response.read()
                        # print(f"[{response.getcode()}] {resp.decode()}")
                        if response.getcode() != 200:
                            # logging.error("gpm request failed: [code] %s" % (response.getcode()))
                            continue # 继续重试
                        
                        resp: dict = json.loads(resp)
                        break
                except Exception as e:
                    print("gmp request [attempt] %d failed: [exception] %s" % (attempt, e))
                    time.sleep(1)
            if not resp or resp["code"] != 0:
                # logging.error("gpm request failed: [code] %s [resp] %s" % (content["code"], content))
                continue # 如果最后返回的信息出错，则跳过处理这个node
            
            datas: list = resp["data"]
            f.write(f"#TYPE {node} gauge\n")
            for data in datas:
                data: dict
                # print(data)
                # Convert the timestamp to a Unix timestamp
                timestamp = parse(data['timestamp']).timestamp()
                unix_timestamp = int(timestamp)
                # Write the data to the file
                for key in query_reference[node]:
                    value = data[key]
                    labelset = {
                        # {{groupname={data["ServiceType"]}:{data["serverId"]}",instance="{data["serviceIp"]}",job="prometheus"}}
                        "groupname": f'{data["ServiceType"]}:{data["serverId"]}',
                        "instance": data["serviceIp"],
                        "job": "prometheus",
                    }
                    if "sceneTemplateID" in data and data["sceneTemplateID"]:
                        labelset["sceneTemplateID"] = data["sceneTemplateID"]
                    if "sceneInstanceID" in data and data["sceneInstanceID"]:
                        labelset["sceneInstanceID"] = data["sceneInstanceID"]
                    if "lineID" in data and data["lineID"]:
                        labelset["lineID"] = data["lineID"]
                    labelset_str = "{" + ','.join([f'{k}="{v}"' for k, v in labelset.items()]) + "}"
                    f.write(f'snake_custom_{key}{labelset_str} {value} {unix_timestamp}\n')
        f.write("#EOF")
    
