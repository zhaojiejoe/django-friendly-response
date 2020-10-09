# -*- coding: utf-8 -*-
from itsdangerous import TimedJSONWebSignatureSerializer
from weixin import WXAPPAPI
from weixin.lib.wxcrypt import WXBizDataCrypt
from django.conf import settings
import random
import string

APPID = getattr(settings, 'WECHATMINI_APPID', 'wxf9d646f2fc2fec92')
SECRET = getattr(settings, 'WECHATMINI_SECRET', '5832053aee6c904bf37b8a4dba6cf534')


class WMPCService(object):

    def __init__(self, appid=APPID, app_secret=SECRET):
        self.appid = appid
        self.api = WXAPPAPI(appid=appid, app_secret=app_secret)

    def get_openid_skey(self, code):
        return self.api.exchange_code_for_session_key(code=code)

    def get_encrypted_data(self, session_key, encrypted_data, iv):
        crypt = WXBizDataCrypt(self.appid, session_key)
        return crypt.decrypt(encrypted_data, iv)

    @staticmethod
    def encode_openid_skey(openid, session_key):
        # 用OpenId加密生成3rdsession
        # 默认过期时间3600
        s = TimedJSONWebSignatureSerializer(settings.SECRET_KEY)
        third_session = s.dumps({'openid': openid, 'session_key': session_key})
        return third_session

    @staticmethod
    def decode_openid_skey(thirdsession):
        # 用3rdsession解密生成OpenId
        s = TimedJSONWebSignatureSerializer(settings.SECRET_KEY)
        encrypted = s.loads(thirdsession)
        return encrypted['openid'], encrypted['session_key']

    @staticmethod
    def gen_password(default_bit=12):
        return ''.join(random.sample(string.ascii_letters + string.digits, default_bit))

