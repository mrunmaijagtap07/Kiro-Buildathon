-- ============================================================
-- CampusArchive Database Schema
-- Character Set: utf8mb4 | Engine: InnoDB
-- ============================================================
-- Changes from initial Schema_DDL.sql:
--   1. users: added google_id, auth_provider; made department_id
--      nullable so Google OAuth users can complete profile later.
--   2. users: password_hash is nullable for pure-OAuth accounts.
--   3. projects: added submitted_at (separate from created_at)
--      to properly track resubmission timestamps.
--   4. project_attachments: added uploader_id for audit trail.
--   5. tags: added created_at, is_active for admin management.
--   6. Added .gitkeep placeholder comments for upload dirs.
-- ============================================================

CREATE DATABASE IF NOT EXISTS campus_repository
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE campus_repository;

-- ─────────────────────────────────────────────────────────────
-- DEPARTMENTS
-- ─────────────────────────────────────────────────────────────
CREATE TABLE departments (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    dept_code     VARCHAR(10)  NOT NULL UNIQUE,
    dept_name     VARCHAR(100) NOT NULL,
    is_active     BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─────────────────────────────────────────────────────────────
-- USERS
-- password_hash is NULL for pure Google-OAuth accounts.
-- department_id is NULL until the user completes their profile.
-- ─────────────────────────────────────────────────────────────
CREATE TABLE users (
    user_id       INT AUTO_INCREMENT PRIMARY KEY,
    full_name     VARCHAR(100) NOT NULL,
    email         VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NULL     DEFAULT NULL,
    google_id     VARCHAR(120) NULL     DEFAULT NULL UNIQUE,
    auth_provider ENUM('LOCAL','GOOGLE','BOTH') NOT NULL DEFAULT 'LOCAL',
    role          ENUM('STUDENT','FACULTY','ADMIN') NOT NULL,
    department_id INT          NULL     DEFAULT NULL,
    roll_or_emp_id VARCHAR(50) NULL     DEFAULT NULL UNIQUE,
    is_active     BOOLEAN      NOT NULL DEFAULT TRUE,
    last_login_at TIMESTAMP    NULL     DEFAULT NULL,
    created_at    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_users_department
        FOREIGN KEY (department_id) REFERENCES departments(department_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,

    INDEX idx_users_role (role),
    INDEX idx_users_google_id (google_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─────────────────────────────────────────────────────────────
-- PROJECTS
-- submitted_at tracks the most recent submission/resubmission.
-- ─────────────────────────────────────────────────────────────
CREATE TABLE projects (
    project_id      INT AUTO_INCREMENT PRIMARY KEY,
    title           VARCHAR(255) NOT NULL,
    abstract        TEXT         NOT NULL,
    academic_year   INT          NOT NULL,
    department_id   INT          NOT NULL,
    lead_student_id INT          NOT NULL,
    guide_id        INT          NOT NULL,
    status          ENUM('PENDING','NEEDS_REVISION','APPROVED','REJECTED') NOT NULL DEFAULT 'PENDING',
    submitted_at    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    views_count     INT          NOT NULL DEFAULT 0,
    downloads_count INT          NOT NULL DEFAULT 0,
    created_at      TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at      TIMESTAMP    NULL     DEFAULT NULL,

    CONSTRAINT fk_projects_department
        FOREIGN KEY (department_id) REFERENCES departments(department_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_projects_lead_student
        FOREIGN KEY (lead_student_id) REFERENCES users(user_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_projects_guide
        FOREIGN KEY (guide_id) REFERENCES users(user_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,

    INDEX idx_projects_status (status),
    INDEX idx_projects_dept (department_id),
    INDEX idx_projects_guide (guide_id),
    INDEX idx_projects_year (academic_year),
    FULLTEXT INDEX idx_projects_fulltext (title, abstract)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─────────────────────────────────────────────────────────────
-- PROJECT AUTHORS  (many-to-many: projects ↔ students)
-- ─────────────────────────────────────────────────────────────
CREATE TABLE project_authors (
    project_id INT NOT NULL,
    student_id INT NOT NULL,
    PRIMARY KEY (project_id, student_id),
    CONSTRAINT fk_authors_project
        FOREIGN KEY (project_id) REFERENCES projects(project_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_authors_student
        FOREIGN KEY (student_id) REFERENCES users(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─────────────────────────────────────────────────────────────
-- PROJECT ATTACHMENTS
-- ─────────────────────────────────────────────────────────────
CREATE TABLE project_attachments (
    attachment_id    INT AUTO_INCREMENT PRIMARY KEY,
    project_id       INT          NOT NULL,
    file_type        ENUM('REPORT_PDF','SOURCE_ZIP','DIAGRAM') NOT NULL,
    original_name    VARCHAR(255) NOT NULL,
    stored_file_path VARCHAR(500) NOT NULL,
    file_size_bytes  BIGINT       NOT NULL,
    file_hash        VARCHAR(64)  NULL DEFAULT NULL,
    uploaded_at      TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_attachments_project
        FOREIGN KEY (project_id) REFERENCES projects(project_id)
        ON DELETE CASCADE ON UPDATE CASCADE,

    INDEX idx_attachments_project (project_id),
    INDEX idx_attachments_type (file_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─────────────────────────────────────────────────────────────
-- TAGS
-- ─────────────────────────────────────────────────────────────
CREATE TABLE tags (
    tag_id     INT AUTO_INCREMENT PRIMARY KEY,
    tag_name   VARCHAR(50) NOT NULL UNIQUE,
    is_active  BOOLEAN     NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─────────────────────────────────────────────────────────────
-- PROJECT TAGS  (many-to-many: projects ↔ tags)
-- ─────────────────────────────────────────────────────────────
CREATE TABLE project_tags (
    project_id INT NOT NULL,
    tag_id     INT NOT NULL,
    PRIMARY KEY (project_id, tag_id),
    CONSTRAINT fk_ptags_project
        FOREIGN KEY (project_id) REFERENCES projects(project_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_ptags_tag
        FOREIGN KEY (tag_id) REFERENCES tags(tag_id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ─────────────────────────────────────────────────────────────
-- FACULTY REVIEWS
-- Stores every review action; multiple rows per project are
-- normal (revision → resubmit → approve etc.)
-- ─────────────────────────────────────────────────────────────
CREATE TABLE faculty_reviews (
    review_id   INT AUTO_INCREMENT PRIMARY KEY,
    project_id  INT          NOT NULL,
    faculty_id  INT          NOT NULL,
    decision    ENUM('APPROVED','REJECTED','REVISION_REQUESTED') NOT NULL,
    comments    TEXT         NULL,
    reviewed_at TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_reviews_project
        FOREIGN KEY (project_id) REFERENCES projects(project_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_reviews_faculty
        FOREIGN KEY (faculty_id) REFERENCES users(user_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,

    INDEX idx_reviews_project (project_id),
    INDEX idx_reviews_faculty (faculty_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
