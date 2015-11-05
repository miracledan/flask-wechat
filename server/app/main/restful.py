# -*- coding: utf-8 -*-

from flask import jsonify
from functools import wraps

def jsonify_status_code(status_code):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            response = jsonify(f(*args, **kwargs))
            response.status_code = status_code
            return response
        return wrapper
    return decorator

class Restful(object):
    @staticmethod
    @jsonify_status_code(200)
    def ok(message={'msg': 'success'}):
        return message

    @staticmethod
    @jsonify_status_code(201)
    def created(message={'msg': 'success'}):
        return message

    @staticmethod
    @jsonify_status_code(204)
    def no_content(message={'msg': 'success'}):
        return message

    @staticmethod
    @jsonify_status_code(400)
    def bad_request(message=None):
        return {'msg': message}

    # please avoid use this method, because browser will alert 
    # login by recv status 401
    @staticmethod
    @jsonify_status_code(401)
    def unauthorized(message=None):
        return {'msg': message}

    @staticmethod
    @jsonify_status_code(403)
    def forbidden(message=None):
        return {'msg': message}

    @staticmethod
    @jsonify_status_code(404)
    def page_not_found(message=None):
        return {'msg': message}

    @staticmethod
    @jsonify_status_code(405)
    def method_not_allowed(message=None):
        return {'msg': message}

    @staticmethod
    @jsonify_status_code(500)
    def internal_server_error(message=None):
        return {'msg': message}