from rest_framework import pagination
from ncore.response import JsonResponse
from ncore.ret_codes import Codes, gen_msg_from_code


class CustomerPagination(pagination.PageNumberPagination):
    page_size_query_param = 'limit'

    def get_paginated_response(self, data):
        return JsonResponse(**gen_msg_from_code(data={
            'count': self.page.paginator.count,
            'pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'results': data
        }, code=Codes.OK))

    def get_paginated_response_schema(self, schema):
        return {
            'type': 'object',
            'properties': {
                'count': {
                    'type': 'integer',
                    'example': 123,
                },
                'pages': {
                    'type': 'integer',
                    'example': 123,
                },
                'current_page': {
                    'type': 'integer',
                    'example': 123,
                },
                'results': schema,
            },
        }
