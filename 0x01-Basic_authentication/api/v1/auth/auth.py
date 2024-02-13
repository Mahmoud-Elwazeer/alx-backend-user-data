#!/usr/bin/env python3
"""import modules"""

from flask import request
from typing import List, TypeVar
from models.user import User


class Auth:
    """ class to manage the API authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ returns False - path and excluded_paths will be used later
        """
        return False

    def authorization_header(self, request=None) -> str:
        """returns None - request will be the Flask request object
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ returns None - request will be the Flask request object
        """
        return None
