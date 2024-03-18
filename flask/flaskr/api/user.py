# coding=utf-8
'''
@File    :   user.py
@Time    :   2024/03/17 17:59:54
@Author  :   youling 
@Contact :   xiezhihong@kingsoft.com
@Desc    :   None
'''

from flask import Blueprint, jsonify

from ..databases.mongodb import User
from ..auth import current_user
from ..auth.decorator import login_required


mod = Blueprint('@user', __name__)

@mod.route("/info", methods=["GET"])
@login_required
def current_user_info():
    """user info"""
    user: User = User.objects(uid=current_user.uid).first()
    return jsonify({"code": 0, "msg": "success", "data": {"uid": user.uid, "email": user.email, "personal_git_token": user.git_token}})
