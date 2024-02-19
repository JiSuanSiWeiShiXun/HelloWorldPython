# coding=utf-8
'''
@File    :   calling_demo_task.py
@Time    :   2024/02/05 10:13:56
@Author  :   youling 
@Contact :   xiezhihong@kingsoft.com
@Desc    :   None
'''

from demo.tasks import echo, search_yy_log_analysis_data, https_task

def invoke_search_yy_log_analysis_data():
    # 调用task方法
    search_yy_log_analysis_data.delay(
            "2024-02-05 00:00:00",
            "2024-02-05 23:59:59",
            ["10.11.69.123"],
            ["GameServer"],
            ["FPS"],           # node
            ["publish_03_gs1_201010001"] # service_id
        )
    # search_yy_log_analysis_data.apply_async(
    #     (
    #         "2024-02-05 00:00:00",
    #         "2024-02-05 23:59:59",
    #         "10.11.69.123",
    #         "GameServer",
    #     ),
    #     countdown=10
    # )

def invoke_https_task():
    # 调用task方法
    https_task.apply_async()
    

if __name__ == "__main__":
    # invoke_https_task()
    invoke_search_yy_log_analysis_data()
