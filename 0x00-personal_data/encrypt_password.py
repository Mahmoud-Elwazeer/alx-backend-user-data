#!/usr/bin/env python3
"""import libraries"""

import bcrypt


def hash_password(password: str) -> bytes:
    """a salted, hashed password, which is a byte string"""
    # converting password to array of bytes
    byte = password.encode('utf-8')

    # generating the salt
    salt = bcrypt.gensalt()

    hash_passwd = bcrypt.hashpw(byte, salt)

    return hash_passwd


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ to validate that the provided password matches the hashed password."""
    valid = False
    byte = password.encode('utf-8')
    if bcrypt.checkpw(byte, hashed_password):
        valid = True

    return valid

