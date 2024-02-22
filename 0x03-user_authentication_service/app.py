#!/usr/bin/env python3
"""import modules
"""
from flask import Flask, jsonify, request, abort
from flask import redirect, url_for
from auth import Auth
import requests

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
        email = request.form['email']
        pwd = request.form['password']
    except KeyError:
        abort(400)

    if auth.valid_login(email, pwd):
        session_id = auth.create_session(email)
        out = jsonify({"email": email, "message": "logged in"})
        out.set_cookie("session_id", session_id)
        return out

    abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
