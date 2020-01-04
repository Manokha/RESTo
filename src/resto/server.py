#!/usr/bin/env python3

import aiopg

from aiohttp import web

from resto.views import RestaurantsView
from resto.models import PGRestaurants


@web.middleware
async def json_middleware(request, handler):
    try:
        return web.json_response(await handler(request))
    except web.HTTPException as e:
        return web.json_response(
            {'error': e.reason},
            status=e.status
        )


async def create_connection_pool(app):
    app['pg_pool'] = await aiopg.create_pool(**dict(app['cfg'].items('Database')))


async def create_collections(app):
    app['restaurants'] = PGRestaurants(app['pg_pool'])


async def dispose_connection_pool(app):
    app['pg_pool'].close()
    await app['pg_pool'].wait_closed()


async def resto_app(cfg):
    app = web.Application(middlewares=[json_middleware])
    app['cfg'] = cfg

    app.on_startup.append(create_connection_pool)
    app.on_startup.append(create_collections)
    app.on_cleanup.append(dispose_connection_pool)

    app.add_routes([
        web.view('/restaurants', RestaurantsView),
        web.view('/restaurants/{name}', RestaurantsView)
    ])
    return app
