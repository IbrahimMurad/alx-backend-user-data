#!/usr/bin/env python3
""" This is flask app
"""
from auth import Auth
from flask import Flask, jsonify, request


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
    Or: a JSON payload: {"message": "email already registered"} with a 400 status code
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if email and password:
        try:
            user = AUTH.register_user(email,password)
            return jsonify({"email": user.email, "message": "user created"})
        except ValueError:
            return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
