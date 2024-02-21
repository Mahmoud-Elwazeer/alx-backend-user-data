#!/usr/bin/env python3
"""import modules
"""
from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
