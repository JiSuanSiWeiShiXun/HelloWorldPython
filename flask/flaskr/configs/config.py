# coding=utf-8

class Config():
    DEBUG = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:youling@172.17.0.1:3306/youling"
    MOGNO_URL = "mongodb://snake.testplus:snake.testplus@10.11.89.55:27017/project1?authSource=admin"
    MONGODB_SETTINGS = {
        'db': 'project1',
        'host': 'mongodb://10.11.89.55:27017/project1',
        'username': 'snake.testplus',
        'password': 'snake.testplus',
        'authentication_source': 'admin',
    }
