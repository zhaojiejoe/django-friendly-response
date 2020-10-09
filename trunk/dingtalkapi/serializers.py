from rest_framework import serializers


class DingTalkSerializer(serializers.Serializer):
    code = serializers.CharField(required=True, help_text="钉钉code码")
