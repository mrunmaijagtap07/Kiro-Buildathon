"""
routes/auth.py — Authentication: registration, login, logout, Google OAuth.
"""

import os
import secrets
import requests
from urllib.parse import urlencode

from flask import (
    Blueprint, render_template, request, redirect, url_for,
    flash, session, current_app, jsonify, g
)
from werkzeug.security import generate_password_hash, check_password_hash

from utils.database import query_one, query_all, execute, transaction
from utils.validators import validate_registration, validate_login
from utils.decorators import login_required

auth_bp = Blueprint("auth", __name__)


# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────

def _set_user_session(user: dict) -> None:
    """Populate Flask session from a user record."""
    session.permanent = True
    session["user_id"]      = user["user_id"]
    session["full_name"]    = user["full_name"]
    session["email"]        = user["email"]
    session["role"]         = user["role"]
    session["department_id"]= user["department_id"]
    session["is_active"]    = bool(user["is_active"])


def _role_redirect(role: str) -> str:
    """Return the dashboard URL for a given role."""
    return {
        "STUDENT": url_for("student.dashboard"),
        "FACULTY": url_for("faculty.dashboard"),
        "ADMIN":   url_for("admin.dashboard"),
    }.get(role, url_for("main.home"))


# ─────────────────────────────────────────────────────────────
# Registration
# ─────────────────────────────────────────────────────────────

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect(_role_redirect(session["role"]))

    departments = query_all(
        "SELECT department_id, dept_name FROM departments WHERE is_active=1 ORDER BY dept_name"
    )

    if request.method == "POST":
        data = request.form.to_dict()
        errors = validate_registration(data)

        if not errors:
            # Check email uniqueness
            existing = query_one("SELECT user_id FROM users WHERE email=%s", (data["email"].strip().lower(),))
            if existing:
                errors.append("An account with this email already exists.")

        if not errors:
            # Check roll_or_emp_id uniqueness if provided
            roll = data.get("roll_or_emp_id", "").strip() or None
            if roll:
                dup = query_one("SELECT user_id FROM users WHERE roll_or_emp_id=%s", (roll,))
                if dup:
                    errors.append("This Roll/Employee ID is already registered.")

        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("auth/register.html", departments=departments, form=data)

        pw_hash = generate_password_hash(data["password"])
        user_id = execute(
            """INSERT INTO users
               (full_name, email, password_hash, role, department_id, roll_or_emp_id, auth_provider)
               VALUES (%s, %s, %s, %s, %s, %s, 'LOCAL')""",
            (
                data["full_name"].strip(),
                data["email"].strip().lower(),
                pw_hash,
                data["role"],
                int(data["department_id"]),
                roll,
            )
        )

        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", departments=departments, form={})


# ─────────────────────────────────────────────────────────────
# Login
# ─────────────────────────────────────────────────────────────

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(_role_redirect(session["role"]))

    if request.method == "POST":
        data = request.form.to_dict()
        errors = validate_login(data)

        if not errors:
            email = data["email"].strip().lower()
            user = query_one(
                "SELECT * FROM users WHERE email=%s",
                (email,)
            )

            if not user or not user.get("password_hash"):
                errors.append("Invalid email or password.")
            elif not check_password_hash(user["password_hash"], data["password"]):
                errors.append("Invalid email or password.")
            elif not user["is_active"]:
                errors.append("Your account has been deactivated. Contact an administrator.")

        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("auth/login.html", form=data)

        # Update last_login_at
        execute("UPDATE users SET last_login_at=NOW() WHERE user_id=%s", (user["user_id"],))
        _set_user_session(user)

        next_url = request.args.get("next")
        if next_url and next_url.startswith("/"):
            return redirect(next_url)
        return redirect(_role_redirect(user["role"]))

    return render_template("auth/login.html", form={})


# ─────────────────────────────────────────────────────────────
# Logout
# ─────────────────────────────────────────────────────────────

@auth_bp.route("/logout")
@login_required
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))


# ─────────────────────────────────────────────────────────────
# Google OAuth — Step 1: Redirect to Google
# ─────────────────────────────────────────────────────────────

@auth_bp.route("/auth/google")
def google_login():
    cfg = current_app.config

    if not cfg.get("GOOGLE_CLIENT_ID") or not cfg.get("GOOGLE_CLIENT_SECRET"):
        flash(
            "Google login is not configured. "
            "Please set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in your .env file.",
            "warning"
        )
        return redirect(url_for("auth.login"))

    # Generate CSRF state token
    state = secrets.token_urlsafe(32)
    session["oauth_state"] = state

    params = urlencode({
        "client_id":     cfg["GOOGLE_CLIENT_ID"],
        "redirect_uri":  cfg["GOOGLE_REDIRECT_URI"],
        "response_type": "code",
        "scope":         "openid email profile",
        "state":         state,
        "access_type":   "online",
        "prompt":        "select_account",
    })

    return redirect(f"{cfg['GOOGLE_AUTH_URL']}?{params}")


# ─────────────────────────────────────────────────────────────
# Google OAuth — Step 2: Callback
# ─────────────────────────────────────────────────────────────

