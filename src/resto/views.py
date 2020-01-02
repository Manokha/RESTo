#!/usr/bin/env python3

import logging

from aiohttp import web
from json import decoder, dumps
from psycopg2.errors import UniqueViolation


logger = logging.getLogger('resto.views')
logger.setLevel(logging.DEBUG)


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

    async def _write_single(self, sql):
        if self.request.body_exists:
            try:
                args = await self.request.json()
            except decoder.JSONDecodeError:
                raise web.HTTPBadRequest(reason="Request body should be a valid JSON.")
        else:
            args = {}

        self._check_parameters(args)

        # TODO: propose pull request to aiopg to fix cursor() from pool (no wait in __aenter__ nor __aexit__)
        async with self.request.app['pool'].acquire() as conn:
            async with conn.cursor() as cursor:
                try:
                    await cursor.execute(sql, args)
                except UniqueViolation as e:
                    # TODO: better error handling. This works as long as name is the only unique field.
                    reason = "A restaurant with that name [%(name)s] already exists." % args
                    raise web.HTTPConflict(reason="A restaurant with that name [%(name)s] already exists." % args)

                if cursor.rowcount < 1:
                    # TODO: better error handling. This works as long as name is the only unique field.
                    raise web.HTTPNotFound(reason="There are no restaurant with that name [%(name)s]." % args)

    async def delete(self):
        return await self._write_single("DELETE FROM Restaurants WHERE name = %(name)s")

    async def get(self):
        args = self.request.query
        self._check_parameters(args)
        assert_one_result = True

        # TODO: handle retrieved columns
        if 'name' in args:
            sql = "SELECT name FROM Restaurants WHERE name = %(name)s"
        elif 'random' in args:
            sql = "SELECT name FROM Restaurants LIMIT 1 OFFSET FLOOR(RANDOM() * (SELECT COUNT(*) FROM Restaurants))"
        else:
            sql = "SELECT name FROM Restaurants"
            assert_one_result = False

        # TODO: propose pull request to aiopg to fix cursor() from pool (no wait in __aenter__ nor __aexit__)
        async with self.request.app['pool'].acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql, args)
                rows = await cursor.fetchall()

        if assert_one_result and len(rows) < 1:
            raise web.HTTPNotFound(reason="There are no restaurant with that name [%(name)s]." % args)

        return [{'name': name} for name, in rows]

    async def patch(self):
        return await self._write_single("UPDATE Restaurants SET name = %(new_name)s WHERE name = %(name)s")

    async def post(self):
        return await self._write_single("INSERT INTO Restaurants (name) VALUES (%(name)s)")
