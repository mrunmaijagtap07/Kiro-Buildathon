"""
routes/student.py — Student dashboard, project submission, and revision.
"""

from flask import (
    Blueprint, render_template, request, redirect, url_for,
    flash, session, abort, current_app, jsonify
)

from utils.database import query_one, query_all, execute, transaction
from utils.decorators import login_required, role_required
from utils.file_handler import save_upload, delete_upload, FileValidationError, human_readable_size
from utils.validators import validate_project_submission
from utils.helpers import academic_year_choices, status_badge_class, status_display

student_bp = Blueprint("student", __name__, url_prefix="/student")


def _student_required(f):
    return login_required(role_required("STUDENT")(f))


# ─────────────────────────────────────────────────────────────
# Dashboard
# ─────────────────────────────────────────────────────────────

@student_bp.route("/dashboard")
@_student_required
def dashboard():
    user_id = session["user_id"]

    stats = query_one(
        """SELECT
             COUNT(*) AS total,
             SUM(status='PENDING') AS pending,
             SUM(status='APPROVED') AS approved,
             SUM(status='NEEDS_REVISION') AS needs_revision,
             SUM(status='REJECTED') AS rejected
           FROM projects
           WHERE lead_student_id=%s AND deleted_at IS NULL""",
        (user_id,)
    )

    recent_projects = query_all(
        """SELECT p.project_id, p.title, p.status, p.submitted_at, p.academic_year,
                  d.dept_name
           FROM projects p
           JOIN departments d ON d.department_id=p.department_id
           WHERE p.lead_student_id=%s AND p.deleted_at IS NULL
           ORDER BY p.submitted_at DESC
           LIMIT 5""",
        (user_id,)
    )

    # Also check if this student is a co-author on other projects
    coauthor_projects = query_all(
        """SELECT p.project_id, p.title, p.status, p.submitted_at,
                  d.dept_name, ls.full_name AS lead_name
           FROM project_authors pa
           JOIN projects p ON p.project_id=pa.project_id
           JOIN departments d ON d.department_id=p.department_id
           JOIN users ls ON ls.user_id=p.lead_student_id
           WHERE pa.student_id=%s AND p.lead_student_id != %s AND p.deleted_at IS NULL
           ORDER BY p.submitted_at DESC
           LIMIT 5""",
        (user_id, user_id)
    )

    return render_template(
        "student/dashboard.html",
        stats=stats,
        recent_projects=recent_projects,
        coauthor_projects=coauthor_projects,
        status_badge_class=status_badge_class,
        status_display=status_display,
    )


# ─────────────────────────────────────────────────────────────
# My Submissions list
# ─────────────────────────────────────────────────────────────

@student_bp.route("/projects")
@_student_required
def my_projects():
    user_id = session["user_id"]

    projects = query_all(
        """SELECT p.project_id, p.title, p.status, p.submitted_at, p.academic_year,
                  d.dept_name, u.full_name AS guide_name
           FROM projects p
           JOIN departments d ON d.department_id=p.department_id
           JOIN users u ON u.user_id=p.guide_id
           WHERE p.lead_student_id=%s AND p.deleted_at IS NULL
           ORDER BY p.submitted_at DESC""",
        (user_id,)
    )

    for proj in projects:
        proj["tags"] = query_all(
            "SELECT t.tag_name FROM tags t JOIN project_tags pt ON pt.tag_id=t.tag_id WHERE pt.project_id=%s",
            (proj["project_id"],)
        )

    return render_template(
        "student/my_projects.html",
        projects=projects,
        status_badge_class=status_badge_class,
        status_display=status_display,
    )


# ─────────────────────────────────────────────────────────────
# Submit project (create)
# ─────────────────────────────────────────────────────────────

