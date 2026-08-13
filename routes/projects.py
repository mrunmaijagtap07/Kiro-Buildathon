"""
routes/projects.py — Public project browsing, search, and detail pages.
Only APPROVED projects are publicly visible.
"""

from flask import (
    Blueprint, render_template, request, abort, send_file,
    session, jsonify, current_app
)

from utils.database import query_one, query_all, execute
from utils.decorators import login_required
from utils.file_handler import get_absolute_path
from utils.helpers import status_badge_class, status_display

projects_bp = Blueprint("projects", __name__)


# ─────────────────────────────────────────────────────────────
# Browse approved projects
# ─────────────────────────────────────────────────────────────

@projects_bp.route("/browse")
def browse():
    page     = max(1, int(request.args.get("page", 1)))
    per_page = 12
    offset   = (page - 1) * per_page

    search     = (request.args.get("q") or "").strip()
    dept_id    = request.args.get("dept", "")
    year       = request.args.get("year", "")
    guide_id   = request.args.get("guide", "")
    tag_id     = request.args.get("tag", "")

    # Build dynamic WHERE clause
    conditions = ["p.status='APPROVED'", "p.deleted_at IS NULL"]
    params     = []

    if search:
        conditions.append(
            "(MATCH(p.title, p.abstract) AGAINST(%s IN BOOLEAN MODE) "
            "OR p.title LIKE %s)"
        )
        params += [f"{search}*", f"%{search}%"]

    if dept_id:
        conditions.append("p.department_id=%s")
        params.append(int(dept_id))

    if year:
        conditions.append("p.academic_year=%s")
        params.append(int(year))

    if guide_id:
        conditions.append("p.guide_id=%s")
        params.append(int(guide_id))

    if tag_id:
        conditions.append(
            "EXISTS(SELECT 1 FROM project_tags pt WHERE pt.project_id=p.project_id AND pt.tag_id=%s)"
        )
        params.append(int(tag_id))

    where = " AND ".join(conditions)

    # Count total
    count_row = query_one(
        f"SELECT COUNT(*) AS cnt FROM projects p WHERE {where}",
        params
    )
    total = count_row["cnt"] if count_row else 0
    pages = max(1, (total + per_page - 1) // per_page)

    # Fetch page
    projects_rows = query_all(
        f"""SELECT p.project_id, p.title, p.abstract, p.academic_year,
                   p.views_count, p.downloads_count,
                   d.dept_name,
                   u.full_name AS guide_name,
                   ls.full_name AS lead_name
            FROM projects p
            JOIN departments d ON d.department_id = p.department_id
            JOIN users u ON u.user_id = p.guide_id
            JOIN users ls ON ls.user_id = p.lead_student_id
            WHERE {where}
            ORDER BY p.submitted_at DESC
            LIMIT %s OFFSET %s""",
        params + [per_page, offset]
    )

    # Attach tags to each project
    for proj in projects_rows:
        proj["tags"] = query_all(
            """SELECT t.tag_name FROM tags t
               JOIN project_tags pt ON pt.tag_id=t.tag_id
               WHERE pt.project_id=%s""",
            (proj["project_id"],)
        )

    # Filter dropdowns
    departments = query_all(
        "SELECT department_id, dept_name FROM departments WHERE is_active=1 ORDER BY dept_name"
    )
    faculty_list = query_all(
        "SELECT user_id, full_name FROM users WHERE role='FACULTY' AND is_active=1 ORDER BY full_name"
    )
    tags_list = query_all(
        "SELECT tag_id, tag_name FROM tags WHERE is_active=1 ORDER BY tag_name"
    )
    years = query_all(
        "SELECT DISTINCT academic_year FROM projects WHERE status='APPROVED' ORDER BY academic_year DESC"
    )

    return render_template(
        "projects/browse.html",
        projects=projects_rows,
        departments=departments,
        faculty_list=faculty_list,
        tags_list=tags_list,
        years=years,
        total=total,
        page=page,
        pages=pages,
        per_page=per_page,
        search=search,
        selected_dept=dept_id,
        selected_year=year,
        selected_guide=guide_id,
        selected_tag=tag_id,
    )


# ─────────────────────────────────────────────────────────────
# Project detail page
# ─────────────────────────────────────────────────────────────

@projects_bp.route("/project/<int:project_id>")
def detail(project_id: int):
    project = query_one(
        """SELECT p.*, d.dept_name,
                  u.full_name AS guide_name, u.email AS guide_email,
                  ls.full_name AS lead_name
           FROM projects p
           JOIN departments d ON d.department_id=p.department_id
           JOIN users u ON u.user_id=p.guide_id
           JOIN users ls ON ls.user_id=p.lead_student_id
           WHERE p.project_id=%s AND p.deleted_at IS NULL""",
        (project_id,)
    )

    if not project:
        abort(404)

    # Non-approved projects are only visible to their authors, guide, or admin
    user_id = session.get("user_id")
    role    = session.get("role")

    if project["status"] != "APPROVED":
        if not user_id:
            abort(404)
        is_author = query_one(
            "SELECT 1 FROM project_authors WHERE project_id=%s AND student_id=%s",
            (project_id, user_id)
        )
        is_lead = project["lead_student_id"] == user_id
        is_guide = project["guide_id"] == user_id
        is_admin = (role == "ADMIN")
        if not (is_author or is_lead or is_guide or is_admin):
            abort(403)

    # Increment view count (only for approved, publicly viewed)
    if project["status"] == "APPROVED":
        execute(
            "UPDATE projects SET views_count=views_count+1 WHERE project_id=%s",
            (project_id,)
        )

    # Authors
    authors = query_all(
        """SELECT u.full_name, u.roll_or_emp_id
           FROM project_authors pa
           JOIN users u ON u.user_id=pa.student_id
           WHERE pa.project_id=%s""",
        (project_id,)
    )

    # Tags
    tags = query_all(
        """SELECT t.tag_name FROM tags t
           JOIN project_tags pt ON pt.tag_id=t.tag_id
           WHERE pt.project_id=%s ORDER BY t.tag_name""",
        (project_id,)
    )

    # Attachments
    attachments = query_all(
        """SELECT attachment_id, file_type, original_name, file_size_bytes
           FROM project_attachments WHERE project_id=%s""",
        (project_id,)
    )

    # Latest faculty review (for students to see feedback)
    latest_review = query_one(
        """SELECT fr.decision, fr.comments, fr.reviewed_at, u.full_name AS faculty_name
           FROM faculty_reviews fr
           JOIN users u ON u.user_id=fr.faculty_id
           WHERE fr.project_id=%s
           ORDER BY fr.reviewed_at DESC LIMIT 1""",
        (project_id,)
    )

    return render_template(
        "projects/detail.html",
        project=project,
        authors=authors,
        tags=tags,
        attachments=attachments,
        latest_review=latest_review,
        status_badge_class=status_badge_class,
        status_display=status_display,
    )


# ─────────────────────────────────────────────────────────────
# File download
# ─────────────────────────────────────────────────────────────

@projects_bp.route("/project/<int:project_id>/download/<int:attachment_id>")
def download(project_id: int, attachment_id: int):
    attachment = query_one(
        """SELECT a.*, p.status, p.lead_student_id, p.guide_id
           FROM project_attachments a
           JOIN projects p ON p.project_id=a.project_id
           WHERE a.attachment_id=%s AND a.project_id=%s""",
        (attachment_id, project_id)
    )

    if not attachment:
        abort(404)

    user_id = session.get("user_id")
    role    = session.get("role")

    # Access control:
    # SOURCE_ZIP: only authors, guide, admin can download
    # REPORT_PDF / DIAGRAM: anyone can download approved project files
    if attachment["file_type"] == "SOURCE_ZIP":
        if not user_id:
            abort(403)
        is_author = query_one(
            "SELECT 1 FROM project_authors WHERE project_id=%s AND student_id=%s",
            (project_id, user_id)
        )
        is_lead   = attachment["lead_student_id"] == user_id
        is_guide  = attachment["guide_id"] == user_id
        is_admin  = (role == "ADMIN")
        is_faculty= (role == "FACULTY")
        if not (is_author or is_lead or is_guide or is_admin or is_faculty):
            abort(403)
    else:
        # Public files — must be from an approved project
        if attachment["status"] != "APPROVED":
            if not user_id:
                abort(403)

    # Resolve safe path
    try:
        abs_path = get_absolute_path(attachment["stored_file_path"])
    except ValueError:
        abort(400)

    if not abs_path.exists():
        abort(404)

    # Increment download count
    execute(
        "UPDATE projects SET downloads_count=downloads_count+1 WHERE project_id=%s",
        (project_id,)
    )

    return send_file(
        abs_path,
        as_attachment=True,
        download_name=attachment["original_name"],
    )


# ─────────────────────────────────────────────────────────────
# Search API (JSON, used by JS for live search suggestions)
# ─────────────────────────────────────────────────────────────

@projects_bp.route("/api/projects/search")
def api_search():
    q = (request.args.get("q") or "").strip()
    if len(q) < 2:
        return jsonify({"success": True, "data": []})

    results = query_all(
        """SELECT p.project_id, p.title, d.dept_name, p.academic_year
           FROM projects p
           JOIN departments d ON d.department_id=p.department_id
           WHERE p.status='APPROVED' AND p.deleted_at IS NULL
             AND (MATCH(p.title,p.abstract) AGAINST(%s IN BOOLEAN MODE)
                  OR p.title LIKE %s)
           ORDER BY p.submitted_at DESC
           LIMIT 8""",
        (f"{q}*", f"%{q}%")
    )
    return jsonify({"success": True, "data": results})
