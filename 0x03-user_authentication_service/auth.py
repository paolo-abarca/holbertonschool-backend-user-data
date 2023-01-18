#!/usr/bin/env python3
"""
In this task you will define a _hash_password method that
takes in a password string arguments and returns bytes
"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
from sqlalchemy.exc import InvalidRequestError
import uuid
from typing import Union


def _hash_password(password: str) -> bytes:
    """
    method that takes in a password string arguments and returns bytes
    """
    hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hash


def _generate_uuid() -> str:
    """
    function should return a string representation of a new UUID.
    Use the uuid module
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """
        method initialized
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        method hash the password with _hash_password, save the user
        to the database using self._db and return the User object
        """
        try:
            if self._db.find_user_by(email=email):
                raise ValueError("User {} already exists".format(email))

        except NoResultFound:
            pwd = _hash_password(password).decode("utf-8")
            user = self._db.add_user(email, pwd)

            return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        method should expect email and password required
        arguments and return a boolean
        """
        if email is None or password is None:
            return False

        try:
            user = self._db.find_user_by(email=email)
            pwd = user.hashed_password
            return bcrypt.checkpw(password.encode(), pwd.encode('utf-8'))

        except (NoResultFound, InvalidRequestError):
            return False

    def create_session(self, email: str) -> str:
        """
        method should find the user corresponding to the email,
        generate a new UUID and store it in the database as the
        user’s session_id, then return the session ID
        """
        try:
            user = self._db.find_user_by(email=email)
            id_user = _generate_uuid()
            self._db.update_user(user.id, session_id=id_user)
            return id_user

        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        method takes a single session_id string argument and returns
        the corresponding User or None
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user

        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        method takes a single user_id integer argument and returns None
        """
        try:
            self._db.update_user(user_id, session_id=None)

        except ValueError:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """
        method  generate a UUID and update the user’s reset_token
        database field. Return the token
        """
        try:
            user = self._db.find_user_by(email=email)
            id_user = _generate_uuid()
            self._db.update_user(user.id, reset_token=id_user)
            return id_user

        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """
        method it takes reset_token string argument and a
        password string argument and returns None
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            pwd = _hash_password(password).decode('utf-8')

            self._db.update_user(user.id, hashed_password=pwd,
                                 reset_token=None)

        except NoResultFound:
            raise ValueError
