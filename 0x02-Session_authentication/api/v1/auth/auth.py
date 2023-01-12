#!/usr/bin/env python3
"""
Now you will create a class to manage the API authentication
"""
from flask import request
from typing import List, TypeVar
import os


class Auth():
    """
    class to manage the API authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        that returns False - path and excluded_paths will be used later,
        now, you don’t need to take care of them
        """
        if path is None:
            return True

        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        if path[-1] != '/':
            path += '/'

        for i in excluded_paths:
            if i[-1] == "*":
                if i[:-1] in path:
                    return False

        if path not in excluded_paths:
            return True
        else:
            return False

    def authorization_header(self, request=None) -> str:
        """
        that returns None - request will be the Flask request object
        """
        if request is None:
            return None

        if 'Authorization' not in request.headers:
            return None

        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        that returns None - request will be the Flask request object
        """
        return None

    def session_cookie(self, request=None):
        """
        that returns a cookie value from a request
        """
        if request is None:
            return None

        _my_session_id = os.getenv("SESSION_NAME")
        result = request.cookies.get(_my_session_id)

        return result
