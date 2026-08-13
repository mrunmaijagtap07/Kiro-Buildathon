"""
utils/auth.py — Authentication helper utilities.
Session user retrieval and role checks used in templates/routes.
"""

from flask import session
from utils.database import query_one


def get_current_user() -> dict | None:
    """Return the full user record for the logged-in user, or None."""
    user_id = session.get("user_id")
    if not user_id:
        return None
    return query_one("SELECT * FROM users WHERE user_id=%s", (user_id,))


def is_logged_in() -> bool:
    return "user_id" in session


def current_role() -> str:
    return session.get("role", "")
