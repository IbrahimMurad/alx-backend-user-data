#!/usr/bin/env python3
""" Module of Users views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session_login() -> str:
    """ POST /api/v1/auth_session/login
    Return:
        - Return the dictionary representation of the current User
    """
    email = request.form.get('email')
    if not email:
        return jsonify({ "error": "email missing" }), 400
    password = request.form.get('password')
    if not password:
        return jsonify({ "error": "password missing" }), 400
    user = User.search({'email': email})
    if not user:
        return jsonify({ "error": "no user found for this email" }), 404
    if not user[0].is_valid_password(password):
        return jsonify({ "error": "wrong password" }), 401
    user = user[0]
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    res = jsonify(user.to_json())
    session_name = getenv('SESSION_NAME')
    res.set_cookie(session_name, session_id)
    return res


@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """ DELETE /api/v1/auth_session/login
    Return:
        - Return empty json (indicating that the session is deleted)
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
