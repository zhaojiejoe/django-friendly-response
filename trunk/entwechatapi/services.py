from wechatpy.enterprise.client import WeChatClient as EntWeChatClient
from django.conf import settings

CORPID = getattr(settings, "ENTWECHAT_CORPID", "wx4b4b6d394cf22d38")
REDIRECT_URI = getattr(settings, "ENTWECHAT_REDIRECT_URI", "http://desktop.polarwin.cn/")
AGENTID = getattr(settings, "ENTWECHAT_AGENTID", "1000003")
SECRET = getattr(settings, "DINGTALK_SECRET", "J6t68JAYvgWNoxzLT1pcmzxQx68IhhVEIQwsHcwF55s")


class EWCService(object):

    def __init__(self, corp_id=CORPID, secret=SECRET, access_token=None, session=None, timeout=None, auto_retry=True):
        # 如果不提供 session 参数，默认使用 wechatpy.session.memorystorage.MemoryStorage session 类型， 注意该类型不是线程安全的，不推荐生产环境使用。
        self.client = EntWeChatClient(corp_id, secret, access_token, session, timeout, auto_retry)
        self.message = self.client.message
        self.oauth = self.client.oauth

    def gen_text_body(self, content, safe=0):
        return {
                'msgtype': 'text',
                'text': {'content': content},
                'safe': safe
                }

    def send_message(self, user_ids, agent_id=AGENTID, party_ids='',
             tag_ids='', msg=None):
        # go2newera0052
        self.message.send(agent_id, user_ids, party_ids, tag_ids, msg)

    def authorize_url(self, redirect_uri=REDIRECT_URI, state="xyz"):
        return self.oauth.authorize_url(redirect_uri, state)#.replace("snsapi_base", "snsapi_userinfo")

    def get_user_id(self, code):
        return self.oauth.get_user_info(code).get('UserId', None)