#!/usr/bin/env python3
"""import modules"""

from flask import request
from typing import List, TypeVar
from models.user import User
from os import getenv


class Auth:
    """ class to manage the API authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ True if the path is not in the list of strings excluded_paths:
        """
        if path is None or excluded_paths is None:
            return True
        if path in excluded_paths:
            return False
        if (path + '/') in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """ validate all requests to secure the API
        """
        if request is None:
            return None

        authorization_header = request.headers.get('Authorization')
        if authorization_header:
            return authorization_header
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ returns None - request will be the Flask request object
        """
        return None

    def session_cookie(self, request=None):
        """ returns a cookie value from a request
        """
        if request is None:
            return None
        
        cookie_name = getenv('SESSION_NAME')
        return request.cookies.get(cookie_name)
