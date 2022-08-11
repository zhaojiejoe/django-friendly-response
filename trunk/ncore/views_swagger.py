from rest_framework import viewsets, status
from rest_framework import views, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout, authenticate
from ncore.serializers import LoginInSerializer, LoginInFinishSerializer
from ncore.ret_codes import Codes, gen_msg_from_code
from ncore.response import JsonResponse

from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class LoginView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginInSerializer
    pagination_class = None

    @swagger_auto_schema(operation_description="密码账号session登入",
                        responses={200 : openapi.Response('密码账号session登入', LoginInFinishSerializer())})
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

    @swagger_auto_schema(operation_description="密码账号session登出", responses={200 : ""})
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


from django.contrib.auth import get_user_model
User = get_user_model()
from ncore.viewsets import CustomModelViewSet
from rest_framework import serializers
from ncore.serializers import custom_validation_error

from drf_yasg.utils import swagger_serializer_method

class OtherStuffSerializer(serializers.Serializer):
    foo = serializers.CharField(help_text="test")

from typing import Dict, List, Union, Optional, Set

class UserSerializer(serializers.ModelSerializer):
    """
    用户添加数据
    """
    test = serializers.SerializerMethodField()
    other_stuff = serializers.SerializerMethodField()

    def get_test(self, obj)-> List[int]:
        """
        普通返回值
        """
        return 1

    @swagger_serializer_method(serializer_or_field=OtherStuffSerializer(many=True))
    def get_other_stuff(self, obj):
        """
        返回列表或者字典
        """
        return OtherStuffSerializer().data

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            #'email',
            #'first_name',
            #'last_name',
            'is_active',
            'other_stuff',
            'test',)


class UserPostSerializer(serializers.ModelSerializer):

        inttest = serializers.IntegerField()
        other = OtherStuffSerializer(many=True)

        class Meta:
            model = User
            fields = (
                'username',
                'email',
                'first_name',
                'last_name',
                'is_active',
                'inttest',
                'other'
            )

import django_filters
from django_filters import rest_framework as filters
from django.db.models import Q



class UserFilter(filters.FilterSet):
    sort = django_filters.OrderingFilter(fields=('username','first_name','last_name',), help_text="排序")
    username = filters.CharFilter('username', lookup_expr='icontains', help_text="姓名")


    class Meta:
        model = User
        fields = ("username",)


from rest_framework.pagination import CursorPagination

class CustomCursorPagination(CursorPagination):
    page_size = 1
    ordering = 'username'

class UserView(CustomModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    filter_class = UserFilter
    http_method_names = ['get', 'post']


    @swagger_auto_schema(operation_description="获取用户列表页接口",
                        responses={200 : openapi.Response('获取用户列表页接口', UserSerializer(many=True))})
    def list(self, request, *args, **kwargs):
        #data = self.get_serializer(self.get_queryset(), many=True).data[0:1]
        rest = super(UserView, self).list(request, *args, **kwargs)
        User.objects.get(id=2)
        return rest

    @swagger_auto_schema(operation_description="获取用户详情页接口",
                        responses={200 : openapi.Response('获取用户详情页接口', UserSerializer())})
    def retrieve(self, request, *args, **kwargs):
        return super(UserView, self).retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="创建用户详情页接口", request_body=UserPostSerializer,
                        responses={200 : openapi.Response('创建用户详情页接口', UserSerializer())})
    def create(self, request, *args, **kwargs):
        return super(UserView, self).create(request, *args, **kwargs)

    
