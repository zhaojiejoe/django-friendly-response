
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Basic': {
            'type': 'basic'
        },
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'USE_SESSION_AUTH': True,
    'LOGIN_URL': 'rest_framework:login',
    'LOGOUT_URL': 'rest_framework:logout',
    'SHOW_REQUEST_HEADERS': True,
    'APIS_SORTER': 'alpha',
    'JSON_EDITOR': False,
    'OPERATIONS_SORTER': 'alpha',
    'VALIDATOR_URL': None,
    'DOC_EXPANSION': 'none',
    'SUPPORTED_SUBMIT_METHODS': ['get', 'post', 'delete', 'patch'],
    'DEFAULT_AUTO_SCHEMA_CLASS': 'ncore.inspectors.CustomSwaggerAutoSchema',
    'DEFAULT_PAGINATOR_INSPECTORS': ["ncore.inspectors.CustomPaginatorInspector"],
}
