#!/usr/bin/env python3

from aiohttp import web
from json import decoder

from resto.exceptions import (
    ConflictException,
    NotFoundException
)


class RestaurantsView(web.View):
    def _extract_name(self):
        if 'name' not in self.request.match_info:
            raise web.HTTPBadRequest(reason="Missing restaurant's name in URL.")

        return self.request.match_info['name']

    async def _extract_args(self, mandatory_args=['name']):
        try:
            args = await self.request.json()
        except decoder.JSONDecodeError:
            raise web.HTTPBadRequest(reason="Request body should be a valid JSON.")

        missing = []
        for mandatory_arg in mandatory_args:
            if mandatory_arg not in args:
                missing.append(mandatory_arg)

        if missing:
            raise web.HTTPBadRequest(reason="Mandatory parameter(s) missing: %s." % ', '.join(missing))

        return args

    async def delete(self):
        name = self._extract_name()

        try:
            return await self.request.app['restaurants'].delete_by_name(name)
        except NotFoundException as e:
            raise web.HTTPNotFound(reason=str(e))

    async def get(self):
        try:
            if 'name' in self.request.match_info:
                return await self.request.app['restaurants'].read_by_name(self.request.match_info['name'])
            elif 'random' in self.request.query and self.request.query['random'].lower() == 'true':
                return await self.request.app['restaurants'].read_random()
            else:
                return await self.request.app['restaurants'].read_all()
        except NotFoundException as e:
            raise web.HTTPNotFound(reason=str(e))

    async def patch(self):
        name = self._extract_name()
        args = await self._extract_args()

        try:
            return await self.request.app['restaurants'].update_by_name(name, args['name'])
        except NotFoundException as e:
            raise web.HTTPNotFound(reason=str(e))
        except ConflictException as e:
            raise web.HTTPConflict(reason=str(e))

    async def post(self):
        args = await self._extract_args()
        if len(args['name']) > 255:
            raise web.HTTPBadRequest(reason="Name can't exceed 255 characters.")

        try:
            return await self.request.app['restaurants'].create(args['name'])
        except ConflictException as e:
            raise web.HTTPConflict(reason=str(e))
