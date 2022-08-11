# -*- codidng: utf-8 -*-
from __future__ import unicode_literals
import django_filters
from django_filters import rest_framework as filters
from django.contrib.auth import get_user_model
User = get_user_model()


class UserFilter(filters.FilterSet):
    sort = django_filters.OrderingFilter(fields=('username','first_name','last_name',), help_text="排序")
    username = filters.CharFilter('username', lookup_expr='icontains', help_text="姓名")

    class Meta:
        model = User
        fields = ("username",)
