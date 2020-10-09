# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class DingtalkUser(models.Model):
    dingtalk_user_id = models.CharField('dingtalk_user_id', max_length=50)
    django_user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.dingtalk_user_id

    class Meta:
        verbose_name = 'ding_talk_user'
        verbose_name_plural = verbose_name
        ordering = ['id']
