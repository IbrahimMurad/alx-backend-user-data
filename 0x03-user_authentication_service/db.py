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
        self._engine = create_engine("sqlite:///a.db", echo=False)
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

    def add_user(self, email: str, hashed_password: str) -> User:
        """ takes in an email string and a hashed_password string
        as arguments and returns a User object.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """ takes in arbitrary keyword arguments and returns the first row
        found in the users table as filtered by the method’s input arguments.
        """
        return self._session.query(User).filter_by(**kwargs).one()

    def update_user(self, user_id: int, **kwargs) -> None:
        """ uses find_user_by to locate the user to update,
        then will update the user’s attributes
        as passed in the method’s arguments
        then commit changes to the database.

        Args:
            user_id (str): id of the user to update
            kwargs: keyward arguments to be updated in user

        return: None
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError
            setattr(user, key, value)
        self._session.commit()
        return None
