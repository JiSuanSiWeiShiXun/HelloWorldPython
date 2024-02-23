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
    # search_yy_log_analysis_data.delay(
    #         "2024-02-22 11:23:29", # "2024-01-30 09:44:26",
    #         "2024-02-22 11:38:29", # "2024-01-30 09:59:26",
    #         ["GameServer"],
    #         ["fps", "LoadInfo", "SceneInfo"],           # node
    #         ["10.11.69.124"],
    #         ["gs_10001_10.11.69.124"], # ["publish_04_gs1_201010001"] # service_id
    #     )
    result = search_yy_log_analysis_data.apply_async(
        (
            "2024-02-21T19:25:47.215+00:00",
            "2024-02-21T19:36:06.728+00:00",
            ["GameServer"],
            ["fps", "LoadInfo", "SceneInfo"],           # node
            # ["10.11.69.124"],
            # ["gs_10001_10.11.69.124"], # ["publish_04_gs1_201010001"] # service_id
        ),
        countdown=10
    )
    # task_result = result.get()
    # print(task_result)

def invoke_https_task():
    # 调用task方法
    https_task.apply_async()
    

if __name__ == "__main__":
    # invoke_https_task()
    invoke_search_yy_log_analysis_data()