@student_bp.route("/projects/create", methods=["GET", "POST"])
@_student_required
def create_project():
    user_id = session["user_id"]
    departments = query_all(
        "SELECT department_id, dept_name FROM departments WHERE is_active=1 ORDER BY dept_name"
    )
    faculty_list = query_all(
        "SELECT user_id, full_name, department_id FROM users WHERE role='FACULTY' AND is_active=1 ORDER BY full_name"
    )
    tags_list = query_all(
        "SELECT tag_id, tag_name FROM tags WHERE is_active=1 ORDER BY tag_name"
    )

    if request.method == "POST":
        data = request.form.to_dict()
        errors = validate_project_submission(data)

        # Team members: comma-separated student emails
        team_emails_raw = request.form.getlist("team_members")
        team_members = []
        seen_ids = {user_id}  # prevent self-duplication

        for email in team_emails_raw:
            email = email.strip().lower()
            if not email:
                continue
            member = query_one(
                "SELECT user_id, full_name FROM users WHERE email=%s AND role='STUDENT' AND is_active=1",
                (email,)
            )
            if not member:
                errors.append(f"Student not found or not active: {email}")
                continue
            if member["user_id"] in seen_ids:
                continue
            seen_ids.add(member["user_id"])
            team_members.append(member)

        # File validation
        report_file   = request.files.get("report_pdf")
        source_file   = request.files.get("source_zip")
        diagram_file  = request.files.get("diagram")

        if not report_file or not report_file.filename:
            errors.append("Project report PDF is required.")
        if not source_file or not source_file.filename:
            errors.append("Source code ZIP is required.")

        selected_tags = request.form.getlist("tags")

        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template(
                "student/submit_project.html",
                departments=departments,
                faculty_list=faculty_list,
                tags_list=tags_list,
                years=academic_year_choices(),
                form=data,
            )

        # Save files
        saved_files = {}
        file_errors = []

        if report_file and report_file.filename:
            try:
                saved_files["REPORT_PDF"] = save_upload(report_file, "REPORT_PDF")
            except FileValidationError as e:
                file_errors.append(str(e))

        if source_file and source_file.filename:
            try:
                saved_files["SOURCE_ZIP"] = save_upload(source_file, "SOURCE_ZIP")
            except FileValidationError as e:
                file_errors.append(str(e))

        if diagram_file and diagram_file.filename:
            try:
                saved_files["DIAGRAM"] = save_upload(diagram_file, "DIAGRAM")
            except FileValidationError as e:
                file_errors.append(str(e))

        if file_errors:
            # Clean up any files already saved
            for info in saved_files.values():
                delete_upload(info["stored_file_path"])
            for e in file_errors:
                flash(e, "danger")
            return render_template(
                "student/submit_project.html",
                departments=departments,
                faculty_list=faculty_list,
                tags_list=tags_list,
                years=academic_year_choices(),
                form=data,
            )

        # Database transaction
        try:
            with transaction() as cursor:
                cursor.execute(
                    """INSERT INTO projects
                       (title, abstract, academic_year, department_id,
                        lead_student_id, guide_id, status)
                       VALUES (%s, %s, %s, %s, %s, %s, 'PENDING')""",
                    (
                        data["title"].strip(),
                        data["abstract"].strip(),
                        int(data["academic_year"]),
                        int(data["department_id"]),
                        user_id,
                        int(data["guide_id"]),
                    )
                )
                project_id = cursor.lastrowid

                # Lead student is always an author
                cursor.execute(
                    "INSERT INTO project_authors (project_id, student_id) VALUES (%s, %s)",
                    (project_id, user_id)
                )

                # Co-authors
                for member in team_members:
                    cursor.execute(
                        "INSERT IGNORE INTO project_authors (project_id, student_id) VALUES (%s, %s)",
                        (project_id, member["user_id"])
                    )

                # Attachments
                for file_type, info in saved_files.items():
                    cursor.execute(
                        """INSERT INTO project_attachments
                           (project_id, file_type, original_name, stored_file_path, file_size_bytes, file_hash)
                           VALUES (%s, %s, %s, %s, %s, %s)""",
                        (
                            project_id,
                            file_type,
                            info["original_name"],
                            info["stored_file_path"],
                            info["file_size_bytes"],
                            info["file_hash"],
                        )
                    )

                # Tags
                for tag_id in selected_tags:
                    cursor.execute(
                        "INSERT IGNORE INTO project_tags (project_id, tag_id) VALUES (%s, %s)",
                        (project_id, int(tag_id))
                    )

        except Exception as e:
            # Rollback happened in context manager; clean up files
            for info in saved_files.values():
                delete_upload(info["stored_file_path"])
            current_app.logger.error(f"Project submission DB error: {e}")
            flash("An error occurred while saving your project. Please try again.", "danger")
            return render_template(
                "student/submit_project.html",
                departments=departments,
                faculty_list=faculty_list,
                tags_list=tags_list,
                years=academic_year_choices(),
                form=data,
            )

        flash("Project submitted successfully! It is now pending faculty review.", "success")
        return redirect(url_for("student.project_detail", project_id=project_id))

    return render_template(
        "student/submit_project.html",
        departments=departments,
        faculty_list=faculty_list,
        tags_list=tags_list,
        years=academic_year_choices(),
        form={},
    )


