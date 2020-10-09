# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.generics import GenericAPIView
from rest_framework import status
import requests
from django.conf import settings
from django.contrib.auth import login
import json
import hashlib

from wechatminiprogramapi.serializers import (WeChatMiniProgramCodeSerializer, WeChatMiniProgramLoginSerializer,
                                            WechatMiniUserInfoSerializer)
from wechatminiprogramapi.services import WMPCService
from wechatminiprogramapi.models import WechatMiniUserInfo
from ncore.response import JsonResponse
from ncore.ret_codes import Codes, gen_msg_from_code


class WeChatMiniProgramCodeView(GenericAPIView):
    """
    获取openid和session_key，生成thirdsession
    """
    permission_classes = ()
    serializer_class = WeChatMiniProgramCodeSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        code = data.get('code', None)
        if code is None:
            return JsonResponse(**gen_msg_from_code(Codes.NO_WECHAT_MINI_CODE))
        wmpcservice = WMPCService()
        thirdsession = wmpcservice.encode_openid_skey(**wmpcservice.get_openid_skey(code=code))
        return JsonResponse(**gen_msg_from_code(Codes.OK, data={"thirdsession": thirdsession}))
        


class WeChatMiniProgramLoginView(GenericAPIView):
    """
    获取用户信息，验签和解码
    """
    permission_classes = ()
    serializer_class = WeChatMiniProgramLoginSerializer

    def update_or_create_user(self, request, session_key, resource, openid):
        # update not implement
        decryptdata = WMPCService().get_encrypted_data(session_key, resource['encryptedData'], resource['iv'])
        decryptdata.pop('watermark')
        decryptdata.pop('language')
        serializer = WechatMiniUserInfoSerializer(data=decryptdata)
        wechatuser = WechatMiniUserInfo.objects.filter(openId=openid).first()
        if wechatuser is None:
            if not serializer.is_valid():
                serializer = WechatMiniUserInfoSerializer(data={"openId": openid, "gender": 0})
                serializer.is_valid()
            wechatuser = serializer.save()
        return wechatuser.user

    def post(self, request, *args, **kwargs):
        data = request.data
        resource = data.get('res', None)
        thirdsession = data.get('thirdsession', None)
        if resource is None:
            return JsonResponse(**gen_msg_from_code(Codes.NO_WECHAT_MINI_RES))
        if thirdsession is None:
            return JsonResponse(**gen_msg_from_code(Codes.NO_WECHAT_MINI_THIRDSESSION))
        openid, session_key = WMPCService.decode_openid_skey(thirdsession)
        signature = resource['signature']
        raw_data = resource['rawData'].encode()
        if not hashlib.sha1((raw_data.decode() + session_key).encode()).hexdigest() == signature:
            return JsonResponse(**gen_msg_from_code(Codes.WECHAT_MINI_SIGN_ERROR))
        user = self.update_or_create_user(request, session_key, resource, openid)
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        data = {"session_key": request.session.session_key, 'expiry_date': str(request.session.get_expiry_date())}
        return JsonResponse(**gen_msg_from_code(Codes.OK, data=data))
