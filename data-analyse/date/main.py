# coding=utf-8
'''
@File    :   main.py
@Time    :   2024/02/27 10:21:30
@Author  :   youling 
@Contact :   xiezhihong@kingsoft.com
@Desc    :   计算指定日期是 从2022.11.04（星期五）算起的第几周（周一作为一周的开始）
'''
from datetime import datetime, timedelta

# 定义起始日期和目标日期
start_date = datetime.strptime('2022-10-31', '%Y-%m-%d')
target_date = datetime.strptime('2024-02-27', '%Y-%m-%d')

# 计算两个日期之间的天数
days_diff = (target_date - start_date).days

# 计算周数和星期数
weeks, weekday = divmod(days_diff, 7)

# 代码的weeks从0开始计算，人为的weeks从1开始计算，所以需要加1
weeks += 1

# 星期数从0开始，0代表星期一，所以需要加1
weekday += 1

print(f'The target date is the {weeks}th week, and the {weekday}th day of the week.')
