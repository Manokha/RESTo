#!/usr/bin/env python3

import logging

from psycopg2.errors import UniqueViolation
from resto.exceptions import (
    ConflictException,
    NotFoundException
)


logger = logging.getLogger('resto.models')


class PGRestaurants:
    def __init__(self, pool):
        self.pool = pool

    async def _read_callback(self, cursor):
        rows = await cursor.fetchall()
        return [{'name': name} for name, in rows]

    async def _write_callback(self, cursor):
        return cursor.rowcount

    async def _read(self, query, *args, **kwargs):
        return await self._query(query, *args, callback=self._read_callback, **kwargs)

    async def _write(self, query, *args, **kwargs):
        return await self._query(query, *args, callback=self._write_callback, **kwargs)

    async def _query(self, query, *args, callback=None, **kwargs):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, *args, **kwargs)
                # TODO: check if callback is callable etc.
                if callback:
                    return await callback(cursor)

    async def create(self, name):
        try:
            affected_rows = await self._write(
                "INSERT INTO Restaurants (name) VALUES (%(name)s)",
                {'name': name}
            )
        except UniqueViolation:
            raise ConflictException("A restaurant with that name [%s] already exists." % name)

    async def delete_by_name(self, name):
        affected_rows = await self._write(
            "DELETE FROM Restaurants WHERE name = %(name)s",
            {'name': name}
        )
        if affected_rows < 1:
            raise NotFoundException("There are no restaurant with that name [%s]." % name)

    async def read_all(self):
        return await self._query("SELECT name FROM Restaurants", callback=self._read_callback)

    async def read_by_name(self, name):
        rows = await self._query(
            "SELECT name FROM Restaurants WHERE name = %(name)s",
            {'name': name},
            callback=self._read_callback
        )
        if len(rows) < 1:
            raise NotFoundException("There are no restaurant with that name [%s]." % name)

        # TODO: return a single row instead of a list ?
        return rows

    async def read_random(self):
        rows = await self._query(
            "SELECT name FROM Restaurants LIMIT 1 OFFSET FLOOR(RANDOM() * (SELECT COUNT(*) FROM Restaurants))",
            callback=self._read_callback
        )
        if len(rows) < 1:
            raise NotFoundException("There are no restaurant at all.")

        # TODO: return a single row instead of a list ?
        return rows

    async def update_by_name(self, name, new_name):
        try:
            affected_rows = await self._write(
                "UPDATE Restaurants SET name = %(new_name)s WHERE name = %(name)s",
                {'name': name, 'new_name': new_name}
            )
        except UniqueViolation:
            raise ConflictException("A restaurant with that name [%s] already exists." % new_name)

        if affected_rows < 1:
            raise NotFoundException("There are no restaurant with that name [%s]." % name)
