# -*- coding: utf-8 -*-

from gevent import monkey; monkey.patch_all()

from werkzeug.contrib.fixers import ProxyFix
from app import create_app

app = create_app('product')

app.wsgi_app = ProxyFix(app.wsgi_app)