# coding=utf-8
'''
@File    :   celery.py
@Time    :   2024/01/15 17:43:51
@Author  :   youling 
@Contact :   xiezhihong@kingsoft.com
@Desc    :   None
'''
from celery import Celery

app = Celery('demo',
             broker='amqp://rabbit:123456@10.11.89.55:5672',
            #  backend="redis://10.11.89.55:6370",
             include=['demo.tasks'])
app.conf.broker_connection_retry_on_startup = True

if __name__ == '__main__':
    app.start()
