#!/usr/bin/env python3
""" This module defines SessionExpAuth class
that inherits from SessionAuth class.
"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """ this class handles expiring sessions """
    def __init__(self):
        """ Instantiate attributes """
        ses_duration = getenv('SESSION_DURATION')
        try:
            self.session_duration = int(ses_duration)
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ creates a session for user_id """
        sessionID = super().create_session(user_id)
        if sessionID is None:
            return None
        self.user_id_by_session_id.update(
            {
                sessionID: {
                    'user_id': user_id,
                    'created_at': datetime.now()
                }
            }
        )
        return sessionID

    def user_id_for_session_id(self, session_id=None):
        """ returns a User ID based on a Session ID """
        if (
            session_id is None
            or session_id not in self.user_id_by_session_id.keys()
        ):
            return None
        session_dictionary = self.user_id_by_session_id.get(session_id)
        if self.session_duration <= 0:
            return session_dictionary.get('user_id')
        if 'created_at' not in session_dictionary.keys():
            return None
        created_at = session_dictionary.get('created_at')
        delta = timedelta(seconds=self.session_duration)
        if created_at + delta < datetime.now():
            return None
        return session_dictionary.get('user_id')
