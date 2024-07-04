#!/usr/bin/env python3
""" module to Implement a hash_password function
that expects one string argument name password
and returns a salted, hashed password, which is a byte string.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ function that returns a salted, hashed password, which is a byte string """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())