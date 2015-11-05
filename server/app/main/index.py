# -*- coding: utf-8 -*-

from flask import request, g, url_for
from app.core import wechatService
from app.exceptions import ServiceError
from . import main
from restful import Restful

@main.route('/', methods=['GET', 'POST'])
def index():
    return wechatService.process(request.args, request.data)

