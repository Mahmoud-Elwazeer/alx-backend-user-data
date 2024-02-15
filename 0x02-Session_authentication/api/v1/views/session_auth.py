#!/usr/bin/env python3
"""import modules"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
@app_views.route('/auth_session/login/',
                 methods=['POST'],
                 strict_slashes=False)
def auth_session_login():
    """handle route for the Session authentication login
    """
    email = request.form.get('email')
    if email is None:
        return jsonify({"error": "email missing"}), 400

    pwd = request.form.get('password')
    if pwd is None:
        return jsonify({"error": "password missing"}), 400

    found_users = User.search({'email': email})
    if len(found_users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = None
    for i in found_users:
        if i.is_valid_password(pwd):
            user = i
            break

    if user is None:
        return jsonify({"error": "wrong password"}), 401

    if user:
        from api.v1.app import auth
        out = jsonify(user.to_json())
        name_cookie = getenv('SESSION_NAME')
        out.set_cookie(name_cookie, auth.create_session(user.id))
        return out, 200


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
@app_views.route('/auth_session/logout/', methods=['DELETE'],
                 strict_slashes=False)
def logout_session() -> str:
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({})
