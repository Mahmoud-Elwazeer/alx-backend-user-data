#!/usr/bin/env python3
"""import modules"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """ returned bytes is a salted hash of the input password, hashed
    """
    convert_to_bytes = password.encode('utf-8')

    salt = bcrypt.gensalt()
    hash_pass = bcrypt.hashpw(convert_to_bytes, salt)
    return hash_pass
