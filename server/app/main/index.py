# -*- coding: utf-8 -*-

from flask import request, g, url_for
from app.core import wechatService
from app.exceptions import ServiceError
from . import main
from restful import Restful
import requests, json

APP_ID = 'wx62506c2e5e39536e'
ENCODING_AES_KEY = 'd4624c36b6795d1d99dcf0547af5443d'

def _request(method, url, **kwargs):
    if isinstance(kwargs.get("data", ""), dict):
        body = json.dumps(kwargs["data"], ensure_ascii=False)
        body = body.encode('utf8')
        kwargs["data"] = body

    print url
    r = requests.request(
        method=method,
        url=url,
        **kwargs
    )
    r.raise_for_status()
    response_json = r.json()
    return response_json

@main.route('/', methods=['GET', 'POST'])
def index():
    return wechatService.process(request.args, request.data)

@main.route('/wechat')
def oauth_login():
    code = request.args.get('code', type=str)
    print code
    url = 'https://api.weixin.qq.com/sns/oauth2/access_token'
    ret = _request('get', url, params = {'appid':APP_ID, 'secret':ENCODING_AES_KEY, 'code':code, 'grant_type':'authorization_code'})
    user = _request('get', 'https://api.weixin.qq.com/sns/userinfo', params = {'access_token':ret['access_token'], 'openid':ret['openid'], 'code':code, 'lang':'zh_CN'})
    print user
    return 'success'

