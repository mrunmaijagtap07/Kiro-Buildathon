"""
routes/admin.py — Admin dashboard: user management, departments, tags, statistics.
"""

from flask import (
    Blueprint, render_template, request, redirect, url_for,
    flash, session, abort, jsonify
)

from utils.database import query_one, query_all, execute
from utils.decorators import login_required, role_required
from utils.helpers import status_badge_class, status_display

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def _admin_required(f):
    return login_required(role_required("ADMIN")(f))


# ─────────────────────────────────────────────────────────────
# Dashboard
# ─────────────────────────────────────────────────────────────

@admin_bp.route("/dashboard")
@_admin_required
def dashboard():
    user_stats = query_one(
        """SELECT
             COUNT(*) AS total_users,
             SUM(role='STUDENT') AS students,
             SUM(role='FACULTY') AS faculty,
             SUM(role='ADMIN') AS admins,
             SUM(is_active=0) AS inactive
           FROM users"""
    )
    project_stats = query_one(
        """SELECT
             COUNT(*) AS total,
             SUM(status='PENDING') AS pending,
             SUM(status='APPROVED') AS approved,
             SUM(status='REJECTED') AS rejected,
             SUM(status='NEEDS_REVISION') AS needs_revision,
             SUM(deleted_at IS NOT NULL) AS deleted
           FROM projects"""
    )
    dept_count  = query_one("SELECT COUNT(*) AS cnt FROM departments WHERE is_active=1")
    tag_count   = query_one("SELECT COUNT(*) AS cnt FROM tags WHERE is_active=1")

    recent_projects = query_all(
        """SELECT p.project_id, p.title, p.status, p.submitted_at,
                  d.dept_name, ls.full_name AS lead_name
           FROM projects p
           JOIN departments d ON d.department_id=p.department_id
           JOIN users ls ON ls.user_id=p.lead_student_id
           WHERE p.deleted_at IS NULL
           ORDER BY p.submitted_at DESC
           LIMIT 8"""
    )

    return render_template(
        "admin/dashboard.html",
        user_stats=user_stats,
        project_stats=project_stats,
        dept_count=dept_count,
        tag_count=tag_count,
        recent_projects=recent_projects,
        status_badge_class=status_badge_class,
        status_display=status_display,
    )


# ─────────────────────────────────────────────────────────────
# User management
# ─────────────────────────────────────────────────────────────

@admin_bp.route("/users")
@_admin_required
def users():
    role_filter   = request.args.get("role", "")
    search        = (request.args.get("q") or "").strip()

    conditions = []
    params     = []

    if role_filter in ("STUDENT", "FACULTY", "ADMIN"):
        conditions.append("u.role=%s")
        params.append(role_filter)

    if search:
        conditions.append("(u.full_name LIKE %s OR u.email LIKE %s OR u.roll_or_emp_id LIKE %s)")
        params += [f"%{search}%", f"%{search}%", f"%{search}%"]

    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""

    users_list = query_all(
        f"""SELECT u.user_id, u.full_name, u.email, u.role, u.is_active,
                   u.roll_or_emp_id, u.created_at, u.last_login_at,
                   d.dept_name
            FROM users u
            LEFT JOIN departments d ON d.department_id=u.department_id
            {where}
            ORDER BY u.created_at DESC""",
        params
    )

    return render_template(
        "admin/users.html",
        users_list=users_list,
        role_filter=role_filter,
        search=search,
    )


@admin_bp.route("/users/<int:user_id>/toggle", methods=["POST"])
@_admin_required
def toggle_user(user_id: int):
    current_admin = session["user_id"]
    if user_id == current_admin:
        return jsonify({"success": False, "message": "You cannot deactivate your own account."}), 400

    user = query_one("SELECT user_id, is_active, full_name FROM users WHERE user_id=%s", (user_id,))
    if not user:
        return jsonify({"success": False, "message": "User not found."}), 404

    new_status = 0 if user["is_active"] else 1
    execute("UPDATE users SET is_active=%s WHERE user_id=%s", (new_status, user_id))

    action = "activated" if new_status else "deactivated"
    return jsonify({
        "success":    True,
        "message":    f"User {user['full_name']} has been {action}.",
        "is_active":  bool(new_status),
    })


# ─────────────────────────────────────────────────────────────
# Department management
# ─────────────────────────────────────────────────────────────

@admin_bp.route("/departments")
@_admin_required
def departments():
    depts = query_all(
        """SELECT d.*, COUNT(u.user_id) AS user_count
           FROM departments d
           LEFT JOIN users u ON u.department_id=d.department_id
           GROUP BY d.department_id
           ORDER BY d.dept_name"""
    )
    return render_template("admin/departments.html", depts=depts)


