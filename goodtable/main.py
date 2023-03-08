# coding=utf-8
import json
import logging

import parsetable

import goodtables
import pandas as pd

schema = {'fields': [{'name': 'Name', 'constraints': {'pattern': '[\\u0021-\\u002f\\u003a-\\u0040\\u005b-\\u0060\\u007b-\\u007e]*'}}]}

def validate():
    report = goodtables.validate(
        "/home/youling/goodtable/ruler_ijt1ea55.csv", 
        schema=schema,
        checks=['pattern-constraint'],
        row_limit=100000,
        headers=1,
        skip_rows=[],
        encoding='utf_8'
    )
    print(json.dumps(report, indent="  "))

class Table(object):
    def __init__(self):
        self.relative_path = ""
        self.header_row = 1
        self.skip_rows = []

def compare_table(cmp_file:Table):
    root = "/home/youling/goodtable/tables"
    std_path = "Settings/Table/UIImage.tab"
    cmp_path = "Settings/Table_Client/UIImage_Client.tab"
    # 转化为csv
    name = f.get('table', 'Unknown')
    header_row = f.get('header_row', 1)
    skip_rows = f.get('skip_rows', [])
    path = name if proj_base == "" else Path(proj_base) / name
    if not path.exists():
        logging.error("file not found :%s" % path.absolute())
    # todo handle hardcode
    csv_file = parsetable.copy_to_std_csv_file('mecha', path, header_row, skip_rows)
    rule_content = rule_content.replace(name, csv_file)
    # 解析csv文件

def read_csv():
    # 先比较表头是否一致：忽略大小写（报warning）
    original = pd.read_csv("ruler_ijt1ea55.csv", header=1) # header默认将第0行设为表头
    compared_one = pd.read_csv()
    # print(original.head(5))
    """
    columns = original.columns.to_list()
    print(columns)
    # pandas.errors.ParserError: Error tokenizing data. C error: Expected 5 fields in line 7, saw 6
    # # i数据类型随以下情况变化
    # 1) int 表示行数
    # 2) str, int, tuple(当表头列少于数据列的时候，表头会自动向右对齐，左边多出来的数据会以元组的形式赋给i)
    for i, row in original.iterrows(): 
        print(f"type {type(i)}")
        for j, column_name in enumerate(columns):
            # 空单元格的值为NaN（类型float）
            print(f"[row]{i} [column]{j} [column_name]{column_name} [unit]{row[column_name]} [type]{type(row[column_name])}") # 对于表头缺失的行无法判断
        print("")
        # print("xx", row['col1'], row['col2'])
    """

    for i, row in original.iterrows():


if __name__ == "__main__":
    read_csv()