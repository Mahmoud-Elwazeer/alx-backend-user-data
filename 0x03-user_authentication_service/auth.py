#!/usr/bin/env python3
"""import modules"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid
from typing import Union


def _generate_uuid() -> str:
    """eturn a string representation of a new UUID.
    """
    return str(uuid.uuid4())


def _hash_password(password: str) -> bytes:
    """ returned bytes is a salted hash of the input password, hashed
    """
    convert_to_bytes = password.encode('utf-8')

    salt = bcrypt.gensalt()
    hash_pass = bcrypt.hashpw(convert_to_bytes, salt)
    return hash_pass


def _check_password(password: str, hash: bytes) -> bool:
    """checks a password against a hashed value
    """
    valid = False
    byte = password.encode('utf-8')
    if bcrypt.checkpw(byte, hash):
        valid = True
    return valid


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ method using to register new user
        """
        if email is None or password is None:
            raise Exception(
                "Function take two argumets string (email, password)")

        try:
            user = self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            user = self._db.add_user(
                email=email,
                hashed_password=_hash_password(password)
                )
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Credentials validation
        """
        try:
            user = self._db.find_user_by(email=email)
            result = _check_password(password, user.hashed_password)
            return result

        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """It takes an email string argument and
        returns the session ID as a string.
        """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return None

        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[str, None]:
        """Find user by session ID
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroy session
        """
        self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """Generate reset password token if user exists
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token
