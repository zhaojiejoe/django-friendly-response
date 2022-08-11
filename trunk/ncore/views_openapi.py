from rest_framework import viewsets, status
from rest_framework import views, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout, authenticate
from django.db.models.enums import TextChoices
from ncore.serializers_openapi import LoginRequestSerializer, LoginResponseSerializer
from ncore.ret_codes import Codes, gen_msg_from_code
from ncore.response import JsonResponse

from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from drf_spectacular.utils import extend_schema, OpenApiParameter,\
    OpenApiExample, PolymorphicProxySerializer, OpenApiResponse,\
    extend_schema_field
from drf_spectacular.types import OpenApiTypes
from ncore.schema import enveloper, pagi_enveloper, EmptySerializer

#PolymorphicProxySerializer anyof语法

class LoginView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginRequestSerializer
    pagination_class = None

    @extend_schema(description="密码账号session登入",
                        responses={200 : enveloper(LoginResponseSerializer)})
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

    @extend_schema(description="密码账号session登出", responses={200 : EmptySerializer})
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
        print(response.data)
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


"""
openapi使用问题案例
"""
class ActiveChoices(TextChoices):
    """
    Enums案例
    """
    t = '是'
    f = '否'

class OtherStuffSerializer(serializers.Serializer):
    foo = serializers.CharField(help_text="test")

from typing import Dict, List, Union, Optional, Set

class UserSerializer(serializers.ModelSerializer):
    """
    用户添加数据
    """
    lst = serializers.SerializerMethodField()
    other_stuff = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()
    fil = serializers.FileField(help_text="文件") #文件测试案例

    def get_lst(self, obj)-> List[int]:
        """
        普通返回值案例
        """
        return [1,2,3]

    @extend_schema_field(OtherStuffSerializer(many=True))
    def get_other_stuff(self, obj):
        """
        返回列表或者字典案例
        """
        return OtherStuffSerializer().data

    def get_is_active(self, obj) -> ActiveChoices:
        return ActiveChoices.f  # pragma: no cover

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
            'lst',
            'fil',)


class UserPostSerializer(serializers.ModelSerializer):

        inttest = serializers.IntegerField()
        fil = serializers.FileField(help_text="文件", read_only=False)
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
                'other',
                'fil'
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
    http_method_names = ['get', 'post', 'patch', 'delete']
    swagger_user = enveloper(UserSerializer)

    @extend_schema(description="获取用户列表页接口",
                        responses={200 : pagi_enveloper(UserSerializer)})
    def list(self, request, *args, **kwargs):
        #data = self.get_serializer(self.get_queryset(), many=True).data[0:1]
        rest = super(UserView, self).list(request, *args, **kwargs)
        User.objects.get(id=2)
        return rest

    @extend_schema(description="获取用户详情页接口",
                        responses={200 : swagger_user})
    def retrieve(self, request, *args, **kwargs):
        return super(UserView, self).retrieve(request, *args, **kwargs)

    @extend_schema(description="创建用户详情页接口", request=UserPostSerializer,
                        responses={200 : swagger_user})
    def create(self, request, *args, **kwargs):
        return super(UserView, self).create(request, *args, **kwargs)

    @extend_schema(description="删除用户详情页接口",
                        responses={200 : EmptySerializer})
    def destroy(self, request, *args, **kwargs):
        return super(UserView, self).destroy(request, *args, **kwargs)
    
    @extend_schema(description="部分修改用户详情页接口", request=UserPostSerializer,
                        responses={200 : swagger_user})
    def partial_update(self, request, *args, **kwargs):
        return super(UserView, self).partial_update(request, *args, **kwargs)