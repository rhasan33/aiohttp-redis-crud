import logging
import uuid
import json
from aiohttp import web

logger = logging.getLogger("search")

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
    data = await request.json()
    key = uuid.uuid4()
    data["user_id"] = str(key)
    redis = request.app.get('redis')
    redis.hmset(str(key), data)
    return web.json_response(data=data, status=201)

async def get_all_users(request):
    redis = request.app.get('redis')
    keys = redis.keys('*')
    data = []
    for key in keys:
        data.append(redis.hgetall(key))
    return web.json_response(data=data, status=200)


async def get_user(request):
    user_id = request.match_info.get('user_id')
    redis = request.app.get('redis')
    data = redis.hgetall(user_id)
    if data:
        return web.json_response(data=data, status=200)
    else:
        return web.json_response(data=data, status=404)

async def update_user(request):
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
    user_id = request.match_info.get('user_id')
    redis = request.app.get('redis')
    data = redis.hgetall(user_id)
    if data:
        redis.delete(user_id)
        return web.json_response(status=204)
    else:
        return web.json_response(data=data, status=404)
