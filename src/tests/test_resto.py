#!/usr/bin/env python3

import pytest
from aiohttp import web
from configparser import ConfigParser

from resto.server import resto_app


async def check_names(client, expected_names):
    to_be_found = list(expected_names)
    resp = await client.get('/restaurants')
    assert resp.status == 200
    assert len(await resp.json()) == len(expected_names)
    for row in await resp.json():
        assert 'name' in row
        assert row['name'] in to_be_found
        to_be_found.remove(row['name'])

    assert len(to_be_found) == 0


@pytest.fixture
async def client(loop, aiohttp_client):
    cfg = ConfigParser()
    # TODO: resto-server allows using different configuration path.
    cfg.read('/etc/peopledoc-test/resto.ini')
    app = await resto_app(cfg)
    return await aiohttp_client(app)


async def test_read_all_empty(client):
    await check_names(client, [])


async def test_read_not_found(client):
    resp = await client.get("/restaurants/I don't exist")
    assert resp.status == 404
    assert 'error' in await resp.json()


async def test_read_random_no_result(client):
    resp = await client.get('/restaurants', params={'random': 'true'})
    assert resp.status == 404
    assert 'error' in await resp.json()


async def test_create_one(client):
    resp = await client.post('/restaurants', json={'name': 'test_one'})
    assert resp.status == 200
    assert await resp.json() is None


async def test_create_duplicate(client):
    resp = await client.post('/restaurants', json={'name': 'test_one'})
    assert resp.status == 409  # Conflict
    assert 'error' in await resp.json()


async def test_create_another(client):
    resp = await client.post('/restaurants', json={'name': 'test_two'})
    assert resp.status == 200
    assert await resp.json() is None


async def test_create_no_param(client):
    resp = await client.post('/restaurants')
    assert resp.status == 400
    assert 'error' in await resp.json()


async def test_create_bad_json(client):
    resp = await client.post('/restaurants', data=b'not a valid json')
    assert resp.status == 400
    assert 'error' in await resp.json()


async def test_read_one(client):
    resp = await client.get('/restaurants/test_one')
    assert resp.status == 200
    assert len(await resp.json()) == 1
    assert (await resp.json())[0]['name'] == 'test_one'


async def test_read_random(client):
    resp = await client.get('/restaurants', params={'random': 'true'})
    assert resp.status == 200
    assert len(await resp.json()) == 1
    assert (await resp.json())[0]['name'] in ('test_one', 'test_two')
    # TODO: loop test to ensure it's not just always returning the same row


async def test_read_all_after_creates(client):
    await check_names(client, ['test_one', 'test_two'])


async def test_update_one(client):
    resp = await client.patch('/restaurants/test_one', json={'name': 'test_one_updated'})
    assert resp.status == 200
    assert await resp.json() is None


async def test_update_duplicate(client):
    resp = await client.patch('/restaurants/test_two', json={'name': 'test_one_updated'})
    assert resp.status == 409  # Conflict
    assert 'error' in await resp.json()


async def test_update_not_found(client):
    resp = await client.patch("/restaurants/I don't exist", json={'name': "I should'nt exist"})
    assert resp.status == 404
    assert 'error' in await resp.json()


async def test_update_no_param(client):
    resp = await client.patch('/restaurants')
    assert resp.status == 400
    assert 'error' in await resp.json()


async def test_update_bad_json(client):
    resp = await client.patch('/restaurants/test_two', data=b'not a valid json')
    assert resp.status == 400
    assert 'error' in await resp.json()


async def test_update_no_name(client):
    resp = await client.patch('/restaurants', json={'name': "I shouldn't exist"})
    assert resp.status == 400
    assert 'error' in await resp.json()


async def test_update_no_new_name(client):
    resp = await client.patch('/restaurants/test_two')
    assert resp.status == 400
    assert 'error' in await resp.json()


async def test_read_all_after_updates(client):
    await check_names(client, ['test_one_updated', 'test_two'])


async def test_delete_one(client):
    resp = await client.delete('/restaurants/test_one_updated')
    assert resp.status == 200
    assert await resp.json() is None


async def test_delete_not_found(client):
    resp = await client.delete("/restaurants/I don't exist")
    assert resp.status == 404
    assert 'error' in await resp.json()


async def test_delete_no_param(client):
    resp = await client.delete('/restaurants')
    assert resp.status == 400
    assert 'error' in await resp.json()


async def test_read_all_after_first_delete(client):
    await check_names(client, ['test_two'])


async def test_delete_another(client):
    resp = await client.delete('/restaurants/test_two')
    assert resp.status == 200
    assert await resp.json() is None


async def test_create_special_characters(client):
    # TODO: / and # characters must be url encoded when used in url (get / patch / delete)
    # Test all special characters.
    resp = await client.post(
        '/restaurants',
        json={'name': '^$€|!§ \' " < ~ (àéîøù)'}
    )
    assert resp.status == 200
    assert await resp.json() is None


async def test_read_all_special_characters(client):
    await check_names(client, ['^$€|!§ \' " < ~ (àéîøù)'])


async def test_read_one_special_characters(client):
    resp = await client.get('/restaurants/^$€|!§ \' " < ~ (àéîøù)')
    assert resp.status == 200
    assert len(await resp.json()) == 1
    assert (await resp.json())[0]['name'] == '^$€|!§ \' " < ~ (àéîøù)'


async def test_delete_special_characters(client):
    resp = await client.delete('/restaurants/^$€|!§ \' " < ~ (àéîøù)')
    assert resp.status == 200
    assert await resp.json() is None


async def test_create_max_characters(client):
    resp = await client.post('/restaurants', json={'name': 'a' * 255})
    assert resp.status == 200
    assert await resp.json() is None


async def test_create_too_much_characters(client):
    resp = await client.post('/restaurants', json={'name': 'a' * 256})
    assert resp.status == 400
    assert 'error' in await resp.json()


async def test_delete_max_characters(client):
    resp = await client.delete('/restaurants/' + 'a' * 255)
    assert resp.status == 200
    assert await resp.json() is None


async def test_read_all_empty_final(client):
    await check_names(client, [])
