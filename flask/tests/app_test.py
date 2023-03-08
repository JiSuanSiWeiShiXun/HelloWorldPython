# coding=utf-8
import unittest

from flaskr import app, db
from flaskr.models import Object, User, Notify

from sqlalchemy.orm import Session

class TestDB(unittest.TestCase):
    # 这个函数在每个setUp之前都会执行
    def setUp(self):
        print("set up")

    def tearDown(self):
        print("tear down")

    def test_add_user(self):
        youling = User(
            name="youling",
        )
        db.session.add(youling)
        db.session.commit()

    # 添加物品数据时如何关联到已存在的对象？
    # 添加物品数据时如何新建一个不存在的对象，并关联之？
    """
    def test_add_object(self):
        youling = User(name="youling")
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
    """
    def test_delete(self):
        pass

    def test_query(self):
        pass

    def test_update(self):
        pass

if __name__ == "__main__":
    unittest.main()