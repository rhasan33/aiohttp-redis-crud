from src.views import user


def setup_routes(app):
    app.router.add_get("/", user.index)
    app.router.add_route('POST', '/api/v1/users', user.create_user)
    app.router.add_get('/api/v1/users', user.get_all_users)
    app.router.add_get('/api/v1/users/{user_id}', user.get_user)
    app.router.add_route('PUT', '/api/v1/users/{user_id}', user.update_user)
    app.router.add_route('DELETE', '/api/v1/users/{user_id}', user.delete_user)
