#!/usr/bin/env python3
"""import modules"""
import requests


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """register new user
    """
    url = "http://127.0.0.1:5000/users"
    req = requests.post(url, data={'email': email, 'password': password})
    try:
        assert req.json() == {"email": email, "message": "user created"}
        assert req.status_code == 200
    except Exception:
        assert req.json() == {"message": "email already registered"}
        assert req.status_code == 400


def log_in(email: str, password: str) -> str:
    """log in
    """
    url = "http://127.0.0.1:5000/sessions"
    req = requests.post(url, data={'email': email, 'password': password})
    try:
        assert req.json() == {"email": email, "message": "logged in"}
        assert req.status_code == 200
    except Exception:
        assert req.status_code == 401

    return (req.cookies.get("session_id"))


def log_in_wrong_password(email: str, password: str) -> None:
    """log in wrong password
    """
    url = "http://127.0.0.1:5000/sessions"
    req = requests.post(url, data={'email': email, 'password': password})
    try:
        assert req.json() == {"email": email, "message": "logged in"}
        assert req.status_code == 200
    except Exception:
        assert req.status_code == 401


def profile_unlogged() -> None:
    """forbidden login to profile
    """
    url = "http://127.0.0.1:5000/profile"
    req = requests.get(url, cookies={"session_id": ""})
    assert req.status_code == 403


def profile_logged(session_id: str) -> None:
    """profile log in
    """
    url = "http://127.0.0.1:5000/profile"
    req = requests.get(url, cookies={"session_id": session_id})
    try:
        assert req.json() == {"email": EMAIL}
        assert req.status_code == 200
    except Exception:
        assert req.status_code == 403


def log_out(session_id: str) -> None:
    """logout from account
    """
    url = "http://127.0.0.1:5000/sessions"
    req = requests.delete(url, cookies={"session_id": session_id})
    try:
        assert req.json() == {"message": "Bienvenue"}
        assert req.status_code == 200
    except Exception:
        assert req.status_code == 403


def reset_password_token(email: str) -> str:
    """reset password
    """
    url = "http://127.0.0.1:5000/reset_password"
    req = requests.post(url, data={"email": email})
    try:
        msg = req.json()
        reset_token = msg.get("reset_token")
        assert req.status_code == 200
        assert req.json() == {'email': email, 'reset_token': reset_token}
        return reset_token
    except Exception:
        assert req.status_code == 403


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """update password
    """
    url = "http://127.0.0.1:5000/reset_password"
    req = requests.put(
        url,
        data={
            'email': EMAIL,
            'reset_token': reset_token,
            'new_password': new_password
        }
    )
    try:
        assert req.json() == {"email": EMAIL, "message": "Password updated"}
        assert req.status_code == 200
    except Exception:
        assert req.status_code == 403


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
