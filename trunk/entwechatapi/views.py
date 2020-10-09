from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from drf_yasg.utils import swagger_auto_schema

from ncore.ret_codes import Codes, gen_msg_from_code
from ncore.response import JsonResponse
from .models import EntWeChatUser
from .services import EWCService
from .serializers import EntWeChatSerializer


# Create your views here.
class EntWeChatLoginView(GenericAPIView):
    """
    流程
    配置redirect跳转页面
    前端get后端返回微信url
    前端redirect至微信url
    微信url自动跳转至配置redirect并附带code和state
    前端post后端带上code和state
    后端返回登录态
    """
    permission_classes = (AllowAny,)
    serializer_class = EntWeChatSerializer
    pagination_class = None

    def post(self, request, *args, **kwargs):
        """
        企业微信session登录
        """
        data = request.data
        code = data.get('code', None)
        state = data.get('state', None)
        if code is None:
            return JsonResponse(**gen_msg_from_code(Codes.NO_ENTWECHAT_CODE))
        if state is None:
            return JsonResponse(**gen_msg_from_code(Codes.NO_ENTWECHAT_STATE))
        entwechat_user_id = EWCService().get_user_id(code)
        ent_wechat_user = EntWeChatUser.objects.filter(entwechat_user_id=entwechat_user_id).first()
        if ent_wechat_user is not None:
            user = ent_wechat_user.django_user
            user.backend = "django.contrib.auth.backends.ModelBackend"
            if user.is_active:
                login(request, user)
                return JsonResponse(**gen_msg_from_code(Codes.OK, data={"id": user.id, "entwechat_user_id": entwechat_user_id,
                                                                        "session_key": request.session.session_key, 'expiry_date': str(request.session.get_expiry_date())}))
            return JsonResponse(**gen_msg_from_code(Codes.INACTIVED_USER))
        return JsonResponse(**gen_msg_from_code(Codes.NO_SUCH_USER))

    def get(self, request, *args, **kwargs):
        """
        企业微信获取授权跳转链接
        """
        authorize_url = EWCService().authorize_url()
        return JsonResponse(**gen_msg_from_code(Codes.OK, data={"authorize_url": authorize_url}))

    def delete(self, request, *args, **kwargs):
        """
        企业微信session登出
        """
        logout(request)
        return JsonResponse(**gen_msg_from_code(Codes.OK))