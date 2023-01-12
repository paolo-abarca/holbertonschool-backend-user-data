#!/usr/bin/env python3
"""
Create a new model UserSession in models/user_session.py
that inherits from Base
"""
from models.base import Base


class UserSession(Base):
    """
    class usersession that inherits from base
    """
    def __init__(self, *args: list, **kwargs: dict):
        """
        method initialized
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
