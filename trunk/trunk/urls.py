"""trunk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include
from django.urls import path, re_path

from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from ncore.views import LoginView

schema_view = get_schema_view(
    openapi.Info(
        title="XXX API",
        default_version='v1',
        description="XXXX",
        terms_of_service="http://www.polarwin.cn/contact",
        contact=openapi.Contact(email="info@polarwin.cn"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
]

if settings.DEBUG:
    urlpatterns += [
        path(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
        re_path(r'swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
        path(r'swagger/', schema_view.with_ui('swagger',
                                               cache_timeout=0), name='schema-swagger-ui'),
        path(r'cached/swagger/', schema_view.with_ui('swagger',
                                                      cache_timeout=None), name='schema-swagger-ui-cached'),
        path(r'redoc/', schema_view.with_ui('redoc',
                                             cache_timeout=0), name='schema-redoc'),
    ]

if settings.DEBUG:
    from rest_framework.routers import DefaultRouter
    from ncore.views import UserView
    from ncore.views import CustomObtainJSONWebTokenView, CustomRefreshJSONWebTokenView
    from dingtalkapi.views import DingTalkLoginView
    from entwechatapi.views import EntWeChatLoginView
    from wechatminiprogramapi.views import WeChatMiniProgramCodeView, WeChatMiniProgramLoginView

    router = DefaultRouter()
    router.register(r'users', UserView, base_name='user')
    urlpatterns += [
        path(r'', include(router.urls)),
        # path('dlogin/', DingTalkLoginView.as_view(), name='dlogin'),
        # path('entwlogin/', EntWeChatLoginView.as_view(), name='entwlogin'),
        # path('api-token-auth/', CustomObtainJSONWebTokenView.as_view(), name='jwt_obtain'),
        # path('api-token-refresh/', CustomRefreshJSONWebTokenView.as_view(), name='jwt_refresh'),
        # path('wechat-mini-program-code/', WeChatMiniProgramCodeView.as_view(), name='wechat_mini_program_code'),
        # path('wechat-mini-program-login/', WeChatMiniProgramLoginView.as_view(), name='wechat_mini_program_login'),
    ]
    # urlpatterns += [path(r'silk/', include('silk.urls', namespace='silk'))]
