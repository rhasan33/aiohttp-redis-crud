from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop

from routes.routes import setup_routes


class UserCreateTest(AioHTTPTestCase):
    async def setUpAsync(self):
        self._data = {
            "name": "Amio",
            "age": 30
        }
        self._url = '/api/v1/users'
    
    async def get_application(self):
        app = web.Application()
        setup_routes(app)
        return app
    
    @unittest_run_loop
    async def test_create_user(self):
        resp = await self.client.get(self._url)
        self.assertEqual(resp.status, 200)