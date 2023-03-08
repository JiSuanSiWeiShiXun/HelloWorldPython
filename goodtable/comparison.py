# coding=utf-8
import logging
import pathlib

import parsetable

import pandas as pd

def compare_table():
    root = "/home/youling/goodtable/tables"
    std_path = "Settings/Table/UIImage.tab"
    cmp_path = "Settings/Table_Client/UIImage_Client.tab"

    # Step1: 将文件转为csv文件以便后续解析
    try:
        # std table
        # 读取schema数据，解析本地配置文件，转csv
        path = pathlib.Path(root).joinpath(std_path)
        header_row = 4 # 行数从1开始计
        skip_rows = [1,2,3]
        # 如果该文件在本地路径不存在
        std_csv_path = parsetable.copy_to_std_csv_file('mecha', path, header_row, skip_rows)
        # rule_content = rule_content.replace(name, csv_file)
        print(std_csv_path)

        # compared table
        # 读取schema数据，解析本地配置文件，转csv
        path = pathlib.Path(root).joinpath(cmp_path)
        header_row = 4 # 行数从1开始计
        skip_rows = [1,2,3]
        # 如果该文件在本地路径不存在
        cmp_csv_path = parsetable.copy_to_std_csv_file('mecha', path, header_row, skip_rows)
        # rule_content = rule_content.replace(name, csv_file)
        print(cmp_csv_path)
    except FileNotFoundError as e:
        logging.error(e)

    # Step 2: 读取文件并进行比对
    # std = pd.read_csv("UIImage_khsped5x.csv")
    # cmp = pd.read_csv("UIImage_Client_pye2yc56.csv")
    std = pd.read_csv("ruler_std.csv")
    cmp = pd.read_csv("ruler_cmp.csv")
    
    # Step 3: 预比对：比对表头，比对行数
    std_row_cnt, std_column_cnt = std.shape
    cmp_row_cnt, cmp_column_cnt = cmp.shape
    if std_row_cnt != cmp_row_cnt:
        raise Exception("行数不一致")
    if std_column_cnt != cmp_column_cnt:
        raise Exception("列数不一致")
        
    # Step 4: 比对内容
    # diff = std.compare(cmp) 默认比较方法遇到这个报错，我懒得看了，自己写个比较方法吧
    # ValueError: Can only compare identically-labeled DataFrame objects    
    columns = std.columns.to_list()
    for i, row in std.iterrows(): 
        for j, column_name in enumerate(columns):
            # 空单元格的值为NaN（类型float）
            # print(f"[row]{i} [column]{j} [column_name]{column_name} [unit]{row[column_name]} [type]{type(row[column_name])}") # 对于表头缺失的行无法判断
            # 比对单元格数据是否一致
            std_unit = str(row[column_name])
            cmp_unit = str(cmp.iloc[i, j])
            try:
                if std_unit != cmp_unit:
                    print(f"配置表 与原表 在第{i+1}行 第{j+1}列的数据不一致，列名{column_name}")
            except Exception as e:
                # 将错误加入队列
                pass

if __name__ == "__main__":
    compare_table()