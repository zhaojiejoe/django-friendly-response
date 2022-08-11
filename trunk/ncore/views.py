from rest_framework import viewsets, status
from rest_framework import views, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout, authenticate
from django.db.models.enums import TextChoices
from ncore.serializers import LoginInSerializer, LoginInFinishSerializer, UserSerializer
from ncore.ret_codes import Codes, gen_msg_from_code
from ncore.response import JsonResponse
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from ncore.viewsets import CustomModelViewSet
from rest_framework import serializers
from django.db.models import Q
from django.contrib.auth import get_user_model
from .filters import UserFilter
User = get_user_model()


class LoginView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginInSerializer
    pagination_class = None


    def post(self, request, *args, **kwargs):
        """
        密码账号session登录
        """
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)
        user = User.objects.filter(username=username).first()
        if user is None:
            return JsonResponse(**gen_msg_from_code(Codes.NO_SUCH_USER))
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return JsonResponse(
                    **gen_msg_from_code(Codes.OK, data={"id": user.id}))
            return JsonResponse(**gen_msg_from_code(Codes.INACTIVED_USER))
        return JsonResponse(**gen_msg_from_code(Codes.INCORRECT_PWD))

    def delete(self, request, *args, **kwargs):
        """
        密码账号session登出
        """
        logout(request)
        return JsonResponse(**gen_msg_from_code(Codes.OK))

class CustomObtainJSONWebTokenView(TokenObtainPairView):


    def post(self, request, *args, **kwargs):
        """
        JWTtoken获取
        jwt使用 http headers中加入Key:Authorization Value:Bearer realtoken
        """
        response = super(CustomObtainJSONWebTokenView, self).post(request, *args, **kwargs)
        if response.status_code != status.HTTP_200_OK:
            return JsonResponse(**gen_msg_from_code(Codes.USER_PWD_ERROR))
        return JsonResponse(**gen_msg_from_code(Codes.OK, data=response.data))


class CustomRefreshJSONWebTokenView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        """
        JWTtoken刷新
        """
        response = super(CustomRefreshJSONWebTokenView, self).post(request, *args, **kwargs)
        if response.status_code != status.HTTP_200_OK:
            return JsonResponse(**gen_msg_from_code(Codes.INVALID_JWT_TOKEN))
        return JsonResponse(**gen_msg_from_code(Codes.OK, data=response.data))


class UserView(CustomModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    filter_class = UserFilter
    http_method_names = ['get', 'post']


    def list(self, request, *args, **kwargs):
        return super(UserView, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super(UserView, self).retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super(UserView, self).create(request, *args, **kwargs)

    
