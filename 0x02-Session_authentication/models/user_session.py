#!/usr/bin/env python3
""" User_session module
"""
from models.base import Base


class UserSession(Base):
    """ User class
    """

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a UserSession instance
        """
        self.user_id: str = kwargs.get('user_id')
        self.session_id: str = kwargs.get('session_id')
