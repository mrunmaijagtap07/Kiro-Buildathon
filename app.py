"""
app.py — CampusArchive Flask application entry point.

Creates and configures the Flask app, registers blueprints,
error handlers, and template utilities.
"""

import os
from flask import Flask, render_template, session, g
from dotenv import load_dotenv

load_dotenv()

from config import ActiveConfig
from utils import database as db_utils
from utils.helpers import status_badge_class, status_display, decision_display
from utils.file_handler import human_readable_size


def create_app(config=None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config or ActiveConfig)

    # Ensure upload subdirectories exist
    for subdir in ("reports", "source", "diagrams"):
        os.makedirs(os.path.join(app.config["UPLOAD_FOLDER"], subdir), exist_ok=True)

    # ── Database ───────────────────────────────────────────────
    db_utils.init_app(app)

    # ── Blueprints ─────────────────────────────────────────────
    from routes.auth     import auth_bp
    from routes.student  import student_bp
    from routes.faculty  import faculty_bp
    from routes.admin    import admin_bp
    from routes.projects import projects_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(faculty_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(projects_bp)

    # ── Home page route (main) ─────────────────────────────────
    from flask import Blueprint, redirect, url_for
    main_bp = Blueprint("main", __name__)

    @main_bp.route("/")
    def home():
        from utils.database import query_one, query_all
        stats = query_one(
            """SELECT
                 (SELECT COUNT(*) FROM projects WHERE status='APPROVED' AND deleted_at IS NULL) AS approved_projects,
                 (SELECT COUNT(*) FROM departments WHERE is_active=1) AS departments,
                 (SELECT COUNT(*) FROM users WHERE role='FACULTY' AND is_active=1) AS faculty_count,
                 (SELECT COUNT(*) FROM tags WHERE is_active=1) AS tag_count"""
        )
        recent = query_all(
            """SELECT p.project_id, p.title, p.academic_year,
                      d.dept_name, u.full_name AS guide_name
               FROM projects p
               JOIN departments d ON d.department_id=p.department_id
               JOIN users u ON u.user_id=p.guide_id
               WHERE p.status='APPROVED' AND p.deleted_at IS NULL
               ORDER BY p.submitted_at DESC
               LIMIT 6"""
        )
        for proj in recent:
            from utils.database import query_all as qa
            proj["tags"] = qa(
                "SELECT t.tag_name FROM tags t JOIN project_tags pt ON pt.tag_id=t.tag_id WHERE pt.project_id=%s LIMIT 3",
                (proj["project_id"],)
            )
        return render_template("home.html", stats=stats, recent_projects=recent)

    @main_bp.route("/about")
    def about():
        return render_template("about.html")

    app.register_blueprint(main_bp)

    # ── Template globals ───────────────────────────────────────
    @app.context_processor
    def inject_globals():
        return {
            "status_badge_class": status_badge_class,
            "status_display":     status_display,
            "decision_display":   decision_display,
            "human_readable_size": human_readable_size,
            "google_oauth_enabled": bool(
                app.config.get("GOOGLE_CLIENT_ID") and app.config.get("GOOGLE_CLIENT_SECRET")
            ),
        }

    # ── Error handlers ─────────────────────────────────────────
    @app.errorhandler(400)
    def bad_request(e):
        return render_template("errors/400.html"), 400

    @app.errorhandler(403)
    def forbidden(e):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(413)
    def too_large(e):
        return render_template("errors/413.html"), 413

    @app.errorhandler(500)
    def server_error(e):
        app.logger.error(f"500 error: {e}")
        return render_template("errors/500.html"), 500

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=app.config.get("DEBUG", True))
