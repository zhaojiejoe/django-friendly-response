from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()

class LoginRequestSerializer(serializers.Serializer):
    """
    登录请求schema
    """
    username = serializers.CharField(required=True, help_text="账号", read_only=False)
    password = serializers.CharField(required=True, help_text="密码", read_only=False)

class LoginResponseSerializer(serializers.Serializer):
    """
    登录返回schema
    """
    user_id = serializers.IntegerField(required=True, help_text="用户id")

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_active'
            )

def custom_validation_error(errmsg, field="non_field_errors"):
    return serializers.ValidationError({field: [errmsg]})
