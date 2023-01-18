#!/usr/bin/env python3
"""
Create a Flask app that has a single GET route ("/") and use
flask.jsonify to return a JSON payload of the form
"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def home():
    """
    route ("/") and use flask.jsonify to return a JSON
    payload of the form
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def register_user():
    """
    route("/users")  should expect two form data fields:
    "email" and "password"
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})

    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """
    route("/sessions") create a new session for the user, store it
    the session ID as a cookie with key "session_id" on the response
    and return a JSON payload of the form
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    result = jsonify({"email": email, "message": "logged in"})
    result.set_cookie('session_id', session_id)

    return result


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """
    route("/sessions") destroy the session and redirect the user to GET /
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)

    if not user:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile():
    """
    route("/profile") If the user exist, respond with a 200 HTTP
    status and the following JSON payload
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)

    if user is not None:
        return jsonify({"email": user.email}), 200

    abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """
    route("/reset_password") generate a token and respond with a
    200 HTTP status and the following JSON payload
    """
    email = request.form.get('email')

    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token}), 200

    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password():
    """
    route("/reset_password") Update the password. If the token is
    invalid, catch the exception and respond with a 403 HTTP code
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200

    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
