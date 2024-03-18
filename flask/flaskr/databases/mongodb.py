# coding=utf-8
'''
@File    :   mongodb.py
@Time    :   2024/03/17 17:30:58
@Author  :   youling 
@Contact :   xiezhihong@kingsoft.com
@Desc    :   None
'''
import uuid
from mongoengine import Document, StringField, BooleanField, DateTimeField


class User(Document):
    uid = StringField(primary_key=True, default=lambda: uuid.uuid4().hex[:12])
    email = StringField(max_length=255, unique=True)
    password = StringField(max_length=255)
    active = BooleanField(default=True)
    confirmed_at = DateTimeField()
    git_token = StringField(max_length=255)

    meta = {
        'indexes': ['email'],
        'index_background': True,
    }
