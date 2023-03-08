# coding=utf-8
import logging

from flaskr import tmp, db
from flaskr.databases.models import User, Object
from flaskr.validators.forms import Success

from flask import Blueprint

bp = Blueprint('test', __name__)

@bp.route("/ping")
def pong():
    return "pong~"

@bp.route("/test/flask-sqlalchemy/add")
def db_add():
    logging.debug("shit")
    youling = User(
        name="youling",
    )
    db.session.add(youling)
    db.session.commit()
    return Success(result={"hello": "world"})

@bp.route("/test/flask-sqlalchemy/add-object")
def test_add_object():
    # 如此：添加物品数据时如何新建一个不存在的user对象，并关联之
    youling = User(name="xiezhh")
    # 如此：添加物品数据时如何关联到已存在的对象
    youling = db.session.query(User).filter_by(name="youling").first()
    macbook = Object(
        name="Macbook pro 14' 21",
        count=1,
        desc="工作第三年双十一换的笔记本",
        owner=youling,
    )
    iphone = Object(
        name="iPhone 11",
        count=1,
        desc="工作第一年双十一买的手机",
        owner=youling,
    )
    db.session.add_all([macbook, iphone])
    db.session.commit()
    return Success()

def test_delete():
    pass

@bp.route("/test/flask-sqlalchemy/query")
def test_query():
    print(tmp)
    user = db.session.query(User).filter_by(name="youling").first()
    print(user)
    return Success()

def test_update():
    pass