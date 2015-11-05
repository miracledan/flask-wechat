# -*- coding: utf-8 -*-

from flask import current_app, g
from wechat.official import WxApplication, WxTextResponse, WxMusic, WxMusicResponse, WxApi
from app.utils import singleton
from app.exceptions import ServiceError


@singleton
class WechatService(WxApplication):
    SECRET_TOKEN = 'wechat'
    APP_ID = 'wx62506c2e5e39536e'
    ENCODING_AES_KEY = 'd4624c36b6795d1d99dcf0547af5443d'
    menus = {
        "button": [
            {  
              "type":"click",
              "name":"今日歌曲",
              "key":"V1001_TODAY_MUSIC"
            },
            {
                "name":"菜单",
                "sub_button": [
                    {    
                       "type":"view",
                       "name":"搜索",
                       "url":"http://www.soso.com/"
                    },
                    {
                       "type":"view",
                       "name":"视频",
                       "url":"http://v.qq.com/"
                    },
                    {
                       "type":"click",
                       "name":"赞一下我们",
                       "key":"V1001_GOOD"
                    }
                ]
            }
        ]
    }

    def __init__(self):
        self.api = WxApi(self.APP_ID, self.ENCODING_AES_KEY)
        ret, error = self.api.create_menu(self.menus)
        if ret is None:
            print '%s,%s' % (error.code, error.message)

    def on_text(self, text):
        openid = text.FromUserName
        print openid
        print self.api.user_info(openid)
        return WxTextResponse(text.Content, text)

wechatService = WechatService()
