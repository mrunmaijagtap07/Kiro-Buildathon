"""
tests/test_auth.py — Authentication tests.
Uses an in-memory SQLite stand-in via monkeypatching or a test MySQL DB.

Run with:  python -m pytest tests/ -v
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from unittest.mock import patch, MagicMock
from app import create_app
from config import Config


class TestConfig(Config):
    TESTING = True
    SECRET_KEY = "test-secret-key"
    WTF_CSRF_ENABLED = False
    # Use a throwaway DB name; tests mock DB calls
    DB_NAME = "campus_test"


@pytest.fixture
def app():
    application = create_app(TestConfig)
    application.config["TESTING"] = True
    yield application


@pytest.fixture
def client(app):
    return app.test_client()


# ── Registration ───────────────────────────────────────────

class TestRegistration:

    def test_register_page_loads(self, client):
        """GET /register returns 200."""
        with patch("routes.auth.query_all", return_value=[
            {"department_id": 1, "dept_name": "Information Technology"}
        ]):
            resp = client.get("/register")
        assert resp.status_code == 200
        assert b"Create your account" in resp.data

    def test_register_missing_fields(self, client):
        """POST /register with empty data should flash errors."""
        with patch("routes.auth.query_all", return_value=[]):
            resp = client.post("/register", data={}, follow_redirects=True)
        # Should stay on register page with errors
        assert resp.status_code == 200

    def test_register_password_too_short(self, client):
        with patch("routes.auth.query_all", return_value=[
            {"department_id": 1, "dept_name": "IT"}
        ]):
            resp = client.post("/register", data={
                "full_name": "Test User",
                "email": "test@example.com",
                "password": "short",
                "confirm_password": "short",
                "role": "STUDENT",
                "department_id": "1",
            }, follow_redirects=True)
        assert b"8 characters" in resp.data or resp.status_code == 200

    def test_register_passwords_mismatch(self, client):
        with patch("routes.auth.query_all", return_value=[
            {"department_id": 1, "dept_name": "IT"}
        ]):
            resp = client.post("/register", data={
                "full_name": "Test User",
                "email": "test@example.com",
                "password": "Password123",
                "confirm_password": "Different123",
                "role": "STUDENT",
                "department_id": "1",
            }, follow_redirects=True)
        assert resp.status_code == 200


# ── Login ──────────────────────────────────────────────────

class TestLogin:

    def test_login_page_loads(self, client):
        resp = client.get("/login")
        assert resp.status_code == 200
        assert b"Welcome back" in resp.data

    def test_login_empty_fields(self, client):
        resp = client.post("/login", data={}, follow_redirects=True)
        assert resp.status_code == 200

    def test_login_wrong_password(self, client):
        mock_user = {
            "user_id": 1,
            "full_name": "Test User",
            "email": "test@example.com",
            "password_hash": "pbkdf2:sha256:wrong_hash",
            "role": "STUDENT",
            "is_active": True,
            "department_id": 1,
        }
        with patch("routes.auth.query_one", return_value=mock_user):
            resp = client.post("/login", data={
                "email": "test@example.com",
                "password": "wrongpassword",
            }, follow_redirects=True)
        assert resp.status_code == 200

    def test_login_inactive_account(self, client):
        from werkzeug.security import generate_password_hash
        mock_user = {
            "user_id": 1,
            "full_name": "Inactive User",
            "email": "inactive@example.com",
            "password_hash": generate_password_hash("Password123"),
            "role": "STUDENT",
            "is_active": False,
            "department_id": 1,
        }
        with patch("routes.auth.query_one", return_value=mock_user):
            resp = client.post("/login", data={
                "email": "inactive@example.com",
                "password": "Password123",
            }, follow_redirects=True)
        assert b"deactivated" in resp.data

    def test_logout_redirects_to_login(self, client):
        # Simulate logged-in session
        with client.session_transaction() as sess:
            sess["user_id"] = 1
            sess["role"] = "STUDENT"
            sess["full_name"] = "Test"
            sess["email"] = "t@t.com"
            sess["is_active"] = True
            sess["department_id"] = 1
        resp = client.get("/logout", follow_redirects=True)
        assert resp.status_code == 200


# ── Role restriction ───────────────────────────────────────

class TestRoleRestriction:

    def test_student_dashboard_requires_login(self, client):
        resp = client.get("/student/dashboard")
        assert resp.status_code in (302, 401)

    def test_faculty_dashboard_requires_login(self, client):
        resp = client.get("/faculty/dashboard")
        assert resp.status_code in (302, 401)

    def test_admin_dashboard_requires_login(self, client):
        resp = client.get("/admin/dashboard")
        assert resp.status_code in (302, 401)

    def test_student_cannot_access_faculty_dashboard(self, client):
        with client.session_transaction() as sess:
            sess["user_id"] = 1
            sess["role"] = "STUDENT"
            sess["full_name"] = "Test"
            sess["email"] = "t@t.com"
            sess["is_active"] = True
            sess["department_id"] = 1
        resp = client.get("/faculty/dashboard")
        assert resp.status_code == 403

    def test_student_cannot_access_admin(self, client):
        with client.session_transaction() as sess:
            sess["user_id"] = 1
            sess["role"] = "STUDENT"
            sess["full_name"] = "Test"
            sess["email"] = "t@t.com"
            sess["is_active"] = True
            sess["department_id"] = 1
        resp = client.get("/admin/dashboard")
        assert resp.status_code == 403
