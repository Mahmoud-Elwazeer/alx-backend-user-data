#!/usr/bin/env python3
"""import modules
"""
from flask import Flask, jsonify, request, abort
from flask import redirect, url_for
from auth import Auth

app = Flask(__name__)
auth = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def home() -> str:
    """home route
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register() -> str:
    """registration route
    """
    email = request.form.get("email")
    if email is None:
        return jsonify({"error": "email missing"}), 400

    pwd = request.form.get("password")
    if pwd is None:
        return jsonify({"error": "password missing"}), 400

    try:
        user = auth.register_user(email, pwd)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """Logs in a user and returns session ID
    """
    try:
        email = request.form.get('email')
        pwd = request.form.get('password')
    except KeyError:
        abort(400)

    if not auth.valid_login(email, pwd):
        abort(401)

    session_id = auth.create_session(email)
    out = jsonify({"email": email, "message": "logged in"})
    out.set_cookie("session_id", session_id)
    return out


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """logout route
    """
    session_id = request.cookies.get("session_id", None)
    if session_id is None:
        abort(403)

    user = auth.get_user_from_session_id(session_id)
    if user is None:
        abort(403)

    auth.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """User profile
    """
    session_id = request.cookies.get("session_id", None)
    if session_id is None:
        abort(403)

    user = auth.get_user_from_session_id(session_id)
    if user is None:
        abort(403)

    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def reset_pass():
    """Get reset password token using to reset password
    """
    email = request.form.get("email")
    if email is None:
        abort(403)

    try:
        reset_token = auth.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token})
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """Update password route
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    if email is None or reset_token is None or new_password is None:
        abort(403)

    try:
        auth.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"})
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
