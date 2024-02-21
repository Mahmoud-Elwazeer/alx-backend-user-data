#!/usr/bin/env python3
"""import modules"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """ returned bytes is a salted hash of the input password, hashed
    """
    convert_to_bytes = password.encode('utf-8')

    salt = bcrypt.gensalt()
    hash_pass = bcrypt.hashpw(convert_to_bytes, salt)
    return hash_pass


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