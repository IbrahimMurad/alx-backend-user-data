#!/usr/bin/env python3
""" auth module for authentication
"""
from bcrypt import hashpw, gensalt, checkpw
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from typing import Optional
from user import User
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """ returns a salted hash of the input password """
    return hashpw(password.encode('utf-8'), gensalt())


def _generate_uuid() -> str:
    """  return a string representation of a new UUID """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ takes an email string and a password string as arguments
        and returns a User object.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """ locates the user by email.
        If it exists, check the password with bcrypt.checkpw.
        If it matches return True.
        In any other case, return False.
        """
        try:
            user = self._db.find_user_by(email=email)
            return checkpw(password.encode('utf-8'), user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """ takes an email string argument and
        returns the session ID as a string """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            user.session_id = session_id
            self._db._session.commit()
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """ finds user by session id """
        if not session_id:
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except Exception:
            return None

    def destroy_session(self, user_id: str) -> None:
        """  updates the corresponding user’s session ID to None """
        if user_id:
            return self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """ finds the user corresponding to the email.
        If the user does not exist, raise a ValueError exception.
        If it exists, generate a UUID and
        update the user’s reset_token database field.
        Return the token
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """ uses the reset_token to find the corresponding user.
        If it does not exist, raise a ValueError exception.
        Otherwise, hash the password and
        update the user’s hashed_password field
        with the new hashed password and the reset_token field to None.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            user.reset_token = None
            self._db.update_user(
                user.id,
                hashed_password=_hash_password(password)
                )
        except NoResultFound:
            raise ValueError
