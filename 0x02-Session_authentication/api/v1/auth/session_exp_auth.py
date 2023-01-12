#!/usr/bin/env python3
"""
Create a class SessionExpAuth that inherits from SessionAuth
"""
from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """
    class SessionExpAuth that inherits from SessionAuth
    """
    def __init__(self):
        """
        method initialized
        """
        try:
            self.session_duration = int(os.getenv("SESSION_DURATION"))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Return the Session ID created
        """
        try:
            session = super().create_session(user_id)
        except Exception:
            return None

        session_dictionary = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session] = session_dictionary

        return session

    def user_id_for_session_id(self, session_id=None):
        """
        return user_id from the session dictionary
        """
        if session_id is None:
            return None

        if session_id not in self.user_id_by_session_id:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)

        if self.session_duration <= 0:
            return session_dict.get('user_id')

        if 'created_at' not in session_dict:
            return None

        time = session_dict.get('created_at')
        session_connect = timedelta(seconds=self.session_duration)

        if time + session_connect < datetime.now():
            return None

        return session_dict.get('user_id')
