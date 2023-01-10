#!/usr/bin/env python3
"""
"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        """
        if authorization_header is None:
            return None

        if type(authorization_header) is not str:
            return None

        if authorization_header[:6] == "Basic ":
            return authorization_header[6:]

        return None

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """
        """
        if base64_authorization_header is None:
            return None

        if type(base64_authorization_header) is not str:
            return None

        try:
            result = b64decode(base64_authorization_header)
            return result.decode("utf-8")

        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        """
        """
        if decoded_base64_authorization_header is None:
            return (None, None)

        if type(decoded_base64_authorization_header) is not str:
            return (None, None)

        if ":" not in decoded_base64_authorization_header:
            return (None, None)

        else:
            result = decoded_base64_authorization_header.split(":", 1)
            return (result[0], result[1])

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        """
        if user_email is None or type(user_email) is not str:
            return None

        if user_pwd is None or type(user_pwd) is not str:
            return None

        try:
            data = User.search({'email': user_email})

        except Exception:
            return None

        for comprobation in data:
            if comprobation.is_valid_password(user_pwd):
                return comprobation

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        """
        basic_auth = self.authorization_header(request)
        extract_base64 = self.extract_base64_authorization_header(basic_auth)
        decode = self.decode_base64_authorization_header(extract_base64)
        email_pwd = self.extract_user_credentials(decode)
        user = self.user_object_from_credentials(email_pwd[0], email_pwd[1])

        return user
