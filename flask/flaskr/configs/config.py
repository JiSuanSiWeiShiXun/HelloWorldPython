# coding=utf-8

class Config():
    DEBUG = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:youling@172.17.0.1:3306/youling"
