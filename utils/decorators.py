"""
utils/decorators.py — Route protection decorators.

Usage:
    @login_required
    @role_required('FACULTY', 'ADMIN')
    def my_view():
        ...
"""

from functools import wraps
from flask import session, redirect, url_for, flash, abort, request, jsonify


def login_required(f):
    """Redirect unauthenticated users to the login page."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            # API routes want JSON, not a redirect
            if request.path.startswith("/api/"):
                return jsonify({"success": False, "message": "Authentication required."}), 401
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("auth.login", next=request.path))
        return f(*args, **kwargs)
    return decorated


def role_required(*roles):
    """
    Allow only users whose role is in the given roles list.
    Must be used AFTER @login_required so session['role'] is set.
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            user_role = session.get("role")
            if user_role not in roles:
                if request.path.startswith("/api/"):
                    return jsonify({"success": False, "message": "Access denied."}), 403
                abort(403)
            return f(*args, **kwargs)
        return decorated
    return decorator


def student_required(f):
    """Shorthand: only STUDENT role."""
    return login_required(role_required("STUDENT")(f))


def faculty_required(f):
    """Shorthand: only FACULTY role."""
    return login_required(role_required("FACULTY")(f))


def admin_required(f):
    """Shorthand: only ADMIN role."""
    return login_required(role_required("ADMIN")(f))


def active_required(f):
    """
    Block inactive (deactivated) accounts even if they have a session.
    Must be used AFTER @login_required.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("is_active", True):
            session.clear()
            flash("Your account has been deactivated. Contact an administrator.", "danger")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated
