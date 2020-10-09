from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

from ncore.ret_codes import Codes, gen_msg_from_code
from ncore.response import JsonResponse
from .models import DingtalkUser
from .services import AKCService
from .serializers import DingTalkSerializer


# Create your views here.
class DingTalkLoginView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = DingTalkSerializer
    pagination_class = None

    def post(self, request, *args, **kwargs):
        """
        钉钉内部应用session登出
        """
        data = request.data
        code = data.get('code', None)
        if code is None:
            return JsonResponse(**gen_msg_from_code(Codes.NO_DINGTALK_CODE))
        dingtalk_user_id = AKCService().get_user_id(code)
        ding_talk_user = DingtalkUser.objects.filter(dingtalk_user_id=dingtalk_user_id).first()
        if ding_talk_user is not None:
            user = ding_talk_user.django_user
            user.backend = "django.contrib.auth.backends.ModelBackend"
            if user.is_active:
                login(request, user)
                return JsonResponse(**gen_msg_from_code(Codes.OK, data={"id": user.id, "dingtalk_user_id": dingtalk_user_id,
                                                                        "session_key": request.session.session_key, 'expiry_date': str(request.session.get_expiry_date())}))
            return JsonResponse(**gen_msg_from_code(Codes.INACTIVED_USER))
        return JsonResponse(**gen_msg_from_code(Codes.NO_SUCH_USER))

    def delete(self, request, *args, **kwargs):
        """
        钉钉内部应用session登出
        钉钉http没delete方法可用@action处理，action只有viewset才支持
        """
        logout(request)
        return JsonResponse(**gen_msg_from_code(Codes.OK))
