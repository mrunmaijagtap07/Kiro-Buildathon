"""
routes/faculty.py — Faculty dashboard and review workflow.
"""

from flask import (
    Blueprint, render_template, request, redirect, url_for,
    flash, session, abort, jsonify, current_app
)

from utils.database import query_one, query_all, execute, transaction
from utils.decorators import login_required, role_required
from utils.validators import validate_review
from utils.helpers import status_badge_class, status_display, decision_display
from utils.file_handler import human_readable_size

faculty_bp = Blueprint("faculty", __name__, url_prefix="/faculty")


def _faculty_required(f):
    return login_required(role_required("FACULTY")(f))


# ─────────────────────────────────────────────────────────────
# Dashboard
# ─────────────────────────────────────────────────────────────

@faculty_bp.route("/dashboard")
@_faculty_required
def dashboard():
    guide_id = session["user_id"]

    stats = query_one(
        """SELECT
             COUNT(*) AS total,
             SUM(status='PENDING') AS pending,
             SUM(status='NEEDS_REVISION') AS needs_revision,
             SUM(status='APPROVED') AS approved,
             SUM(status='REJECTED') AS rejected
           FROM projects
           WHERE guide_id=%s AND deleted_at IS NULL""",
        (guide_id,)
    )

    pending_projects = query_all(
        """SELECT p.project_id, p.title, p.submitted_at, p.academic_year,
                  d.dept_name, ls.full_name AS lead_name
           FROM projects p
           JOIN departments d ON d.department_id=p.department_id
           JOIN users ls ON ls.user_id=p.lead_student_id
           WHERE p.guide_id=%s AND p.status='PENDING' AND p.deleted_at IS NULL
           ORDER BY p.submitted_at ASC""",
        (guide_id,)
    )

    revision_projects = query_all(
        """SELECT p.project_id, p.title, p.submitted_at, p.academic_year,
                  d.dept_name, ls.full_name AS lead_name
           FROM projects p
           JOIN departments d ON d.department_id=p.department_id
           JOIN users ls ON ls.user_id=p.lead_student_id
           WHERE p.guide_id=%s AND p.status='NEEDS_REVISION' AND p.deleted_at IS NULL
           ORDER BY p.submitted_at ASC""",
        (guide_id,)
    )

    recent_reviews = query_all(
        """SELECT fr.review_id, fr.decision, fr.reviewed_at,
                  p.project_id, p.title
           FROM faculty_reviews fr
           JOIN projects p ON p.project_id=fr.project_id
           WHERE fr.faculty_id=%s
           ORDER BY fr.reviewed_at DESC
           LIMIT 5""",
        (guide_id,)
    )

    return render_template(
        "faculty/dashboard.html",
        stats=stats,
        pending_projects=pending_projects,
        revision_projects=revision_projects,
        recent_reviews=recent_reviews,
        status_badge_class=status_badge_class,
        status_display=status_display,
        decision_display=decision_display,
    )


# ─────────────────────────────────────────────────────────────
# Review queue (full list of assigned projects)
# ─────────────────────────────────────────────────────────────

@faculty_bp.route("/reviews")
@_faculty_required
def reviews():
    guide_id   = session["user_id"]
    status_filter = request.args.get("status", "")

    conditions = ["p.guide_id=%s", "p.deleted_at IS NULL"]
    params     = [guide_id]

    if status_filter:
        conditions.append("p.status=%s")
        params.append(status_filter)

    where = " AND ".join(conditions)

    projects = query_all(
        f"""SELECT p.project_id, p.title, p.status, p.submitted_at, p.academic_year,
                   d.dept_name, ls.full_name AS lead_name
            FROM projects p
            JOIN departments d ON d.department_id=p.department_id
            JOIN users ls ON ls.user_id=p.lead_student_id
            WHERE {where}
            ORDER BY
              FIELD(p.status,'PENDING','NEEDS_REVISION','APPROVED','REJECTED'),
              p.submitted_at ASC""",
        params
    )

    return render_template(
        "faculty/reviews.html",
        projects=projects,
        status_filter=status_filter,
        status_badge_class=status_badge_class,
        status_display=status_display,
    )


