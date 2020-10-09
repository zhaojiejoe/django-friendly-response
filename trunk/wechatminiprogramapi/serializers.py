from rest_framework import serializers
from django.db import transaction

from wechatminiprogramapi.models import WechatMiniUserInfo, User
from wechatminiprogramapi.services import WMPCService

class WeChatMiniProgramCodeSerializer(serializers.Serializer):
    code = serializers.CharField(required=True, help_text="微信小程序jscode码")


class WeChatMiniProgramLoginSerializer(serializers.Serializer):
    res = serializers.CharField(required=True, help_text="微信小程序userinfo接口res")
    thirdsession = serializers.CharField(required=True, help_text="微信小程序第三方生成session")


class WechatMiniUserInfoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = WechatMiniUserInfo
        fields = (
            'nickName',
            'country',
            'province',
            'city',
            'openId',
            'unionId',
            'gender',
            'avatarUrl')

    def create(self, validated_data):
        with transaction.atomic():
            openid = validated_data['openId']
            wui = WechatMiniUserInfo.objects.filter(openId=openid).first()
            if wui is not None:
                user = wui.user
            else:
                user, created = User.objects.get_or_create(
                    username=openid, defaults={'password': WMPCService.gen_password()})
            print(user)
            wechatuser, created = WechatMiniUserInfo.objects.update_or_create(
                user=user, defaults=validated_data)
        return wechatuser
