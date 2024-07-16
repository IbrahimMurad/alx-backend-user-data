#!/usr/bin/env python3
""" DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base
from user import User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(
        self,
        email: str,
        hashed_password: str,
        **kwargs: dict
    ) -> User:
        """ adds a new user to the users table """
        id = None
        session_id = None
        reset_token = None
        for key, value in kwargs.items():
            if key == 'id':
                id = value
            elif key == 'session_id':
                session_id = value
            elif key == 'reset_token':
                reset_token = value
        new_user = User(
            email=email,
            hashed_password=hashed_password,
            **kwargs
            )
        self._session.add(new_user)
        self._session.commit()
        return new_user
