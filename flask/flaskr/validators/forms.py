# coding=utf-8
from flask import request, json
from werkzeug.exceptions import HTTPException

class APIException(HTTPException):
    code = 500
    msg = u'sorry, we made a mistake (*￣︶￣)!'
    ret = 999

    def __init__(self, msg=None, code=None, ret=None, result=None, headers="application/json"):
        if code is not None:
            self.code = code
        if ret is not None:
            self.ret = ret
        if msg is not None:
            self.msg = msg
        self.headers = headers
        self.result = result
        super(APIException, self).__init__(msg, None)

    def get_body(self, environ=None, scope=None):
        """Get the HTML body."""
        body = dict(
            msg=self.msg,
            ret=self.ret,
            request=request.method + ' ' + self.get_url_no_param()
        )
        if self.result is not None:
            body["result"] = self.result
        return json.dumps(body)

    @staticmethod
    def get_url_no_param():
        full_path = str(request.full_path)
        main_path = full_path.split('?')
        return main_path[0]

    def get_headers(self, environ=None, scope=None):
        """Get a list of headers."""
        return [("Content-Type", self.headers)]

class Success(APIException):
    code = 200
    msg = u'ok'
    ret = 0