@auth_bp.route("/auth/google/callback")
def google_callback():
    cfg = current_app.config
    error = request.args.get("error")
    if error:
        flash(f"Google login failed: {error}", "danger")
        return redirect(url_for("auth.login"))

    # CSRF check
    state = request.args.get("state")
    if state != session.pop("oauth_state", None):
        flash("Invalid OAuth state. Please try again.", "danger")
        return redirect(url_for("auth.login"))

    code = request.args.get("code")
    if not code:
        flash("No authorization code received from Google.", "danger")
        return redirect(url_for("auth.login"))

    # Exchange code for tokens
    try:
        token_resp = requests.post(
            cfg["GOOGLE_TOKEN_URL"],
            data={
                "code":          code,
                "client_id":     cfg["GOOGLE_CLIENT_ID"],
                "client_secret": cfg["GOOGLE_CLIENT_SECRET"],
                "redirect_uri":  cfg["GOOGLE_REDIRECT_URI"],
                "grant_type":    "authorization_code",
            },
            timeout=10,
        )
        token_data = token_resp.json()
    except requests.RequestException as e:
        current_app.logger.error(f"Google token exchange failed: {e}")
        flash("Could not connect to Google. Please try again.", "danger")
        return redirect(url_for("auth.login"))

    access_token = token_data.get("access_token")
    if not access_token:
        flash("Google authentication failed. Please try again.", "danger")
        return redirect(url_for("auth.login"))

    # Fetch user profile
    try:
        userinfo_resp = requests.get(
            cfg["GOOGLE_USERINFO_URL"],
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10,
        )
        userinfo = userinfo_resp.json()
    except requests.RequestException:
        flash("Could not retrieve profile from Google.", "danger")
        return redirect(url_for("auth.login"))

    google_id   = userinfo.get("sub")
    email       = (userinfo.get("email") or "").lower()
    full_name   = userinfo.get("name") or email.split("@")[0]
    verified    = userinfo.get("email_verified", False)

    if not google_id or not email:
        flash("Could not retrieve your Google profile information.", "danger")
        return redirect(url_for("auth.login"))

    if not verified:
        flash("Your Google account email is not verified.", "danger")
        return redirect(url_for("auth.login"))

    # ── Find or create user ────────────────────────────────────
    # 1. Look up by google_id
    user = query_one("SELECT * FROM users WHERE google_id=%s", (google_id,))

    if not user:
        # 2. Look up by email (existing local account → link Google)
        user = query_one("SELECT * FROM users WHERE email=%s", (email,))
        if user:
            # Link this Google account to existing user
            new_provider = "BOTH" if user["auth_provider"] == "LOCAL" else user["auth_provider"]
            execute(
                "UPDATE users SET google_id=%s, auth_provider=%s, last_login_at=NOW() WHERE user_id=%s",
                (google_id, new_provider, user["user_id"])
            )
            user["google_id"] = google_id
            user["auth_provider"] = new_provider
        else:
            # 3. New user via Google — create account (role/dept to be completed)
            user_id = execute(
                """INSERT INTO users
                   (full_name, email, google_id, auth_provider, role, department_id, is_active)
                   VALUES (%s, %s, %s, 'GOOGLE', 'STUDENT', NULL, 1)""",
                (full_name, email, google_id)
            )
            user = query_one("SELECT * FROM users WHERE user_id=%s", (user_id,))

    if not user["is_active"]:
        flash("Your account has been deactivated. Contact an administrator.", "danger")
        return redirect(url_for("auth.login"))

    execute("UPDATE users SET last_login_at=NOW() WHERE user_id=%s", (user["user_id"],))
    _set_user_session(user)

    # If new Google user hasn't set role/dept, send to profile completion
    if not user.get("department_id"):
        flash("Welcome! Please complete your profile to continue.", "info")
        return redirect(url_for("auth.complete_profile"))

    flash(f"Welcome back, {user['full_name']}!", "success")
    return redirect(_role_redirect(user["role"]))


# ─────────────────────────────────────────────────────────────
# Complete Profile (for new Google OAuth users)
# ─────────────────────────────────────────────────────────────

@auth_bp.route("/auth/complete-profile", methods=["GET", "POST"])
@login_required
def complete_profile():
    user_id = session["user_id"]
    departments = query_all(
        "SELECT department_id, dept_name FROM departments WHERE is_active=1 ORDER BY dept_name"
    )

    if request.method == "POST":
        role   = request.form.get("role", "").strip()
        dept   = request.form.get("department_id", "").strip()
        roll   = request.form.get("roll_or_emp_id", "").strip() or None

        errors = []
        if role not in ("STUDENT", "FACULTY"):
            errors.append("Please select a valid role.")
        if not dept:
            errors.append("Please select your department.")
        if roll:
            dup = query_one(
                "SELECT user_id FROM users WHERE roll_or_emp_id=%s AND user_id!=%s",
                (roll, user_id)
            )
            if dup:
                errors.append("This Roll/Employee ID is already registered.")

        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("auth/complete_profile.html", departments=departments)

        execute(
            "UPDATE users SET role=%s, department_id=%s, roll_or_emp_id=%s WHERE user_id=%s",
            (role, int(dept), roll, user_id)
        )
        # Update session
        session["role"] = role
        session["department_id"] = int(dept)

        flash("Profile completed! Welcome to CampusArchive.", "success")
        return redirect(_role_redirect(role))

    return render_template("auth/complete_profile.html", departments=departments)
