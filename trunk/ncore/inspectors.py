from drf_yasg.inspectors import SwaggerAutoSchema, PaginatorInspector
from drf_yasg import openapi
from collections import OrderedDict
from ncore.paginations import CustomerPagination

class CustomPaginatorInspector(PaginatorInspector):

    def get_paginator_parameters(self, paginator):
        if isinstance(paginator, CustomerPagination):
            return [
                openapi.Parameter(
                    'page', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="页数"
                ),
                openapi.Parameter(
                    'limit', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="每页显示数"
                ),
            ]
        return super(CustomPaginatorInspector, self).get_paginator_parameters(paginator)

    def get_paginated_response(self, paginator, response_schema):
        paged_schema = None

        if isinstance(paginator, CustomerPagination):
            paged_schema = openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={"count": openapi.Schema(type="integer", description="数据总量"),
                            "pages": openapi.Schema(type="integer", description="总页数"),
                            "current_page": openapi.Schema(type="integer", description="当前页"),
                            "results": response_schema,
                },)
            return paged_schema
        return super(CustomPaginatorInspector, self).get_paginated_response(paginator, response_schema)


class CustomSwaggerAutoSchema(SwaggerAutoSchema):


    def custom_get_pagination_schema(self, schema):
        # @swagger_auto_schema时没有正确处理是否需要分页，这里我们直接强制进行分页，所以对我们swagger_auto_schema的写法有要求
        if self.has_list_response() and self.should_page():
            schema = self.get_paginated_response(schema) or schema
        return schema

    def get_responses(self):                      
        r = super(CustomSwaggerAutoSchema, self).get_responses()                                                       
        if '200' in r.keys():
            if "schema" in r["200"].keys():
                r["200"]["schema"] = {"allOf": 
                [
                    openapi.Schema(type=openapi.TYPE_OBJECT, properties={"data": self.custom_get_pagination_schema(r["200"]["schema"])}),
                    openapi.Schema(type=openapi.TYPE_OBJECT, properties={"code": openapi.Schema(type="integer", default=200)}),
                    openapi.Schema(type=openapi.TYPE_OBJECT, properties={"msg": openapi.Schema(type="string", default='成功')}),
                ]}
            else:
                r["200"]["schema"] = {"allOf": 
                [
                    openapi.Schema(type=openapi.TYPE_OBJECT, properties={"data":openapi.Schema(type="string", default='')}),
                    openapi.Schema(type=openapi.TYPE_OBJECT, properties={"code": openapi.Schema(type="integer", default=200)}),
                    openapi.Schema(type=openapi.TYPE_OBJECT, properties={"msg": openapi.Schema(type="string", default='成功')}),
                ]}
        return r
