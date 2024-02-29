# coding=utf-8
'''
@File    :   main.py
@Time    :   2024/02/20 14:44:36
@Author  :   youling 
@Contact :   xiezhihong@kingsoft.com
@Desc    :   从指定网站获取excel文件，处理excel文件中的内容得到目标格式的csv
'''
import re
from datetime import datetime, timedelta

import requests
import pandas as pd


def get_log_data(
    appkey: str,
    log_string: str,
    fromtime: str = (datetime.today() - timedelta(days=15)).strftime('%Y-%m-%d'), # "2024-02-19"
    totime: str = datetime.today().strftime('%Y-%m-%d'), # "2024-02-19"
    project_versions: str = None, # "0.7.0.426684"
) -> str:
    if fromtime > totime:
        raise Exception("fromtime should be less than totime.")

    # 获取CSV文件
    url = "https://logapi.testplus.cn/api/statistic/csv"
    payload = {
        "appkey": appkey, # "mecha",
        "from": 0,
        "size": 10,
        "fromtime": fromtime,
        "totime": totime,
        "merge_type": 0,
        "compare_with_project_version": "gte", # 大于等于
        "skip": 0,
        "log_string": log_string,
    }
    if project_versions:
        payload["project_versions"] = [project_versions] # 版本号
    response = requests.post(url, json=payload)
    filename = "original.xls"
    with open(filename, 'wb') as file:
        file.write(response.content)
    return filename

def process_log_string(xls_path: str):
    df = pd.read_excel(xls_path)

    # 定义一个函数来处理logstring列
    def process_logstring(logstring):
        shader_name = re.search(r'ShaderName: (.*?)   ', logstring).group(1)
        pass_type = re.search(r'PassType:(.*?)\n', logstring).group(1)
        keyword = re.search(r'Keywords:(.*?)   ', logstring).group(1)
        return pd.Series([shader_name, pass_type, keyword])

    # 处理logstring列
    df[['ShaderName', 'PassType', 'Keywords']] = df['log_string'].apply(process_logstring)
    # 删除不需要的列
    df = df.drop(['count', 'level', "log_string"], axis=1)
    # 去掉重复行
    df = df.drop_duplicates()
    # 写入新的CSV文件
    df.to_csv('processed.csv', index=False)


if __name__ == "__main__":
    original_csv_path = get_log_data(
        appkey="mecha",
        # fromtime="2024-02-19",
        # totime="2024-02-19",
        log_string="Keywords not perfectly matched. ShaderName:"
        # project_versions="0.7.0.426684",
    )
    process_log_string(original_csv_path)
