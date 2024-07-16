#!/usr/bin/env python3
""" auth module for authentication
"""
from bcrypt import hashpw, gensalt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from typing import TypeVar


def _hash_password(password: str) -> bytes:
    """ returns a salted hash of the input password """
    return hashpw(password.encode('utf-8'), gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> TypeVar('User'):
        """ hashes the password of the user with whose email is email """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            return self._db.add_user(
                email=email,
                hashed_password=_hash_password(password)
                )
