# RESTo: a REST API for restaurants
### Requirements
This module requires:
- an installed and configured postgresql server.
- a python 3.8 installation.

## Install:
```sh
pip3 install .
```

### Database
Apply sql/install.sql to desired user (this will create Restaurants table).

### Configure
Copy /etc/peopledoc-test/resto.example.ini to /etc/peopledoc-test/resto.ini

Set postgresql connection informations. You're set !

## Test:
```sh
pytest
```
/!\ There are deprecation warnings as aiohttp uses deprecated arguments (loop).

## Launch:
### Help:
```
$ resto-server --help
usage: resto-server [-h] [-c CONFIGURATION]

resto server

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIGURATION, --configuration CONFIGURATION
                        Configuration file path (default: /etc/peopledoc-test/resto.ini).
```

### Examples:
```sh
resto-server
```
```sh
resto-server -c test-resto.ini
```

## Documentation:
[Postman documentation](https://documenter.getpostman.com/view/9855198/SWEDzESm)

### Explorations
- aiohttp-graphql: https://github.com/graphql-python/aiohttp-graphql
- aiopg vs asyncpg ? (asyncpg would be much faster but doesn't implement dbapi)
- tavern testing (yaml tests) : https://taverntesting.github.io/

### Evolutions
- Improve documentation.
- Improve logs.
- Implement a reload function for the configuration file.
- Install init.d script (through debian package ?).
- Create table automatically.
- Implement profiling.
- Use sqlalchemy ?
- Use a gateway for authentication / rate-limiting etc (Kong ?).
- Make restaurant name the last part of url instead of a standard parameter, github style.
- Handle web handler cancellation using asyncio.shield (https://docs.aiohttp.org/en/stable/web_advanced.html#web-handler-cancellation).
- Package using docker or .deb or both.
- Test python 3.6 compatibility for pypy, then pypy and check performance gains.
