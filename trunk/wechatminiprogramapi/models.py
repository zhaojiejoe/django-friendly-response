# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.

class WechatMiniUserInfo(models.Model):
    GENDER_CHOICE = ((0, '未知'), (1, '男'), (2, '女'),)
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    nickName = models.CharField('昵称', null=True, blank=True, max_length=50)
    country = models.CharField('国家', null=True, blank=True, max_length=50)
    province = models.CharField('省市', null=True, blank=True, max_length=50)
    city = models.CharField('区县', null=True, blank=True, max_length=50)
    openId = models.CharField('openId', max_length=50, unique=True)
    unionId = models.CharField('unionId', null=True, blank=True, max_length=50)
    gender = models.SmallIntegerField('性别', choices=GENDER_CHOICE)
    avatarUrl = models.URLField('头像', null=True, blank=True, max_length=500)
    date_created = models.DateTimeField('创建日期', auto_now_add=True)
    date_updated = models.DateTimeField('更新日期', auto_now=True)

    @property
    def profile_picture(self):
        if self.avatarUrl:
            return self.avatarUrl[:-1] + '46'
        return None

    def __str__(self):
        return self.nickName

    class Meta:
        ordering = ['-id']