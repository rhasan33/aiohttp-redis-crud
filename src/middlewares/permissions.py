import logging
import json
from ast import literal_eval
from aiohttp import web

logger = logging.getLogger("search")

SUCCESS_STATUS = [200, 201]
DELETE_STATUS = 204
ERROR_STATUS = [400, 404, 401]

def permissions():
    return {
        'post': ['93a5fcba-c31b-482e-8177-41b469cdb4f8'],
        'put': ['7643b5f3-5ec7-48a2-8ad7-5fc6e198e5fd', '93a5fcba-c31b-482e-8177-41b469cdb4f8'],
        'get': [
            '93a5fcba-c31b-482e-8177-41b469cdb4f8',
            '7643b5f3-5ec7-48a2-8ad7-5fc6e198e5fd',
            'ced29724-0ef7-4e5a-9f8f-b8404f142553'
        ],
        'delete': ['93a5fcba-c31b-482e-8177-41b469cdb4f8']
    }

@web.middleware
async def auth_middleware(request, handler):
    if not request.path == '/':
        try:
            if request.headers['Authorization'] not in permissions().get(request.method.lower()):
                raise web.HTTPUnauthorized()
        except KeyError:
            raise web.HTTPBadRequest()
    resp = await handler(request)
    if int(resp.status) in SUCCESS_STATUS:
        data = {
            "error": False,
            "msg": "",
            "data": json.loads(resp.body.decode("utf-8"))
        }
        return web.json_response(data=data, status=int(resp.status))
    elif int(resp.status) in ERROR_STATUS:
        data = {
            "error": True,
            "msg": "Not found",
            "data": json.loads(resp.body.decode("utf-8"))
        }
        return web.json_response(data=data, status=int(resp.status))
    elif int(resp.status) == DELETE_STATUS:
        return web.json_response(status=int(resp.status))
    else:
        data = {
            "error": True,
            "msg": "Internal server error"
        }
    return web.json_response(data=data, status=int(resp.status))