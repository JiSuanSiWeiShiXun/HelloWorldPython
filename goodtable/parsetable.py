# coding=utf-8
"""
解析tab分隔的文件 转化为 csv文件
"""
import logging
import os
import pathlib
import tempfile

import pandas as pd
from charset_normalizer import from_path

def try_get_delimiter(csv_file, header_row):
    def getFileDelimiter(file):
        i = 0
        for row in file:
            i = i + 1
            if i == header_row:
                if row.find(',') > 0:
                    return ','
                elif row.find('\t') > 0:
                    return '\t'
                break
    try:
        pd.read_excel(csv_file)  # 判断是否为标准的xls 报错则是csv文件格式
    except Exception as xe:
        try:
            with open(csv_file, 'r', encoding="gbk") as delimfile:
                delimiter = getFileDelimiter(delimfile)
                if delimiter: return delimiter
        except UnicodeDecodeError as ue:
            with open(csv_file, 'r', encoding="utf8") as delimfile:
                delimiter = getFileDelimiter(delimfile)
                if delimiter: return delimiter
    return ','

# 将不同格式（xsl,tsv..）不同编码（gbk,gb9001...）的表文件转换成 utf-8 编码，','分隔，首行为header的csv文件，方便后续标准化处理
def copy_to_std_csv_file(project_name, path, header_row=1, skip_rows=None):
    name = pathlib.Path(path).stem
    fullname = pathlib.Path(path).name
    if not os.path.exists(path):
        logging.error("shit")
        open(path)
    else:
        raw_file_path = path
        is_temp_file = False
    delimiter = try_get_delimiter(csv_file=raw_file_path, header_row=header_row)
    temp_file = tempfile.NamedTemporaryFile(prefix=name + '_', suffix='.csv', delete=False)
    try:
        df = pd.read_excel(raw_file_path, 'Sheet1', index_col=0)
    except ValueError:
        try:
            # 转码为 utf-8
            best_encoding = from_path(raw_file_path).best().encoding
            df = pd.read_csv(raw_file_path, encoding=best_encoding, delimiter=delimiter, low_memory=False,
                             header=None)  # header为None，会生成数字为索引的表头
        except Exception:
            raise
    finally:
        if is_temp_file:
            os.remove(raw_file_path)
    df.columns = df.iloc[header_row - 1]  # 此时用第0行数据（也就是原表头）重新赋值为表头
    df.columns = df.columns.str.lower() # 修改表头数据，将英文变为小写
    df['rowIndex'] = pd.Series(['rowIndex'], index=[0])  # 增加'rowIndex'的列
    for index in range(len(df.iloc[:, 0])):
        df.loc[index, ['rowIndex']] = index + 1

    # df = df.reindex(df.index.drop(header_row - 1))  # 重新设置行号索引，避免影响行号记录
    skip_rows_include_header = [header_row]
    if skip_rows is not None:
        skip_rows_include_header.extend(skip_rows)
    drop_rows = [x - 1 for x in skip_rows_include_header]
    df.drop(index=drop_rows, inplace=True)
    df.to_csv(temp_file.name, index=False, header=True, encoding='utf_8')
    return pathlib.Path(temp_file.name).as_posix().__str__()
