from rest_framework.views import exception_handler
from ncore.ret_codes import CodesMsgMapper
from rest_framework import exceptions
from django.utils.translation import ugettext as _
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.db.models.deletion import ProtectedError
from django.core.exceptions import ObjectDoesNotExist
from ncore.response import JsonResponse
import copy

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    _exc = copy.deepcopy(exc)
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data.clear()
        response.data['code'] = response.status_code
        response.data['data'] = {}
        # 可以自定义某些错误返回信息
        if response.status_code in CodesMsgMapper:
            response.data['msg'] = CodesMsgMapper[response.status_code]
        else:
            if isinstance(_exc, exceptions.APIException):
                if isinstance(_exc.detail, dict):
                    first_error = list(_exc.detail.values())[0]
                    if isinstance(first_error, list):
                        response.data['msg'] =  first_error[0]
                    else:
                        response.data['msg'] =  first_error
                    #response.data['errors'] = _exc.detail
                else:
                    if isinstance(_exc.detail, list):
                        response.data['msg'] = list(_exc.detail)[0]
                    else:
                        response.data['msg'] = _exc.detail
            elif isinstance(_exc, Http404):
                response.data['msg'] = str(_exc)
            elif isinstance(_exc, PermissionDenied):
                response.data['msg'] = str(_exc)
            else:
                response.data['msg'] = ''
        response.status_code = 200
    else:
        if isinstance(_exc, ProtectedError):
            response = JsonResponse(**{"code": 404, "data": {}, "msg": "该条目存在关联数据无法删除"})
        elif isinstance(_exc, ObjectDoesNotExist):
            response = JsonResponse(**{"code": 404, "data": {}, "msg": "该条目不存在"})
    return response
