#!/usr/bin/env python3
"""
Create a new Flask view that handles all routes
for the Session authentication
"""
from flask import jsonify, request
from api.v1.views import app_views
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session():
    """
    create a Session ID for the User ID
    """
    email_user = request.form.get('email')
    password_user = request.form.get('password')

    if not email_user or len(email_user) == 0:
        return jsonify({"error": "email missing"}), 400

    if not password_user or len(password_user) == 0:
        return jsonify({"error": "password missing"}), 400

    try:
        data = User.search({'email': email_user})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if not data:
        return jsonify({"error": "no user found for this email"}), 404

    for i in data:
        if not i.is_valid_password(password_user):
            return jsonify({"error": "wrong password"}), 401

    user = data[0]
    from api.v1.app import auth

    cookie = os.getenv('SESSION_NAME')
    session = auth.create_session(user.id)
    result = jsonify(user.to_json())
    result.set_cookie(cookie, session)

    return result


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def delete_session():
    """
    return an empty JSON dictionary with the status code 200
    """
    from api.v1.app import auth

    delete_user = auth.destroy_session(request)
    if not delete_user:
        abort(404)

    return jsonify({}), 200
