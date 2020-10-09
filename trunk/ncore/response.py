from rest_framework.response import Response

class JsonResponse(Response):
    def __init__(self, data=None, code=None, msg=None,
                 status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None):
        super(JsonResponse, self).__init__(data=data, status=status,
				template_name=template_name, headers=headers,
                                exception=exception, content_type=content_type)
        self.data = {"code": code, "msg": msg, "data": data}
