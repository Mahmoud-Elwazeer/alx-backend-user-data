#!/usr/bin/env python3
"""import modules
"""
from flask import Flask, jsonify, request, abort
from auth import Auth

app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def home():
    """home route
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register():
    """registration route
    """
    email = request.form.get("email")
    if email is None:
        return jsonify({"error": "email missing"}), 400

    pwd = request.form.get("password")
    if pwd is None:
        return jsonify({"error": "password missing"}), 400

    auth = Auth()
    try:
        user = auth.register_user(email, pwd)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """login route
    """
    email = request.form.get("email")
    if email is None:
        abort(401)

    pwd = request.form.get("password")
    if pwd is None:
        abort(401)

    auth = Auth()
    if auth.valid_login(email, pwd):
        session_id = auth.create_session(email)
        out = jsonify({"email": email, "message": "logged in"})
        out.set_cookie("session_id", session_id)
        return out, 200

    abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
