#!/usr/bin/env python3
"""
Create one function for each of the following tasks
"""
import requests


def register_user(email: str, password: str) -> None:
    """
    test for register_user
    """
    query = requests.post("http://127.0.0.1:5000/users",
                          data={"email": email, "password": password})

    if query.status_code == 200:
        assert (query.json() == {"email": email, "message": "user created"})

    if query.status_code == 400:
        assert (query.json() == {"message": "email already registered"})


def log_in_wrong_password(email: str, password: str) -> None:
    """
    test for log_in_wrong_password
    """
    query = requests.post("http://127.0.0.1:5000/sessions",
                          data={"email": email, "password": password})

    if query.status_code == 200:
        assert (query.json() == {"email": email, "message": "logged in"})

    else:
        assert (query.status_code == 401)


def log_in(email: str, password: str) -> str:
    """
    test for log_in
    """
    query = requests.post("http://127.0.0.1:5000/sessions",
                          data={"email": email, "password": password})

    if query.status_code == 200:
        assert (query.json() == {"email": email, "message": "logged in"})
        return query.cookies["session_id"]

    else:
        assert (query.status_code == 401)


def profile_unlogged() -> None:
    """
    test for profile_unlogged
    """
    query = requests.get("http://127.0.0.1:5000/profile")
    assert (query.status_code == 403)


def profile_logged(session_id: str) -> None:
    """
    test for profile_logged
    """
    cookies = {"session_id": session_id}
    query = requests.get("http://127.0.0.1:5000/profile", cookies=cookies)
    assert (query.status_code == 200)


def log_out(session_id: str) -> None:
    """
    test for log_out
    """
    cookies = {"session_id": session_id}
    query = requests.delete("http://127.0.0.1:5000/sessions", cookies=cookies)
    assert(query.status_code == 200)


def reset_password_token(email: str) -> str:
    """
    test for reset_password_token
    """
    query = requests.post("http://127.0.0.1:5000/reset_password",
                          data={"email": email})

    if query.status_code == 200:
        assert (query.json() == {"email": email,
                                 "reset_token": query.json()["reset_token"]})
        return query.json()["reset_token"]

    assert (query.status_code == 403)


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    test for update_password
    """
    query = requests.put("http://127.0.0.1:5000/reset_password",
                         data={"email": email, "reset_token": reset_token,
                               "new_password": new_password})
    assert (query.status_code == 200)
    assert (query.json() == {"email": email, "message": "Password updated"})


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
