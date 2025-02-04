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


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """ GET /profile
    The request is expected to contain a session_id cookie.
    Use it to find the user.
    If the user exist, respond with a 200 HTTP status
    and the following JSON payload:
    {"email": "<user email>"}
    """
    session_id = request.cookies.get('session_id')
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return jsonify({"email": user.email}), 200
    abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """ POST /reset_password
    The request is expected to contain form data with the "email" field.
    If the email is not registered, respond with a 403 status code.
    Otherwise, generate a token and respond with a 200 HTTP status
    and the following JSON payload:
    {"email": "<user email>", "reset_token": "<reset token>"}
    """
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({'email': email, 'reset_token': token})
    except Exception:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """
    The request is expected to contain form data with fields
    "email", "reset_token" and "new_password".

    Update the password.

    If the token is invalid, catch the exception and
    respond with a 403 HTTP code.

    If the token is valid, respond with a 200 HTTP code
    and the following JSON payload:
    {"email": "<user email>", "message": "Password updated"}
    """

    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    if email and reset_token and new_password:
        try:
            AUTH.update_password(reset_token, new_password)
            return jsonify({"email": email, "message": "Password updated"})
        except Exception:
            pass
    abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
