from rest_framework import serializers


class EntWeChatSerializer(serializers.Serializer):
    code = serializers.CharField(required=True, help_text="企业微信code码")
    state = serializers.CharField(required=True, help_text="企业微信state码")
