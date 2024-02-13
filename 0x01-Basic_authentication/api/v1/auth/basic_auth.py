#!/usr/bin/env python3
"""import modules"""

from .auth import Auth
import base64


class BasicAuth(Auth):
    """ Basic authentication method using encode base64
    """
    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """return the decoded value of a
        Base64 string base64_authorization_header"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded = base64.b64decode(base64_authorization_header)
            return decoded.decode('utf-8')
        except Exception:
            return None
