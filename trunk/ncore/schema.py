from drf_spectacular.openapi import AutoSchema
from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers

class CustomAutoSchema(AutoSchema):

    def _get_response_for_code(self, serializer, status_code, media_types=None, direction='response'):
        ret = super(CustomAutoSchema, self)._get_response_for_code(serializer, status_code, media_types, direction)
        return ret

def enveloper(serializer_class, many=False):
    component_name = 'Enveloped{}{}'.format(
        serializer_class.__name__.replace("Serializer", ""),
        "List" if many else "",
    )

    @extend_schema_serializer(many=False, component_name=component_name)
    class EnvelopeSerializer(serializers.Serializer):
        status = serializers.IntegerField(default=200)  # some arbitrary envelope field
        data = serializer_class(many=many)  # the enveloping part
        msg = serializers.CharField()

    return EnvelopeSerializer


def pagi_enveloper(serializer_class):
    component_name = 'PagiEnveloped{}'.format(
        serializer_class.__name__.replace("Serializer", "")
    )
    inner_component_name = 'InnerPagiEnveloped{}'.format(
        serializer_class.__name__.replace("Serializer", "")
    )

    @extend_schema_serializer(many=False, component_name=inner_component_name)
    class PagiEnvelopeSerializer(serializers.Serializer):
        count = serializers.IntegerField()  # some arbitrary envelope field
        pages = serializers.IntegerField()
        current_page = serializers.IntegerField()
        results = serializer_class(many=True)  # the enveloping part

    @extend_schema_serializer(many=False, component_name=component_name)
    class EnvelopeSerializer(serializers.Serializer):
        status = serializers.IntegerField(default=200)  # some arbitrary envelope field
        data = PagiEnvelopeSerializer()  # the enveloping part
        msg = serializers.CharField()

    return EnvelopeSerializer

from typing import Dict, Any

class EmptySerializer(serializers.Serializer):
    status = serializers.IntegerField(default=200)  # some arbitrary envelope field
    data = serializers.SerializerMethodField()  # the enveloping part
    msg = serializers.CharField()

    def get_data(self, obj)-> Dict[Any, Any]:
        """
        普通返回值案例
        """
        return {}
    
