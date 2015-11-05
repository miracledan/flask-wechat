# -*- coding: utf-8 -*-

from flask import current_app, request, render_template
from app.exceptions import ValidationError
from . import main
from restful import Restful

# overwrite flask app error handler
@main.app_errorhandler(404)
def app_page_not_found(e):
    current_app.logger.error(e)
    response = Restful.page_not_found()
    return response

@main.app_errorhandler(405)
def app_method_not_allowed(e):
    current_app.logger.error(e)
    response = Restful.method_not_allowed()
    return response

@main.app_errorhandler(500)
def app_internal_server_error(e):
    current_app.logger.error(e)
    response = Restful.internal_server_error(e.message)
    return response


# process exception 'ValidationError'
@main.errorhandler(ValidationError)
def validation_error(e):
    current_app.logger.error(e)
    return Restful.bad_request(e.message) 

# @main.errorhandler(Exception)
# def validation_error(e):
#     current_app.logger.error(e)
#     return Restful.internal_server_error(e)