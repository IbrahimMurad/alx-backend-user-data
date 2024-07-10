#!/usr/bin/env python3
""" This module defines SessionDBAuth class
that inherits from SessionAuth class.
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ this class handles expiring sessions """
    def create_session(self, user_id=None):
        """ creates a session for user_id """
        sessionID = super().create_session(user_id)
        user_session = UserSession(user_id=user_id, session_id=sessionID)
        user_session.save()
        return sessionID

    def user_id_for_session_id(self, session_id=None):
        """ returns a User ID based on a Session ID """
        if session_id is None:
            return None
        user_session = UserSession.search({'session_id': session_id})[0]
        return user_session.user_id

    def destroy_session(self, request=None):
        """ destroys the UserSession based on the Session ID
        from the request cookie """
        sessionID_from_cookie = self.session_cookie(request)
        user_session = UserSession.search(
            {'session_id': sessionID_from_cookie}
        )[0]
        user_session.remove()