@admin_bp.route("/departments", methods=["POST"])
@_admin_required
def add_department():
    dept_code = (request.form.get("dept_code") or "").strip().upper()
    dept_name = (request.form.get("dept_name") or "").strip()

    if not dept_code or not dept_name:
        flash("Department code and name are required.", "danger")
        return redirect(url_for("admin.departments"))

    existing = query_one("SELECT department_id FROM departments WHERE dept_code=%s", (dept_code,))
    if existing:
        flash(f"A department with code '{dept_code}' already exists.", "danger")
        return redirect(url_for("admin.departments"))

    execute(
        "INSERT INTO departments (dept_code, dept_name) VALUES (%s, %s)",
        (dept_code, dept_name)
    )
    flash(f"Department '{dept_name}' added.", "success")
    return redirect(url_for("admin.departments"))


@admin_bp.route("/departments/<int:dept_id>/toggle", methods=["POST"])
@_admin_required
def toggle_department(dept_id: int):
    dept = query_one("SELECT * FROM departments WHERE department_id=%s", (dept_id,))
    if not dept:
        return jsonify({"success": False, "message": "Department not found."}), 404
    new_status = 0 if dept["is_active"] else 1
    execute("UPDATE departments SET is_active=%s WHERE department_id=%s", (new_status, dept_id))
    return jsonify({"success": True, "is_active": bool(new_status)})


# ─────────────────────────────────────────────────────────────
# Tag management
# ─────────────────────────────────────────────────────────────

@admin_bp.route("/tags")
@_admin_required
def tags():
    tags_list = query_all(
        """SELECT t.*, COUNT(pt.project_id) AS usage_count
           FROM tags t
           LEFT JOIN project_tags pt ON pt.tag_id=t.tag_id
           GROUP BY t.tag_id
           ORDER BY t.tag_name"""
    )
    return render_template("admin/tags.html", tags_list=tags_list)


@admin_bp.route("/tags", methods=["POST"])
@_admin_required
def add_tag():
    tag_name = (request.form.get("tag_name") or "").strip()
    if not tag_name or len(tag_name) > 50:
        flash("Tag name must be 1–50 characters.", "danger")
        return redirect(url_for("admin.tags"))

    existing = query_one("SELECT tag_id FROM tags WHERE tag_name=%s", (tag_name,))
    if existing:
        flash(f"Tag '{tag_name}' already exists.", "warning")
        return redirect(url_for("admin.tags"))

    execute("INSERT INTO tags (tag_name) VALUES (%s)", (tag_name,))
    flash(f"Tag '{tag_name}' added.", "success")
    return redirect(url_for("admin.tags"))


@admin_bp.route("/tags/<int:tag_id>/toggle", methods=["POST"])
@_admin_required
def toggle_tag(tag_id: int):
    tag = query_one("SELECT * FROM tags WHERE tag_id=%s", (tag_id,))
    if not tag:
        return jsonify({"success": False, "message": "Tag not found."}), 404
    new_status = 0 if tag["is_active"] else 1
    execute("UPDATE tags SET is_active=%s WHERE tag_id=%s", (new_status, tag_id))
    return jsonify({"success": True, "is_active": bool(new_status)})


# ─────────────────────────────────────────────────────────────
# Statistics
# ─────────────────────────────────────────────────────────────

@admin_bp.route("/statistics")
@_admin_required
def statistics():
    # Projects by department
    by_dept = query_all(
        """SELECT d.dept_name, COUNT(p.project_id) AS cnt
           FROM departments d
           LEFT JOIN projects p ON p.department_id=d.department_id AND p.deleted_at IS NULL
           GROUP BY d.department_id
           ORDER BY cnt DESC"""
    )

    # Projects by year
    by_year = query_all(
        """SELECT academic_year, COUNT(*) AS cnt
           FROM projects WHERE deleted_at IS NULL
           GROUP BY academic_year
           ORDER BY academic_year DESC"""
    )

    # Top tags
    top_tags = query_all(
        """SELECT t.tag_name, COUNT(pt.project_id) AS cnt
           FROM tags t
           JOIN project_tags pt ON pt.tag_id=t.tag_id
           JOIN projects p ON p.project_id=pt.project_id AND p.deleted_at IS NULL
           GROUP BY t.tag_id
           ORDER BY cnt DESC
           LIMIT 10"""
    )

    # Top viewed
    top_viewed = query_all(
        """SELECT p.project_id, p.title, p.views_count, p.downloads_count
           FROM projects p
           WHERE p.status='APPROVED' AND p.deleted_at IS NULL
           ORDER BY p.views_count DESC
           LIMIT 10"""
    )

    return render_template(
        "admin/statistics.html",
        by_dept=by_dept,
        by_year=by_year,
        top_tags=top_tags,
        top_viewed=top_viewed,
    )
