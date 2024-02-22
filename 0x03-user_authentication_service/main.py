#!/usr/bin/env python3
"""import modules"""
import requests


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    url = "http://127.0.0.1:5000/users"
    req = requests.post(url, data={'email': EMAIL, 'password': PASSWD })
    try:
        assert req.json() == { "email": EMAIL, "message": "user created" }
        assert req.status_code == 200
    except Exception:
        assert req.json() == {"message": "email already registered"}
        assert req.status_code == 400


def log_in(email: str, password: str) -> str:
    pass


def log_in_wrong_password(email: str, password: str) -> None:
    pass


def profile_unlogged() -> None:
    pass


def profile_logged(session_id: str) -> None:
    pass


def log_out(session_id: str) -> None:
    pass


def reset_password_token(email: str) -> str:
    pass


def update_password(email: str, reset_token: str, new_password: str) -> None:
    pass


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)

