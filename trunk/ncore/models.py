# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import pre_delete, post_delete
from django.dispatch.dispatcher import receiver

from django.contrib.auth.models import AbstractUser

"""
class User(AbstractUser):
    pass

# Create your models here.
class Photo(models.Model):
    image = models.ImageField(upload_to='photos/%Y-%m-%d')

@receiver(post_delete, sender=Photo)
def photo_delete(sender, instance, **kwargs):
    # 这里是为了触发oss的远程删除动作
    instance.image.delete(False)

from django.contrib import admin
@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass
"""
