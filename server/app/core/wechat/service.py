# -*- coding: utf-8 -*-

from flask import current_app, g
from wechat.official import WxApplication, WxTextResponse, WxMusic, WxMusicResponse
from app.utils import singleton
from app.exceptions import ServiceError


@singleton
class WechatService(WxApplication):
    SECRET_TOKEN = 'wechat'
    APP_ID = 'gh_825ced18df81'
    ENCODING_AES_KEY = 'tX5WJ1P2SG4U9Ye1bhdVVm4V3qNFpNiUM0cTvOceikc'

    def on_text(self, text):
        return WxTextResponse(text.Content, text)

wechatService = WechatService()
