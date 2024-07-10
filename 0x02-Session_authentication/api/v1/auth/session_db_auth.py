#!/usr/bin/env python3
""" This module defines SessionDBAuth class
that inherits from SessionAuth class.
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from uuid import uuid4
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """ this class handles expiring sessions """
    def __init__(self):
        super().__init__()

    def create_session(self, user_id=None):
        """ creates a session for user_id """
        sessionID = str(uuid4())
        user_session = UserSession(user_id=user_id, session_id=sessionID)
        user_session.save()
        return sessionID

    def user_id_for_session_id(self, session_id=None):
        """ returns a User ID based on a Session ID """
        if session_id is None:
            return None
        user_session = UserSession.search(
            {'session_id': session_id}
        )
        if not user_session:
            return None
        user_session = user_session[0]
        if self.session_duration <= 0:
            return user_session.user_id
        delta = timedelta(seconds=self.session_duration)
        if user_session.created_at + delta < datetime.utcnow():
            return None
        return user_session.user_id

    def destroy_session(self, request=None):
        """ destroys the UserSession based on the Session ID
        from the request cookie """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_session = UserSession.search({'session_id': session_id})
        if not user_session:
            return False
        user_session = user_session[0]
        user_session.remove()
        return True
