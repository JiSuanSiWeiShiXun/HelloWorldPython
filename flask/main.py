# coding=utf-8
from flask_mongoengine import MongoEngine

from flaskr import create_app


app = create_app()
db = MongoEngine(app)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, processes=True)
