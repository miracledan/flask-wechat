# -*- coding: utf-8 -*-

from hashlib import sha1
from flask import current_app, g
from app.utils import singleton
from app.exceptions import ServiceError
from wechat_sdk import WechatBasic
from .crypt import WXBizMsgCrypt

TOKEN = 'wechat'
APP_ID = 'wx62506c2e5e39536e'
ENCODING_AES_KEY = 'd4624c36b6795d1d99dcf0547af5443d'

class WechatService(WechatBasic):
    UNSUPPORT_TXT = u'暂不支持此类型消息'
    WELCOME_TXT = u'你好！感谢您的关注！'

    menus = {
        "button": [
            {  
                "type":"click",
                "name":"推送消息",
                "key":"send_message"
            },
            {
                "name":"菜单",
                "sub_button": [
                    {    
                        "type":"view",
                        "name":"raindrop",
                        "url":"https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx62506c2e5e39536e&redirect_uri=http://www.yudianer.com/&response_type=code&scope=snsapi_base&state=123#wechat_redirect"
                    },
                    {    
                        "type":"view",
                        "name":"cevel",
                        "url":"https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx62506c2e5e39536e&redirect_uri=http://www.yudianer.com/&response_type=code&scope=snsapi_userinfo&state=123#wechat_redirect"
                    },
                    {    
                        "type":"view",
                        "name":"zhihu",
                        "url":"http://www.zhihu.com/"
                    }                    
                ]
            },
            {
                "name":"授权",
                "sub_button": [
                    {    
                        "type":"view",
                        "name":"base",
                        "url":"https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx62506c2e5e39536e&redirect_uri=http://www.yudianer.com/&response_type=code&scope=snsapi_base&state=123#wechat_redirect"
                    },
                    {    
                        "type":"view",
                        "name":"userinfo",
                        "url":"https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx62506c2e5e39536e&redirect_uri=http://www.yudianer.com/&response_type=code&scope=snsapi_userinfo&state=123#wechat_redirect"
                    }                  
                ]
            }            
        ]
    }



    def __init__(self, token=None, appid=None, appsecret=None, *args,  **kwargs):
        super(WechatService, self).__init__(token, appid, appsecret, *args, **kwargs)
        self.token = token
        self.app_id = appid
        self.aes_key = appsecret
        print self.create_menu(self.menus)

    def is_valid_params(self, params):
        timestamp = params.get('timestamp', '')
        nonce = params.get('nonce', '')
        signature = params.get('signature', '')
        echostr = params.get('echostr', '')

        sign_ele = [self.token, timestamp, nonce]
        sign_ele.sort()
        if(signature == sha1(''.join(sign_ele)).hexdigest()):
            return True, echostr
        else:
            return None

    def process(self, params, xml=None):
        ret = self.is_valid_params(params)

        if not ret:
            return 'invalid request'
        if not xml:
            # 微信开发者接入验证
            return ret[1]

        # 解密消息
        encrypt_type = params.get('encrypt_type', '')
        if encrypt_type != '' and encrypt_type != 'raw':
            msg_signature = params.get('msg_signature', '')
            timestamp = params.get('timestamp', '')
            nonce = params.get('nonce', '')
            if encrypt_type == 'aes':
                cpt = WXBizMsgCrypt(self.token,
                                    self.aes_key, self.app_id)
                err, xml = cpt.DecryptMsg(xml, msg_signature, timestamp, nonce)
                if err:
                    return 'decrypt message error, code : %s' % err
            else:
                return 'unsupport encrypty type %s' % encrypt_type

        self.parse_data(xml)
        req = self.get_message()

        func = self.handler_map().get(type(req).__name__, None)
        if not func:
            return self.response_text(content=self.UNSUPPORT_TXT)
        self.pre_process()
        rsp = func(req)
        self.post_process(rsp)

        # 加密消息
        if encrypt_type != '' and encrypt_type != 'raw':
            if encrypt_type == 'aes':
                err, rsp = cpt.EncryptMsg(rsp, nonce)
                if err:
                    return 'encrypt message error , code %s' % err
            else:
                return 'unsupport encrypty type %s' % encrypt_type
        return rsp

    def handler_map(self):
        if getattr(self, 'handlers', None):
            return self.handlers
        return {
            'TextMessage': self.on_text,
            'LinkMessage': self.on_link,
            'ImageMessage': self.on_image,
            'VoiceMessage': self.on_voice,
            'VideoMessage': self.on_video,
            'LocationMessage': self.on_location,
            'EventMessage': self.on_event,
        }

    def on_text(self, text):
        if text.content == 'user':
            openid = text.source
            return self.response_text(content=self.get_user_info(openid))
        return self.response_text(content=u'文字信息')

    def on_link(self, link):
        return self.response_text(content=u'链接信息')

    def on_image(self, image):
        return self.response_text(content=u'图片信息')

    def on_voice(self, voice):
        return self.response_text(content=u'语音信息')

    def on_video(self, video):
        return self.response_text(content=u'视频信息')

    def on_location(self, loc):
        return self.response_text(content=u'地理位置信息')

    def on_event(self, event):
        func = self.event_map().get(event.type, None)
        return func(event)

    def event_map(self):
        return {
            'subscribe': self.on_subscribe,
            'unsubscribe': self.on_unsubscribe,
            'scan': self.on_scan,
            'location': self.on_location_update,
            'click': self.on_click,
            'view': self.on_view,
            'scancode_push': self.on_scancode_push,
            'scancode_waitmsg': self.on_scancode_waitmsg,
            'pic_sysphoto': self.on_pic_sysphoto,
            'pic_photo_or_album': self.on_pic_photo_or_album,
            'pic_weixin': self.on_pic_weixin,
            'location_select': self.on_location_select,
        }

    def on_subscribe(self, event):
        return self.response_text(content=self.WELCOME_TXT)

    def on_unsubscribe(self, event):
        return self.response_text(content=self.WELCOME_TXT)

    def on_click(self, event):
        if event.key == 'send_message':
            self.send_template_message(event.source, 'ljIXlkv0iQ1DWSBiG75uLUT5-Rk5YwGgVxvIXwa2ZXA', 
                {
                   "first": {
                       "value":"恭喜你购买成功！",
                       "color":"#173177"
                   },
                   "product":{
                       "value":"巧克力",
                       "color":"#173177"
                   },
                   "billId":{
                       "value":"",
                       "color":"#173177"
                   },                   
                   "money": {
                       "value":"39.8元",
                       "color":"#173177"
                   },
                   "time": {
                       "value":"2014年9月22日",
                       "color":"#173177"
                   },
                   "remark":{
                       "value":"欢迎再次购买！",
                       "color":"#173177"
                   }                
                })
        return self.response_text(content=event.key)

    def on_scan(self, event):
        return self.response_text(content=self.WELCOME_TXT)

    def on_location_update(self, event):
        return self.response_text(content=self.WELCOME_TXT)

    def on_view(self, event):
        return self.response_text(content=self.WELCOME_TXT)

    def on_scancode_push(self, event):
        return self.response_text(content=self.WELCOME_TXT)

    def on_scancode_waitmsg(self, event):
        return self.response_text(content=self.WELCOME_TXT)

    def on_pic_sysphoto(self, event):
        return self.response_text(content=self.WELCOME_TXT)

    def on_pic_photo_or_album(self, event):
        return self.response_text(content=self.WELCOME_TXT)

    def on_pic_weixin(self, event):
        return self.response_text(content=self.WELCOME_TXT)

    def on_location_select(self, event):
        return self.response_text(content=self.WELCOME_TXT)

    def pre_process(self):
        pass

    def post_process(self, rsp):
        pass

wechatService = WechatService(token=TOKEN, appid=APP_ID, appsecret=ENCODING_AES_KEY)
