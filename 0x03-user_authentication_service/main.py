#!/usr/bin/env python3
"""
defines some functions to test this web app
"""
import requests


def register_user(email: str, password: str) -> None:
    """ tests a succesful registeration process """
    res = requests.post(
        url='http://0.0.0.0:5000/users',
        data={'email': email, 'password': password}
    )
    assert res.status_code == 200
    assert res.json() == {'email': email, 'message': 'user created'}


def log_in_wrong_password(email: str, password: str) -> None:
    """ tests a login process with wrong password """
    res = requests.post(
        url='http://0.0.0.0:5000/sessions',
        data={'email': email, 'password': password}
    )
    assert res.status_code == 401


def log_in(email: str, password: str) -> str:
    """ tests a login process with wrong password """
    res = requests.post(
        url='http://0.0.0.0:5000/sessions',
        data={'email': email, 'password': password}
    )
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "logged in"}
    assert res.cookies.get('session_id') is not None
    return res.cookies.get('session_id')


def profile_unlogged() -> None:
    """ test get profile with no session_id """
    res = requests.get(
        url='http://0.0.0.0:5000/profile',
    )
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    """ test get profile with valid session_id """
    res = requests.get(
        url='http://0.0.0.0:5000/profile',
        cookies={'session_id': session_id}
    )
    assert res.status_code == 200


def log_out(session_id: str) -> None:
    """ tests the logout proccess """
    res = requests.delete(
        url='http://0.0.0.0:5000/sessions',
        cookies={'session_id': session_id}
    )
    assert res.status_code == 200
    assert res.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """ tests the reset_password_token proccess """
    res = requests.post(
        url='http://0.0.0.0:5000/reset_password',
        data={'email': email}
    )
    assert res.status_code == 200
    reset_token = res.json().get('reset_token')
    assert reset_token is not None
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    res = requests.put(
        url='http://0.0.0.0:5000/reset_password',
        data={
            'email': email,
            'reset_token': reset_token,
            'new_password': new_password,
        }
    )
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


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
