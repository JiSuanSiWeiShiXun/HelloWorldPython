# coding=utf-8
'''
@File    :   migrate_mysql_row.py
@Time    :   2024/03/25 17:12:58
@Author  :   youling 
@Contact :   xiezhihong@kingsoft.com
@Desc    :   迁移10.11.10.200:3307 dump_win32数据库中指定表中符合条件数据 到 目标数据库相同结构的表中
'''
import datetime
import mysql.connector

# 定义源数据库和目标数据库的连接参数
source_db_config = {
  'host': '10.11.10.200',
  'port': 3307,
  'user': 'dump',
  'password': 'dump@xsj.com',
  'database': 'dump_win32'
}

target_db_config = {
  'host': '10.11.11.145',
  'port': 3306,
  'user': 'root',
  'password': 'KinG3202@#SofTKing',
  'database': 'dump_win32'
}

# 定义要迁移的表
tables = [
  'statistic_dump',
  'statistic_dump_by_hour',
  'statistic_dump_key',
  'statistic_dump_machine',
  'statistic_dump_session',
  'statistic_dump_session_by_hour'
]

# 定义时间段
start_time = datetime.datetime.strptime('2022-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
end_time = datetime.datetime.strptime('2023-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')

# 创建源数据库和目标数据库的连接
source_db = mysql.connector.connect(**source_db_config)
target_db = mysql.connector.connect(**target_db_config)

source_cursor = source_db.cursor()
target_cursor = target_db.cursor()

# 定义每批处理的时间间隔，这里我们设为1小时
delta = datetime.timedelta(hours=24)

current_time = start_time
while current_time < end_time:
    next_time = min(current_time + delta, end_time)
    print(f"handling {current_time} - {next_time}")

    for table in tables:
        time_column = 'DumpDate'
        if table in ['statistic_dump_session', 'statistic_dump_session_by_hour']:
            time_column = 'Date'
        # 从源数据库查询指定时间段的数据
        query = f"SELECT * FROM {table} WHERE {time_column}>='{current_time}' AND {time_column}<'{next_time}'"
        source_cursor.execute(query)
        rows = source_cursor.fetchall()

        # 在插入数据之前，先删除目标数据库中指定时间段的数据
        delete_query = f"DELETE FROM {table} WHERE {time_column}>='{current_time}' AND {time_column}<'{next_time}'"
        target_cursor.execute(delete_query)
        # print(delete_query)

        # 将查询结果插入到目标数据库的相应表中
        for row in rows:
            placeholders = ', '.join(['%s'] * len(row))
            insert_query = f"INSERT INTO {table} VALUES ({placeholders})"
            target_cursor.execute(insert_query, row)
            # print(insert_query, row)
        target_db.commit()

    current_time = next_time
  
source_cursor.close()
target_cursor.close()
source_db.close()
target_db.close()