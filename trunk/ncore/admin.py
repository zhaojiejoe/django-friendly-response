from __future__ import unicode_literals
from django.contrib import admin
from django.utils.encoding import smart_text
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import NOT_PROVIDED, DateTimeField
from django.utils import timezone
from django.core import serializers

import json

def get_field_value(obj, field):
    """
    Gets the value of a given model instance field.
    :param obj: The model instance.
    :type obj: Model
    :param field: The field you want to find the value of.
    :type field: Any
    :return: The value of the field as a string.
    :rtype: str
    """
    if isinstance(field, DateTimeField):
        # DateTimeFields are timezone-aware, so we need to convert the field
        # to its naive form before we can accuratly compare them for changes.
        try:
            value = field.to_python(getattr(obj, field.name, None))
            if value is not None and settings.USE_TZ and not timezone.is_naive(value):
                value = timezone.make_naive(value, timezone=timezone.utc)
        except ObjectDoesNotExist:
            value = field.default if field.default is not NOT_PROVIDED else None
    else:
        try:
            value = smart_text(getattr(obj, field.name, None))
        except ObjectDoesNotExist:
            value = field.default if field.default is not NOT_PROVIDED else None

    return value


def model_delta(old_model, new_model):
    """
    Provides delta/difference between two models
    :param old: The old state of the model instance.
    :type old: Model
    :param new: The new state of the model instance.
    :type new: Model
    :return: A dictionary with the names of the changed fields as keys and a
             two tuple of the old and new field values
             as value.
    :rtype: dict
    """

    delta = {}
    fields = new_model._meta.fields
    for field in fields:
        old_value = get_field_value(old_model, field)
        new_value = get_field_value(new_model, field)
        if old_value != new_value:
            delta[field.name] = [smart_text(old_value),
                                 smart_text(new_value)]

    if len(delta) == 0:
        delta = None

    return delta


from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

class UserAdmin(BaseUserAdmin):
    def log_change(self, request, object, message):
        delta = model_delta(self._old_model, object)
        changed_fields = json.dumps(delta)
        super(UserAdmin, self).log_change(request, object, str(message)+changed_fields)

    def save_model(self, request, obj, form, change):
        self._old_model = self.model.objects.get(id=obj.id)
        super(UserAdmin, self).save_model(request, obj, form, change)


# Register your models here.
@admin.register(admin.models.LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    """
    该类用于显示 admin 内置的 django_admin_log 表。
    其中，content_type 是指用户修改的 Model 名
    """
    list_display = ['action_time', 'user', 'content_type', '__str__']
    list_display_links = ['action_time']
    list_filter = ['action_time', 'content_type', 'user']
    list_per_page = 15
    readonly_fields = ['action_time', 'user', 'content_type',
                       'object_id', 'object_repr', 'action_flag', 'change_message']


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

