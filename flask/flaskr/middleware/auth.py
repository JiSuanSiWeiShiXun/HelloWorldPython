# coding=utf-8
import jwt
from flask import request, jsonify

class JWTRequiredMiddleware(object):
    def __init__(self, app):
        self.app = app
        self.secret = 'secret-key'  # Replace with your secret key

    def __call__(self, environ, start_response):
        # Get the JWT token from the authorization header
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                # Decode the JWT token
                token = auth_header.split(' ')[1]
                decoded_token = jwt.decode(token, self.secret, algorithms=['HS256'])

                # Add the decoded token to the request
                request.jwt = decoded_token
            except jwt.exceptions.DecodeError:
                # If the token is invalid, return a 401 Unauthorized error
                return jsonify({'error': 'Unauthorized'}), 401

        response = self.app(environ, start_response)

        return response