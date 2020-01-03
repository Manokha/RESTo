#!/usr/bin/env python3


class RestoException(Exception):
    def __init__(self, msg='Something bad happened.'):
        super().__init__(msg)


class NotFoundException(RestoException):
    pass


class ConflictException(RestoException):
    pass
