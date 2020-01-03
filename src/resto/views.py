#!/usr/bin/env python3

from aiohttp import web
from json import decoder

from resto.exceptions import (
    ConflictException,
    NotFoundException
)


class RestaurantsView(web.View):
    # TODO: better arguments check
    _mandatory_parameters = {
        'DELETE': ['name'],
        'GET': [],
        'POST': ['name'],
        'PATCH': ['name', 'new_name'],
    }

    def _check_parameters(self, args):
        missing = []
        for arg in self._mandatory_parameters.get(self.request.method, []):
            if arg not in args:
                missing.append(arg)

        if missing:
            raise web.HTTPBadRequest(reason="Mandatory parameter(s) missing: %s." % ", ".join(missing))

    async def _extract_body(self):
        if self.request.body_exists:
            try:
                args = await self.request.json()
            except decoder.JSONDecodeError:
                raise web.HTTPBadRequest(reason="Request body should be a valid JSON.")
        else:
            args = {}

        self._check_parameters(args)
        return args

    async def delete(self):
        args = await self._extract_body()
        try:
            return await self.request.app['restaurants'].delete_by_name(args['name'])
        except NotFoundException as e:
            raise web.HTTPNotFound(reason=str(e))

    async def get(self):
        args = self.request.query
        self._check_parameters(args)

        try:
            if 'name' in args:
                return await self.request.app['restaurants'].read_by_name(args['name'])
            elif 'random' in args and args['random'].lower() == 'true':
                return await self.request.app['restaurants'].read_random()
            else:
                return await self.request.app['restaurants'].read_all()
        except NotFoundException as e:
            raise web.HTTPNotFound(reason=str(e))

    async def patch(self):
        args = await self._extract_body()
        try:
            return await self.request.app['restaurants'].update_by_name(args['name'], args['new_name'])
        except NotFoundException as e:
            raise web.HTTPNotFound(reason=str(e))
        except ConflictException as e:
            raise web.HTTPConflict(reason=str(e))

    async def post(self):
        args = await self._extract_body()
        try:
            return await self.request.app['restaurants'].create(args['name'])
        except ConflictException as e:
            raise web.HTTPConflict(reason=str(e))
