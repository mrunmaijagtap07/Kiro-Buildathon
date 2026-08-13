"""
config.py — Centralized application configuration.
All values come from environment variables (loaded from .env).
Never hard-code secrets here.
"""

import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


def _require(key: str) -> str:
    """Read an env var; raise a clear error if it is missing."""
    val = os.getenv(key)
    if not val:
        raise RuntimeError(
            f"Required environment variable '{key}' is not set. "
            f"Copy .env.example to .env and fill in your values."
        )
    return val


class Config:
    # ── Flask ──────────────────────────────────────────────────
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-insecure-key-change-in-production")
    DEBUG: bool = os.getenv("FLASK_DEBUG", "0") == "1"
    TESTING: bool = False

    # ── Session ────────────────────────────────────────────────
    SESSION_COOKIE_HTTPONLY: bool = True
    SESSION_COOKIE_SAMESITE: str = "Lax"
    PERMANENT_SESSION_LIFETIME: timedelta = timedelta(
        hours=int(os.getenv("SESSION_LIFETIME_HOURS", "8"))
    )

    # ── Database ───────────────────────────────────────────────
    DB_HOST: str = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT: int = int(os.getenv("DB_PORT", "3306"))
    DB_NAME: str = os.getenv("DB_NAME", "campus_repository")
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")

    # ── File Uploads ───────────────────────────────────────────
    UPLOAD_FOLDER: str = os.getenv("UPLOAD_FOLDER", "uploads")
    MAX_REPORT_SIZE_MB: int = int(os.getenv("MAX_REPORT_SIZE_MB", "20"))
    MAX_SOURCE_SIZE_MB: int = int(os.getenv("MAX_SOURCE_SIZE_MB", "50"))
    MAX_DIAGRAM_SIZE_MB: int = int(os.getenv("MAX_DIAGRAM_SIZE_MB", "10"))

    # Flask's MAX_CONTENT_LENGTH is the hard ceiling for any single request.
    # Set it to the largest allowed upload + some buffer.
    MAX_CONTENT_LENGTH: int = (int(os.getenv("MAX_SOURCE_SIZE_MB", "50")) + 5) * 1024 * 1024

    ALLOWED_REPORT_EXTENSIONS: set = {"pdf"}
    ALLOWED_SOURCE_EXTENSIONS: set = {"zip"}
    ALLOWED_DIAGRAM_EXTENSIONS: set = {"pdf", "png", "jpg", "jpeg", "gif", "svg"}

    # ── Google OAuth ───────────────────────────────────────────
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    GOOGLE_REDIRECT_URI: str = os.getenv(
        "GOOGLE_REDIRECT_URI", "http://localhost:5000/auth/google/callback"
    )
    # Google OAuth endpoints (public, no secret needed)
    GOOGLE_AUTH_URL: str = "https://accounts.google.com/o/oauth2/v2/auth"
    GOOGLE_TOKEN_URL: str = "https://oauth2.googleapis.com/token"
    GOOGLE_USERINFO_URL: str = "https://www.googleapis.com/oauth2/v3/userinfo"

    @property
    def google_oauth_enabled(self) -> bool:
        return bool(self.GOOGLE_CLIENT_ID and self.GOOGLE_CLIENT_SECRET)

    # ── Application URL ────────────────────────────────────────
    APP_BASE_URL: str = os.getenv("APP_BASE_URL", "http://localhost:5000")


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True  # Require HTTPS in production


# Select config based on FLASK_ENV
_configs = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}

ActiveConfig = _configs.get(os.getenv("FLASK_ENV", "development"), DevelopmentConfig)