# ─────────────────────────────────────────────────────────────
# Student project detail (own project)
# ─────────────────────────────────────────────────────────────

@student_bp.route("/projects/<int:project_id>")
@_student_required
def project_detail(project_id: int):
    user_id = session["user_id"]

    project = query_one(
        """SELECT p.*, d.dept_name,
                  g.full_name AS guide_name,
                  g.email AS guide_email
           FROM projects p
           JOIN departments d ON d.department_id=p.department_id
           JOIN users g ON g.user_id=p.guide_id
           WHERE p.project_id=%s AND p.deleted_at IS NULL""",
        (project_id,)
    )

    if not project:
        abort(404)

    # Authorization: only lead, co-author, or admin
    is_lead = project["lead_student_id"] == user_id
    is_coauthor = query_one(
        "SELECT 1 FROM project_authors WHERE project_id=%s AND student_id=%s",
        (project_id, user_id)
    )
    if not (is_lead or is_coauthor):
        abort(403)

    authors = query_all(
        """SELECT u.full_name, u.roll_or_emp_id, u.email
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
        "SELECT * FROM project_attachments WHERE project_id=%s ORDER BY uploaded_at",
        (project_id,)
    )
    reviews = query_all(
        """SELECT fr.*, u.full_name AS faculty_name
           FROM faculty_reviews fr
           JOIN users u ON u.user_id=fr.faculty_id
           WHERE fr.project_id=%s
           ORDER BY fr.reviewed_at DESC""",
        (project_id,)
    )

    return render_template(
        "student/project_detail.html",
        project=project,
        is_lead=is_lead,
        authors=authors,
        tags=tags,
        attachments=attachments,
        reviews=reviews,
        status_badge_class=status_badge_class,
        status_display=status_display,
        human_readable_size=human_readable_size,
    )


# ─────────────────────────────────────────────────────────────
# Resubmit (for NEEDS_REVISION projects)
# ─────────────────────────────────────────────────────────────

@student_bp.route("/projects/<int:project_id>/resubmit", methods=["GET", "POST"])
@_student_required
def resubmit(project_id: int):
    user_id = session["user_id"]

    project = query_one(
        "SELECT * FROM projects WHERE project_id=%s AND lead_student_id=%s AND deleted_at IS NULL",
        (project_id, user_id)
    )
    if not project:
        abort(404)
    if project["status"] != "NEEDS_REVISION":
        flash("This project cannot be resubmitted in its current status.", "warning")
        return redirect(url_for("student.project_detail", project_id=project_id))

    departments = query_all(
        "SELECT department_id, dept_name FROM departments WHERE is_active=1 ORDER BY dept_name"
    )
    faculty_list = query_all(
        "SELECT user_id, full_name FROM users WHERE role='FACULTY' AND is_active=1 ORDER BY full_name"
    )
    tags_list = query_all(
        "SELECT tag_id, tag_name FROM tags WHERE is_active=1 ORDER BY tag_name"
    )
    current_tags = [t["tag_name"] for t in query_all(
        "SELECT t.tag_name FROM tags t JOIN project_tags pt ON pt.tag_id=t.tag_id WHERE pt.project_id=%s",
        (project_id,)
    )]
    current_attachments = query_all(
        "SELECT * FROM project_attachments WHERE project_id=%s ORDER BY file_type",
        (project_id,)
    )

    if request.method == "POST":
        data = request.form.to_dict()
        errors = []

        abstract = (data.get("abstract") or "").strip()
        if abstract and len(abstract) >= 50:
            pass
        elif abstract:
            errors.append("Abstract must be at least 50 characters.")

        new_files = {}
        for field, file_type in [("report_pdf", "REPORT_PDF"), ("source_zip", "SOURCE_ZIP"), ("diagram", "DIAGRAM")]:
            f = request.files.get(field)
            if f and f.filename:
                try:
                    new_files[file_type] = save_upload(f, file_type)
                except FileValidationError as e:
                    errors.append(str(e))

        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template(
                "student/resubmit.html",
                project=project, departments=departments,
                faculty_list=faculty_list, tags_list=tags_list,
                current_tags=current_tags, current_attachments=current_attachments,
                years=academic_year_choices(),
            )

        try:
            with transaction() as cursor:
                # Update project fields
                updates = []
                vals = []
                if abstract:
                    updates.append("abstract=%s"); vals.append(abstract)
                if data.get("guide_id"):
                    updates.append("guide_id=%s"); vals.append(int(data["guide_id"]))
                updates += ["status='PENDING'", "submitted_at=NOW()"]
                vals.append(project_id)

                cursor.execute(
                    f"UPDATE projects SET {', '.join(updates)} WHERE project_id=%s",
                    vals
                )

                # Replace tags if new ones submitted
                new_tags = request.form.getlist("tags")
                if new_tags:
                    cursor.execute("DELETE FROM project_tags WHERE project_id=%s", (project_id,))
                    for tag_id in new_tags:
                        cursor.execute(
                            "INSERT IGNORE INTO project_tags (project_id, tag_id) VALUES (%s, %s)",
                            (project_id, int(tag_id))
                        )

                # New file attachments
                for file_type, info in new_files.items():
                    # Remove old attachment of same type
                    old = query_one(
                        "SELECT stored_file_path FROM project_attachments WHERE project_id=%s AND file_type=%s",
                        (project_id, file_type)
                    )
                    if old:
                        cursor.execute(
                            "DELETE FROM project_attachments WHERE project_id=%s AND file_type=%s",
                            (project_id, file_type)
                        )
                        delete_upload(old["stored_file_path"])
                    cursor.execute(
                        """INSERT INTO project_attachments
                           (project_id, file_type, original_name, stored_file_path, file_size_bytes, file_hash)
                           VALUES (%s, %s, %s, %s, %s, %s)""",
                        (project_id, file_type, info["original_name"],
                         info["stored_file_path"], info["file_size_bytes"], info["file_hash"])
                    )

        except Exception as e:
            for info in new_files.values():
                delete_upload(info["stored_file_path"])
            current_app.logger.error(f"Resubmit error: {e}")
            flash("An error occurred. Please try again.", "danger")
            return redirect(url_for("student.resubmit", project_id=project_id))

        flash("Project resubmitted for review.", "success")
        return redirect(url_for("student.project_detail", project_id=project_id))

    return render_template(
        "student/resubmit.html",
        project=project, departments=departments,
        faculty_list=faculty_list, tags_list=tags_list,
        current_tags=current_tags, current_attachments=current_attachments,
        years=academic_year_choices(),
    )


# ─────────────────────────────────────────────────────────────
# Student search for team member emails (AJAX)
# ─────────────────────────────────────────────────────────────

@student_bp.route("/api/students/search")
@login_required
def search_students():
    q = (request.args.get("q") or "").strip()
    if len(q) < 2:
        return jsonify({"success": True, "data": []})

    user_id = session["user_id"]
    results = query_all(
        """SELECT user_id, full_name, email, roll_or_emp_id
           FROM users
           WHERE role='STUDENT' AND is_active=1
             AND user_id != %s
             AND (full_name LIKE %s OR email LIKE %s OR roll_or_emp_id LIKE %s)
           LIMIT 8""",
        (user_id, f"%{q}%", f"%{q}%", f"%{q}%")
    )
    return jsonify({"success": True, "data": results})
