# coding=utf-8
"""
实现下列功能
1. 根据model定义新建数据库表
2. 根据需求修改数据库表定义
3. 实现数据的增删查改
"""
from sqlalchemy import create_engine
from flaskr.databases.models import Base

def add_object():
    pass

def delete_object():
    pass

def query_object():
    pass

def update_object():
    pass

if __name__ == "__main__":
    db = create_engine("mysql+mysqlconnector://root:youling@172.17.0.1:3306/youling", echo=True)
    print(type(db))
    
    Base.metadata.create_all(db) # 会创建以Base为基类的Model表
    print("shit")