"""
utils/helpers.py — Miscellaneous helper utilities.
"""

from datetime import datetime


def current_academic_year() -> int:
    """
    Return the current academic year.
    Academic year is the calendar year in which the academic
    session started (e.g., 2024 for the 2024-25 session).
    If we are before July, we consider it the previous year's session.
    """
    now = datetime.now()
    return now.year if now.month >= 7 else now.year - 1


def academic_year_choices(start: int = 2015) -> list[int]:
    """Return a list of academic years from start to current."""
    return list(range(current_academic_year(), start - 1, -1))


def status_badge_class(status: str) -> str:
    """Return a CSS class name for a project status badge."""
    return {
        "PENDING":        "badge-pending",
        "NEEDS_REVISION": "badge-revision",
        "APPROVED":       "badge-approved",
        "REJECTED":       "badge-rejected",
    }.get(status, "badge-pending")


def status_display(status: str) -> str:
    """Return a human-friendly status label."""
    return {
        "PENDING":        "Pending Review",
        "NEEDS_REVISION": "Revision Requested",
        "APPROVED":       "Approved",
        "REJECTED":       "Rejected",
    }.get(status, status)


def decision_display(decision: str) -> str:
    """Return a human-friendly review decision label."""
    return {
        "APPROVED":           "Approved",
        "REJECTED":           "Rejected",
        "REVISION_REQUESTED": "Revision Requested",
    }.get(decision, decision)


def paginate(items: list, page: int, per_page: int) -> dict:
    """
    Simple in-memory pagination helper.
    Returns a dict with: items, page, per_page, total, pages.
    Prefer DB-level LIMIT/OFFSET for large datasets.
    """
    total = len(items)
    pages = max(1, (total + per_page - 1) // per_page)
    page = max(1, min(page, pages))
    start = (page - 1) * per_page
    return {
        "items":    items[start:start + per_page],
        "page":     page,
        "per_page": per_page,
        "total":    total,
        "pages":    pages,
    }
