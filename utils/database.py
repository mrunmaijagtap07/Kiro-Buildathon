"""
utils/database.py — Database connection management.

Uses a simple connection-per-request pattern with PyMySQL.
Flask's g object stores the connection for the lifetime of
each request and closes it automatically in teardown.
"""

import pymysql
import pymysql.cursors
from flask import g, current_app
from contextlib import contextmanager


def get_db():
    """
    Return the database connection for the current request.
    Creates a new connection if one does not exist yet.
    The connection is stored in Flask's g object and closed
    automatically by close_db() at request teardown.
    """
    if "db" not in g:
        cfg = current_app.config
        g.db = pymysql.connect(
            host=cfg["DB_HOST"],
            port=cfg["DB_PORT"],
            user=cfg["DB_USER"],
            password=cfg["DB_PASSWORD"],
            database=cfg["DB_NAME"],
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False,
        )
    return g.db


def close_db(e=None):
    """Close the database connection at the end of a request."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_app(app):
    """Register the teardown handler with the Flask app."""
    app.teardown_appcontext(close_db)


# ── Query helpers ─────────────────────────────────────────────

def query_one(sql: str, params=None) -> dict | None:
    """Execute a SELECT and return the first row (or None)."""
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(sql, params or ())
        return cursor.fetchone()


def query_all(sql: str, params=None) -> list[dict]:
    """Execute a SELECT and return all rows."""
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(sql, params or ())
        return cursor.fetchall()


def execute(sql: str, params=None) -> int:
    """
    Execute an INSERT / UPDATE / DELETE.
    Returns lastrowid (useful after INSERT).
    Commits immediately.
    """
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(sql, params or ())
        last_id = cursor.lastrowid
    db.commit()
    return last_id


def execute_many(sql: str, params_list: list) -> None:
    """Execute a statement for each item in params_list. Commits once."""
    db = get_db()
    with db.cursor() as cursor:
        cursor.executemany(sql, params_list)
    db.commit()


@contextmanager
def transaction():
    """
    Context manager for multi-statement transactions.

    Usage:
        with transaction() as cursor:
            cursor.execute(...)
            cursor.execute(...)
        # auto-commits on success, rolls back on exception
    """
    db = get_db()
    try:
        with db.cursor() as cursor:
            yield cursor
        db.commit()
    except Exception:
        db.rollback()
        raise
