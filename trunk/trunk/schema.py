from django.conf import settings
from drf_spectacular.extensions import OpenApiAuthenticationExtension

class MySessionAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = 'ncore.authentications.CsrfExemptSessionAuthentication'  # full import path OR class ref
    name = 'CustomSessionAuth'  # name used in the schema
    priority = 1

    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'in': 'cookie',
            'name': settings.SESSION_COOKIE_NAME,
        }

class MyTokenAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = 'rest_framework_simplejwt.authentication.JWTAuthentication'  # full import path OR class ref
    name = 'CustomTokenAuth'  # name used in the schema
    priority = 2

    def get_security_definition(self, auto_schema):
        return {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
