# coding=utf-8
'''
@File    :   decorator.py
@Time    :   2024/03/17 18:08:57
@Author  :   youling 
@Contact :   xiezhihong@kingsoft.com
@Desc    :   None
'''
import logging
from functools import wraps

from flask import request

from . import _get_unauthenticated_view


def login_required(fn):
    """
    重写flask鉴权流程中的@login_required,
    在flask中用于验证用户是否登录, 要求在请求头中携带auth信息
    登录流程移到网关之后，这个装饰器没有用了
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        email = request.headers.get("K-USER-EMAIL")
        uid = request.headers.get("K-USER-UID")
        if not email or not uid:
            return _get_unauthenticated_view()
        logging.debug(f"[current_user] [email]{email} [uid]{uid}")
        return fn(*args, **kwargs)
    return wrapper