# coding=utf-8
'''
@File    :   __init__.py
@Time    :   2024/03/17 18:03:19
@Author  :   youling 
@Contact :   xiezhihong@kingsoft.com
@Desc    :   None
'''
import logging

from werkzeug.local import LocalProxy
from flask import request, jsonify

from ..databases.mongodb import User


current_user = LocalProxy(lambda: _get_user())

class CurrentUser(object):
    """
    当前用户信息
    请求到达后端后, 在视图函数调用current_user时动态初始化
    """
    def __init__(self, uid: str, email: str):
        self.uid = uid
        self.email = email

def get_uid(email:str) -> str:
    """通过email获取uid"""
    return email.replace("@", "--").replace(".", "-")

def _get_user() -> CurrentUser :
    email = request.headers.get("K-USER-EMAIL")
    uid = get_uid(email)
    if not uid or not email:
        logging.error("header lack unauthentication info, maybe something wrong with gateway")
        raise Exception("user unauthenticated")
    
    if not User.objects(uid=uid).first(): # TODO(youling): redis缓存
        User(uid=uid, email=email).save()
    return CurrentUser(uid, email)

def _get_unauthenticated_view():
    return jsonify({"code": 1, "msg": "login required"}), 401