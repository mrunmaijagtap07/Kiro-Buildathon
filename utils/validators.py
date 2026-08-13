"""
utils/validators.py — Server-side input validation helpers.

All public functions return a list of error strings.
An empty list means validation passed.
"""

import re
from datetime import datetime


_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_ROLL_RE  = re.compile(r"^[A-Za-z0-9/_\-]{3,50}$")


def validate_registration(data: dict) -> list[str]:
    """Validate registration form data. Returns list of error messages."""
    errors = []

    full_name = (data.get("full_name") or "").strip()
    if not full_name:
        errors.append("Full name is required.")
    elif len(full_name) < 2 or len(full_name) > 100:
        errors.append("Full name must be between 2 and 100 characters.")

    email = (data.get("email") or "").strip().lower()
    if not email:
        errors.append("Email address is required.")
    elif not _EMAIL_RE.match(email):
        errors.append("Enter a valid email address.")

    password = data.get("password") or ""
    if not password:
        errors.append("Password is required.")
    elif len(password) < 8:
        errors.append("Password must be at least 8 characters long.")
    elif len(password) > 128:
        errors.append("Password must be less than 128 characters.")

    confirm = data.get("confirm_password") or ""
    if password and confirm and password != confirm:
        errors.append("Passwords do not match.")

    role = data.get("role") or ""
    if role not in ("STUDENT", "FACULTY"):
        errors.append("Please select a valid role (Student or Faculty).")

    dept = data.get("department_id") or ""
    if not dept:
        errors.append("Please select your department.")

    roll = (data.get("roll_or_emp_id") or "").strip()
    if roll and not _ROLL_RE.match(roll):
        errors.append("Roll/Employee ID contains invalid characters.")

    return errors


def validate_login(data: dict) -> list[str]:
    errors = []
    if not (data.get("email") or "").strip():
        errors.append("Email address is required.")
    if not data.get("password"):
        errors.append("Password is required.")
    return errors


def validate_project_submission(data: dict) -> list[str]:
    """Validate project submission form data."""
    errors = []

    title = (data.get("title") or "").strip()
    if not title:
        errors.append("Project title is required.")
    elif len(title) < 5:
        errors.append("Title must be at least 5 characters.")
    elif len(title) > 255:
        errors.append("Title must be less than 255 characters.")

    abstract = (data.get("abstract") or "").strip()
    if not abstract:
        errors.append("Abstract is required.")
    elif len(abstract) < 50:
        errors.append("Abstract must be at least 50 characters.")
    elif len(abstract) > 5000:
        errors.append("Abstract must be less than 5000 characters.")

    year = data.get("academic_year")
    try:
        year_int = int(year)
        current = datetime.now().year
        if year_int < 2000 or year_int > current:
            errors.append(f"Academic year must be between 2000 and {current}.")
    except (TypeError, ValueError):
        errors.append("Please select a valid academic year.")

    if not data.get("department_id"):
        errors.append("Please select a department.")

    if not data.get("guide_id"):
        errors.append("Please select a faculty guide.")

    return errors


def validate_review(data: dict) -> list[str]:
    errors = []
    decision = data.get("decision") or ""
    if decision not in ("APPROVED", "REJECTED", "REVISION_REQUESTED"):
        errors.append("Invalid review decision.")
    comments = (data.get("comments") or "").strip()
    if decision in ("REJECTED", "REVISION_REQUESTED") and not comments:
        errors.append("Please provide comments explaining your decision.")
    if comments and len(comments) > 2000:
        errors.append("Comments must be less than 2000 characters.")
    return errors
