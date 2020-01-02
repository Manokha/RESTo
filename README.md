# RESTo: a REST API for restaurants
### Requirements
This module requires:
- an installed and configured postgresql server.
- a python 3.8 installation.

## Install:
```sh
pip3 install .
```

### Configure
Copy /etc/peopledoc-test/resto.example.ini to /etc/peopledoc-test/resto.ini

Set postgresql connection informations. You're set !

## Test:
```sh
pytest
```
/!\ There are deprecation warnings as aiohttp uses deprecated arguments (loop).

## Documentation:
https://web.postman.co/collections/9855198-6d064006-9222-486e-af6f-296f89787925?version=latest&workspace=88b07ed0-f43c-4e10-852b-fbab0be77dec

### Explorations
- aiohttp-graphql: https://github.com/graphql-python/aiohttp-graphql
- aiopg vs asyncpg ? (asyncpg would be much faster but doesn't implement dbapi)
- tavern testing (yaml tests) : https://taverntesting.github.io/

### Evolutions
- Improve documentation.
- Improve logs.
- Implement a reload function for the configuration file.
- Install init.d script (through debian package ?).
- Implement profiling.
- Use sqlalchemy ?
- Use a gateway for authentication / rate-limiting etc (Kong ?).
- Make restaurant name the last part of url instead of a standard parameter, github style.
- Handle web handler cancellation using asyncio.shield (https://docs.aiohttp.org/en/stable/web_advanced.html#web-handler-cancellation).
- Package using docker or .deb or both.
- Test python 3.6 compatibility for pypy, then pypy and check performance gains.
