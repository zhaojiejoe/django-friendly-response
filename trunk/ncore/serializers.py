from rest_framework import serializers

class LoginInSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, help_text="账号")
    password = serializers.CharField(required=True, help_text="密码")

class LoginInFinishSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True, help_text="用户id")

def custom_validation_error(errmsg, field="non_field_errors"):
    return serializers.ValidationError({field: [errmsg]})