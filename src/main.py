import os
from aiohttp import web
import redis

from src.logger import search_logger
from src.routes.routes import setup_routes

DEBUG = bool(os.environ.get("DEBUG", True))
app = web.Application(debug=DEBUG, logger=search_logger("search"))
redis_conn = redis.Redis(host=os.environ.get('REDIS_HOST', 'localhost'), port=6379, db=0, charset="utf-8", decode_responses=True)
app['redis'] = redis_conn
setup_routes(app)