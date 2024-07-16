#!/usr/bin/env python3
""" auth module for authentication
"""
from bcrypt import hashpw, gensalt


def _hash_password(password: str) -> bytes:
    """ returns a salted hash of the input password """
    return hashpw(password.encode('utf-8'), gensalt())
