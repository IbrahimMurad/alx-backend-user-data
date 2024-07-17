#!/usr/bin/env python3
""" This is flask app
"""
from auth import Auth
from flask import (
    abort,
    Flask,
    jsonify,
    redirect,
    request,
    url_for
)


AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def basic() -> str:
    """ GET /
    Return: a JSON payload: {"message": "Bienvenue"}
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """ POST /users
    an end-point to register a user
    Returns: a JSON payload: {"email": "<email>", "message": "user created"}
    Or: a JSON payload: {"message": "email already registered"}
    with a 400 status code
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if email and password:
        try:
            user = AUTH.register_user(email, password)
            return jsonify({"email": user.email, "message": "user created"})
        except ValueError:
            return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ POST /sessions
    create a new session for the user
    Returns:
        str: {"email": "<user email>", "message": "logged in"}
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if not email or not password:
        abort(401)
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    if session_id is None:
        abort(401)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie('session_id', session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """ DELETE /sessions
    logout the user
    If the user exists destroy the session and redirect the user to GET /.
    If the user does not exist, respond with a 403 HTTP status."""
    session_id = request.cookies.get('session_id')
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect(url_for('basic'))
    abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
