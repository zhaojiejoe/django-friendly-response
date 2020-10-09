from dingtalk import AppKeyClient, SecretClient
from dingtalk.client.api import User as DUser
from dingtalk.client.api import Message as DMsessage
from dingtalk.model.message import TextBody, LinkBody
from django.conf import settings

CORP_ID = getattr(settings, "DINGTALK_CORP_ID", "270790861")
APP_KEY = getattr(settings, "DINGTALK_APP_KEY", "ding7geqf0ejkxt8f6gj")
APP_SECRET = getattr(settings, "DINGTALK_APP_SECRET", "_Ixl3zDQ_GL_SDSX815L7UUTs_mhp8qm17BRUU15PFTI9jEfae_JD5nIpbfTWdFi")


class AKCService(object):

    def __init__(self, corp_id=CORP_ID, app_key=APP_KEY, app_secret=APP_SECRET, storage=None):
        # 原始的AppKeyClient初始化有9个参数，lint会报错，这边只保留了部分关键参数
        self.client = AppKeyClient(CORP_ID, APP_KEY, APP_SECRET, storage=storage)
        self.duser = DUser(self.client)
        self.dmessage = DMsessage(self.client)

    def gen_text_body(self, content, **kwargs):
        return TextBody(content)

    def gen_link_body(self, message_url, pic_url, title, text, **kwargs):
        return LinkBody(message_url, pic_url, title, text)

    def send_message(self, msg_body, agent_id=CORP_ID, userid_list=(), dept_id_list=(), to_all_user='false'):
        # 相同的数据一天只能发一次,可以加时间戳
        self.dmessage.asyncsend_v2(msg_body, agent_id, userid_list, dept_id_list, to_all_user)

    def get_user_id(self, code):
        # "0305133722-1587170244"
        result =  self.duser.getuserinfo(code)
        user_id = result.get('userid')
        return user_id