# ─────────────────────────────────────────────────────────────
# Review a specific project
# ─────────────────────────────────────────────────────────────

@faculty_bp.route("/review/<int:project_id>", methods=["GET", "POST"])
@_faculty_required
def review(project_id: int):
    guide_id = session["user_id"]

    project = query_one(
        """SELECT p.*, d.dept_name,
                  ls.full_name AS lead_name, ls.email AS lead_email, ls.roll_or_emp_id AS lead_roll
           FROM projects p
           JOIN departments d ON d.department_id=p.department_id
           JOIN users ls ON ls.user_id=p.lead_student_id
           WHERE p.project_id=%s AND p.guide_id=%s AND p.deleted_at IS NULL""",
        (project_id, guide_id)
    )

    if not project:
        abort(404)

    authors = query_all(
        """SELECT u.full_name, u.email, u.roll_or_emp_id
           FROM project_authors pa
           JOIN users u ON u.user_id=pa.student_id
           WHERE pa.project_id=%s""",
        (project_id,)
    )
    tags = query_all(
        "SELECT t.tag_name FROM tags t JOIN project_tags pt ON pt.tag_id=t.tag_id WHERE pt.project_id=%s",
        (project_id,)
    )
    attachments = query_all(
        "SELECT * FROM project_attachments WHERE project_id=%s ORDER BY file_type",
        (project_id,)
    )
    review_history = query_all(
        """SELECT fr.*, u.full_name AS faculty_name
           FROM faculty_reviews fr
           JOIN users u ON u.user_id=fr.faculty_id
           WHERE fr.project_id=%s
           ORDER BY fr.reviewed_at DESC""",
        (project_id,)
    )

    if request.method == "POST":
        # Only allow review if status is PENDING or NEEDS_REVISION
        if project["status"] not in ("PENDING", "NEEDS_REVISION"):
            flash("This project cannot be reviewed in its current status.", "warning")
            return redirect(url_for("faculty.review", project_id=project_id))

        data    = request.form.to_dict()
        errors  = validate_review(data)

        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template(
                "faculty/review.html",
                project=project, authors=authors, tags=tags,
                attachments=attachments, review_history=review_history,
                status_badge_class=status_badge_class, status_display=status_display,
                decision_display=decision_display, human_readable_size=human_readable_size,
            )

        decision = data["decision"]
        comments = (data.get("comments") or "").strip()

        # Map decision → project status
        status_map = {
            "APPROVED":           "APPROVED",
            "REJECTED":           "REJECTED",
            "REVISION_REQUESTED": "NEEDS_REVISION",
        }
        new_status = status_map[decision]

        try:
            with transaction() as cursor:
                cursor.execute(
                    "UPDATE projects SET status=%s WHERE project_id=%s",
                    (new_status, project_id)
                )
                cursor.execute(
                    """INSERT INTO faculty_reviews (project_id, faculty_id, decision, comments)
                       VALUES (%s, %s, %s, %s)""",
                    (project_id, guide_id, decision, comments or None)
                )
        except Exception as e:
            current_app.logger.error(f"Review submission error: {e}")
            flash("An error occurred saving the review. Please try again.", "danger")
            return redirect(url_for("faculty.review", project_id=project_id))

        decision_labels = {
            "APPROVED":           "approved",
            "REJECTED":           "rejected",
            "REVISION_REQUESTED": "sent back for revision",
        }
        flash(f"Project has been {decision_labels[decision]}.", "success")
        return redirect(url_for("faculty.dashboard"))

    return render_template(
        "faculty/review.html",
        project=project, authors=authors, tags=tags,
        attachments=attachments, review_history=review_history,
        status_badge_class=status_badge_class, status_display=status_display,
        decision_display=decision_display, human_readable_size=human_readable_size,
    )
