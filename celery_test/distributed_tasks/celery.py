# coding=utf-8
'''
@File    :   celery.py
@Time    :   2024/01/15 17:43:51
@Author  :   youling 
@Contact :   xiezhihong@kingsoft.com
@Desc    :   None
'''
from celery import Celery

app = Celery('distributed_tasks',
             broker='amqp://10.11.89.55:5672',
             backend='rpc://',
             include=['app.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()
