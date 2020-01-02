#!/usr/bin/env python3

import aiopg

from aiohttp import web

from resto.views import RestaurantsView


@web.middleware
async def json_middleware(request, handler):
    try:
        return web.json_response(await handler(request))
    except web.HTTPException as e:
        return web.json_response(
            {'error': e.reason},
            status=e.status
        )


async def resto_app(cfg):
    app = web.Application(middlewares=[json_middleware])
    app['cfg'] = cfg
    app['pool'] = await aiopg.create_pool(**dict(cfg.items('Database')))
    app.add_routes([web.view('/restaurants', RestaurantsView)])
    return app
