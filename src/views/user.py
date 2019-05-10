import logging
import uuid
import json
from aiohttp import web

logger = logging.getLogger("search")

perms = {
    'create': ['93a5fcba-c31b-482e-8177-41b469cdb4f8'],
    'update': ['7643b5f3-5ec7-48a2-8ad7-5fc6e198e5fd', '93a5fcba-c31b-482e-8177-41b469cdb4f8'],
    'get': [
        '93a5fcba-c31b-482e-8177-41b469cdb4f8',
        '7643b5f3-5ec7-48a2-8ad7-5fc6e198e5fd',
        'ced29724-0ef7-4e5a-9f8f-b8404f142553'
    ],
    'delete': ['93a5fcba-c31b-482e-8177-41b469cdb4f8']
}

async def index(request):
    """
    :purpose: health check api
    :params: request:- aiohttp request object
    :returns: dictionary object
    """
    data = {
        "success": True,
        "message": "User API v.1.0.0",
        "method": "Requested method is ({})".format(request.method),
    }
    logger.info("Health check api.")

    return web.json_response(data=data, status=200)

async def create_user(request):
    try:
        if request.headers['Authorization'] not in perms['create']:
            return web.json_response(data={"msg": "Access Denied!!"}, status=401)
    except KeyError:
        return web.json_response(data={"msg": "Invalid Request"}, status=400)
    data = await request.json()
    key = uuid.uuid4()
    data["user_id"] = str(key)
    redis = request.app.get('redis')
    redis.hmset(str(key), data)
    return web.json_response(data=data, status=201)

async def get_all_users(request):
    try:
        if request.headers['Authorization'] not in perms['get']:
            return web.json_response(data={"msg": "Access Denied!!"}, status=401)
    except KeyError:
        return web.json_response(data={"msg": "Invalid Request"}, status=400)
    redis = request.app.get('redis')
    keys = redis.keys('*')
    data = {
        "person": []
    }
    for key in keys:
        data['person'].append(redis.hgetall(key))
    return web.json_response(data=data, status=200)


async def get_user(request):
    try:
        if request.headers['Authorization'] not in perms['get']:
            return web.json_response(data={"msg": "Access Denied!!"}, status=401)
    except KeyError:
        return web.json_response(data={"msg": "Invalid Request"}, status=400)
    user_id = request.match_info.get('user_id')
    redis = request.app.get('redis')
    data = redis.hgetall(user_id)
    if data:
        return web.json_response(data=data, status=200)
    else:
        return web.json_response(data=data, status=404)

async def update_user(request):
    try:
        if request.headers['Authorization'] not in perms['update']:
            return web.json_response(data={"msg": "Access Denied!!"}, status=401)
    except KeyError:
        return web.json_response(data={"msg": "Invalid Request"}, status=400)
    user_id = request.match_info.get('user_id')
    body = await request.json()
    redis = request.app.get('redis')
    data = redis.hgetall(user_id)
    if data:
        redis.hmset(user_id, body)
        data = redis.hgetall(user_id)
        return web.json_response(data=data, status=200)
    else:
        return web.json_response(data=data, status=404)

async def delete_user(request):
    try:
        if request.headers['Authorization'] not in perms['delete']:
            return web.json_response(data={"msg": "Access Denied!!"}, status=401)
    except KeyError:
        return web.json_response(data={"msg": "Invalid Request"}, status=400)
    user_id = request.match_info.get('user_id')
    redis = request.app.get('redis')
    data = redis.hgetall(user_id)
    if data:
        redis.delete(user_id)
        return web.json_response(status=204)
    else:
        return web.json_response(data=data, status=404)
