# coding=utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy, BaseQuery
from flask_migrate import Migrate

# from .blueprint import bp
from .api.user import mod as user_mod


tmp = "nice"
db = SQLAlchemy(query_class=BaseQuery)
migrate = Migrate()

def create_app():
    # global tmp, db, migrate
    tmp = "fuck away"
    # 初始化db
    app = Flask(__name__)
    app.config.from_object("flaskr.configs.config.DevConfig")

    from flaskr.databases import models
    db.init_app(app) # 初始化mysql句柄
    migrate.init_app(app, db) # 初始化mysql迁移工具
    # export FLASK_APP=flaskr

    # app.register_blueprint(bp)
    app.register_blueprint(user_mod)

    return app