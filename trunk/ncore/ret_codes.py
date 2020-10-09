from django.utils.translation import ugettext as _

class Codes(object):
    OK = 200
    NO_SUCH_USER = 40001
    INCORRECT_PWD = 40002
    INACTIVED_USER = 40003
    NO_DINGTALK_CODE = 40004
    NO_ENTWECHAT_CODE = 40005
    NO_ENTWECHAT_STATE = 40006
    USER_PWD_ERROR = 40007
    INVALID_JWT_TOKEN = 40008
    NO_WECHAT_MINI_CODE = 40009
    NO_WECHAT_MINI_RES = 400010
    NO_WECHAT_MINI_THIRDSESSION = 400011
    WECHAT_MINI_SIGN_ERROR = 400012


CodesMsgMapper = {
    Codes.OK: _('ok'),
    Codes.NO_SUCH_USER: _("no_such_user"),
    Codes.INCORRECT_PWD: _("incorrect_password"),
    Codes.INACTIVED_USER: _("inactived_user"),
    Codes.NO_DINGTALK_CODE: _("no_dingtalk_code"),
    Codes.NO_ENTWECHAT_CODE: _("no_entwechat_code"),
    Codes.NO_ENTWECHAT_STATE: _("no_entwechat_state"),
    Codes.USER_PWD_ERROR: _("user_pwd_error"),
    Codes.INVALID_JWT_TOKEN: _("invalid_jwt_token"),
    Codes.NO_WECHAT_MINI_CODE: _("no_wechat_mini_code"),
    Codes.NO_WECHAT_MINI_RES: _("no_wechat_mini_res"),
    Codes.NO_WECHAT_MINI_THIRDSESSION: _("no_wechat_mini_thirdsession"),
    Codes.WECHAT_MINI_SIGN_ERROR: _("wechat_mini_sign_error"),
}


def gen_msg_from_code(code, data=[], msg=""):
    data = data or []
    if code in CodesMsgMapper:
        msg = msg or CodesMsgMapper[code]
    return {"code": code, "data": data, "msg": msg}
