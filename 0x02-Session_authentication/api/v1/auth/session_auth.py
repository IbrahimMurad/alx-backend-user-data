#!/usr/bin/env python3
""" This module defines SessionAuth class that inherits from Auth class.
"""
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """ a session Authentication class """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ creates a Session ID for a user_id """
        if user_id is None or not isinstance(user_id, str):
            return None
        SessionID = str(uuid4())
        self.user_id_by_session_id.update({SessionID: user_id})
        return SessionID

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ returns a User ID based on a Session ID """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ overloads the one from Auth and
        returns a User instance based on a cookie value """
        my_session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(my_session_id)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """ LogOut: deletes the user session """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False
        self.user_id_by_session_id.pop(session_id)
        return True
