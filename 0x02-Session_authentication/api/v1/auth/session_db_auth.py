#!/usr/bin/env python3
"""
Create a new authentication class SessionDBAuth in
api/v1/auth/session_db_auth.py that inherits from SessionExpAuth
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta
from flask import request


class SessionDBAuth(SessionExpAuth):
    """
    class SessionDBAuth that inherits from SessionExpAuth
    """
    def create_session(self, user_id=None) -> str:
        """
        that creates and stores new instance of
        UserSession and returns the Session ID
        """
        try:
            session_id = super().create_session(user_id)
        except Exception:
            return None

        if type(session_id) == str:
            kwargs = {
                'user_id': user_id,
                'session_id': session_id,
            }
            user_session = UserSession(**kwargs)
            user_session.save()

            return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        that returns the User ID by requesting
        UserSession in the database based on session_id
        """
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None

        if len(sessions) <= 0:
            return None

        time = sessions[0].created_at
        session_connect = timedelta(seconds=self.session_duration)

        if time + session_connect < datetime.now():
            return None

        else:
            return sessions[0].user_id

    def destroy_session(self, request=None) -> bool:
        """
        that destroys the UserSession based on
        the Session ID from the request cookie
        """
        session_id = self.session_cookie(request)
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False

        if len(sessions) <= 0:
            return False

        sessions[0].remove()

        return True
