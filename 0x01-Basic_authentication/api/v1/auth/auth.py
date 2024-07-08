#!/usr/bin/env python3
"""
This module defines Auth class that manages the API authentication.
"""
from flask import request
import re
from models.user import User
from typing import List, TypeVar


class Auth:
    """ manages the API authentication """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ returns True if the path is not in the list of strings
        excluded_paths """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if path[-1] != '/':
            path += '/'
        for ex_path in excluded_paths:
            if ex_path[-1] == '*':
                ex_path = ex_path[:-1]
            if re.match(ex_path, path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ validates all requests to secure the API """
        if request is None or request.headers.get('Authorization') is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ retrieves the User instance for a request """
        return None
