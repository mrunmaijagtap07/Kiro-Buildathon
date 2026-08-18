# CampusArchive

**Institutional Student Project Repository for Academic Excellence**

Built for the Kiro Buildathon | August 2026

---

## Project Overview

CampusArchive is a centralized web application designed to solve the critical problem of lost student innovation in academic institutions. Every semester, students create exceptional capstone projects, research work, IoT prototypes, and software applications. However, once the semester ends, these projects typically disappear — scattered across personal drives, forgotten in email attachments, or simply lost to time.

CampusArchive provides a permanent institutional home for student work, connecting three key stakeholders: students who want their work preserved and discoverable, faculty who need to review and approve submissions, and institutions seeking to build a searchable archive of academic innovation.

## Problem Statement

### The Challenge

Educational institutions face several interconnected problems with student project management:

**For Students:**
- No centralized location to showcase completed work
- Projects disappear after graduation
- Difficult to discover what previous students have built
- Risk of duplicating existing work
- No permanent record for future reference or portfolio building

**For Faculty:**
- Manual, scattered review processes
- No standard workflow for project approval
- Difficult to track submission status
- Limited visibility into departmental project trends
- No systematic way to provide feedback

**For Institutions:**
- Lost institutional knowledge each semester
- No searchable archive of student innovation
- Inability to showcase student work to prospective students
- Missed opportunities to identify research trends
- Administrative overhead in managing projects

## Solution

CampusArchive addresses these problems through an integrated submission-review-discovery workflow:

### Centralized Repository
A single platform where all approved student projects are permanently archived, searchable, and accessible to the campus community.

### Structured Workflow
Students submit projects → Faculty review with feedback → Approved projects enter the public archive.

### Role-Based System
- **Students** submit projects with metadata, team information, and file uploads
- **Faculty** review assigned projects, provide feedback, and make approval decisions
- **Admins** manage users, departments, technology tags, and platform settings
- **Public visitors** browse and search approved projects without authentication

### Smart Discovery
Full-text search, department filtering, technology tag filtering, and academic year filtering enable users to find relevant projects quickly.

## Key Features

### Student Features

✅ **User Registration & Authentication**
- Email/password registration with secure hashing (Werkzeug)
- Google OAuth 2.0 integration for institutional accounts
- Profile completion for OAuth users

✅ **Project Submission**
- Comprehensive project metadata form (title, abstract, academic year, department)
- Team member management (multiple authors per project)
- Faculty guide assignment
- Technology tag selection

✅ **File Uploads**
- Project report PDF upload (validated for type and size)
- Source code ZIP upload (validated for type and size)
- Optional diagram/architecture image upload
- Secure file storage with hash verification

✅ **Submission Tracking**
- Student dashboard showing all submitted projects
- Real-time status indicators (Pending/Approved/Rejected/Needs Revision)
- View faculty feedback and review comments
- Track submission history and resubmissions

✅ **Project Resubmission**
- Ability to revise and resubmit projects marked "Needs Revision"
- Update project details, files, and metadata
- Review previous feedback before resubmitting

✅ **Archive Browsing**
- Browse all approved projects
- Search by keywords (title and abstract full-text search)
- Filter by department, technology tags, and academic year
- View project details and download files

### Faculty Features

✅ **Faculty Dashboard**
- Overview of projects assigned for review
- Status breakdown of pending/reviewed projects
- Recent activity feed

✅ **Review Queue**
- List of all projects assigned to the faculty member
- Filter by status (pending, approved, rejected, needs revision)
- Sort by submission date

✅ **Project Review Workflow**
- View complete project details, team information, and abstract
- Download project report PDF and source code ZIP
- Read previous review history (for resubmissions)
- Make approval decision: Approve / Reject / Request Revision
- Provide detailed written feedback to students
- Review timestamps and audit trail

✅ **Review History**
- Track all reviews completed
- View previous decisions and feedback provided

### Admin Features

✅ **Admin Dashboard**
- Platform-wide statistics
- Total users, projects, departments, and tags
- Status distribution (pending, approved, rejected)
- Recent platform activity

✅ **User Management**
- View all users (students, faculty, admins)
- Filter by role and department
- Activate/deactivate user accounts
- View user registration details

✅ **Department Management**
- Add new academic departments
- Edit department names and codes
- Activate/deactivate departments
- View project count per department

✅ **Technology Tag Management**
- Add new technology tags (Python, Flask, React, etc.)
- Edit existing tags
- Activate/deactivate tags
- View project count per tag

✅ **Platform Statistics**
- Total approved projects
- Projects per department
- Most-used technologies
- Faculty review metrics

### Public Features

✅ **Public Homepage**
- Welcome hero section
- Platform statistics (projects, departments, technologies, faculty)
- Recently approved projects showcase
- Search functionality

✅ **Project Browse & Search**
- Browse all approved projects without authentication
- Full-text keyword search
- Department filtering
- Technology tag filtering
- Academic year filtering
- Pagination for large result sets

✅ **Project Detail View**
- Complete project information
- Team member details
- Faculty guide information
- Technology tags
- Download project report and source code
- View/download counter tracking

✅ **About Page**
- Platform mission and purpose
- Feature overview
- Technology stack information

### System Features

✅ **Security**
- Werkzeug password hashing (pbkdf2:sha256)
- Parameterized SQL queries (SQL injection prevention)
- Path traversal protection for file operations
- File type and size validation
- Session management with secure cookies
- Role-based access control (@role_required decorators)

✅ **Theming**
- Light mode (warm ivory backgrounds, forest green primary, gold accents)
- Dark mode (deep forest green surfaces, ivory text, gold accents)
- Theme persistence via localStorage
- Accessible contrast ratios

✅ **Responsive Design**
- Mobile-first CSS design
- Tablet and desktop breakpoints
- Touch-friendly navigation
- Adaptive layouts

✅ **Error Handling**
- Custom error pages (400, 403, 404, 413, 500)
- Flash messages for user feedback
- Toast notifications
- Form validation feedback

## User Roles

### Student
**Access:** Student dashboard, project submission, resubmission, browse public archive

**Capabilities:**
- Register and log in (email/password or Google OAuth)
- Submit new projects with files
- View submission status and faculty feedback
- Resubmit projects marked for revision
- Browse approved projects
- Search and filter archive

**Restrictions:**
- Cannot access faculty review queue
- Cannot access admin management functions
- Cannot view other students' pending/rejected projects

### Faculty
**Access:** Faculty dashboard, review queue, browse public archive

**Capabilities:**
- Log in (email/password or Google OAuth)
- View projects assigned for review
- Download project files
- Approve, reject, or request revisions
- Provide written feedback to students
- Browse approved projects

**Restrictions:**
- Cannot submit projects
- Cannot access admin management functions
- Can only review projects where they are assigned as guide

### Admin
**Access:** Admin dashboard, all management functions, full platform access

**Capabilities:**
- Manage users (activate/deactivate)
- Manage departments (add, edit, activate/deactivate)
- Manage technology tags (add, edit, activate/deactivate)
- View platform-wide statistics
- Browse all projects (including pending/rejected)
- All faculty and student capabilities

**Restrictions:**
- None (highest privilege level)

### Public Visitor
**Access:** Homepage, browse approved projects, about page

**Capabilities:**
- Browse approved projects
- Search and filter projects
- View project details
- Download project files

**Restrictions:**
- Cannot submit projects
- Cannot view pending/rejected projects
- Cannot access dashboards
- No write operations

## Technology Stack

### Backend
- **Python 3.13** — Core programming language
- **Flask 3.0.3** — Web framework
- **PyMySQL 1.1.1** — MySQL database driver
- **Werkzeug 3.0.3** — WSGI utility library (password hashing, security utilities)
- **python-dotenv 1.0.1** — Environment variable management
- **Requests 2.32.3** — HTTP library for OAuth
- **cryptography 42.0.8** — Cryptographic recipes and primitives
- **itsdangerous 2.2.0** — Secure token generation

### Frontend
- **HTML5** — Semantic markup
- **CSS3** — Modern styling with CSS custom properties (variables)
- **Vanilla JavaScript (ES6+)** — Client-side interactivity
  - Theme toggle and persistence
  - Toast notifications
  - Form enhancements
  - Modal dialogs

### Database
- **MySQL 8.0** — Relational database
- **utf8mb4** character set — Full Unicode support
- **InnoDB** engine — ACID compliance, foreign keys, transactions

### Authentication
- **Email/Password** — Werkzeug password hashing (pbkdf2:sha256)
- **Google OAuth 2.0** — Institutional account integration

### Architecture Pattern
- **MVC Pattern** — Model (database utilities), View (Jinja2 templates), Controller (Flask routes)
- **Blueprint Architecture** — Modular route organization (auth, student, faculty, admin, projects)
- **Template Inheritance** — Base templates for consistent layouts

## Project Structure

```
CampusArchive/
│
├── app.py                          # Flask application entry point
├── config.py                       # Configuration management (loads .env)
├── init_db.py                      # Database initialization script
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (secret)
├── .env.example                    # Environment variable template
│
├── database/
│   ├── schema.sql                  # Complete database schema
│   ├── seed.sql                    # Initial departments and tags
│   └── migrations/                 # Schema migration directory
│
├── routes/                         # Flask blueprints
│   ├── auth.py                     # Authentication routes
│   ├── student.py                  # Student dashboard and submission
│   ├── faculty.py                  # Faculty review workflow
│   ├── admin.py                    # Admin management
│   └── projects.py                 # Public project browsing
│
├── templates/                      # Jinja2 HTML templates
│   ├── base.html                   # Authenticated layout (sidebar)
│   ├── public_base.html            # Public layout (navbar)
│   ├── auth_base.html              # Auth pages layout
│   ├── home.html                   # Landing page
│   ├── about.html                  # About page
│   ├── auth/                       # Login, register, OAuth
│   ├── student/                    # Student dashboard and submission
│   ├── faculty/                    # Faculty review pages
│   ├── admin/                      # Admin management pages
│   ├── projects/                   # Browse, search, detail
│   └── errors/                     # Error pages (400, 403, 404, 413, 500)
│
├── static/
│   ├── css/
│   │   ├── themes.css              # Light/dark theme variables
│   │   └── style.css               # Main stylesheet
│   └── js/
│       ├── theme.js                # Theme toggle
│       └── main.js                 # UI utilities
│
├── uploads/                        # User-uploaded files
│   ├── reports/                    # Project report PDFs
│   ├── source/                     # Source code ZIPs
│   └── diagrams/                   # Optional diagrams
│
├── utils/                          # Helper modules
│   ├── database.py                 # Database connection and queries
│   ├── decorators.py               # @login_required, @role_required
│   ├── file_handler.py             # Secure file upload/download
│   ├── validators.py               # Input validation
│   ├── helpers.py                  # Display utilities
│   └── auth.py                     # Authentication utilities
│
└── tests/                          # Automated tests
    ├── test_auth.py                # Authentication tests
    └── test_uploads.py             # File upload validation tests
```

## Unique Selling Points

### 1. Complete Submission-to-Discovery Workflow
Unlike generic file storage or document management systems, CampusArchive implements the entire academic project lifecycle: student submission → faculty review with feedback → institutional archive → public discovery.

### 2. Role-Based Academic Workflow
Purpose-built for educational institutions with distinct roles (student, faculty, admin) and workflows that match real academic processes.

### 3. Faculty Review Integration
Most institutional repositories lack faculty review workflows. CampusArchive makes faculty the gatekeepers, ensuring only quality-approved projects enter the permanent archive.

### 4. Smart Discovery
Full-text search, multi-dimensional filtering (department, technology, year), and tag-based browsing help users find relevant projects quickly.

### 5. Campus-Specific
Designed for a single institution's internal use, not a generic cloud service. Data stays on-premise or in the institution's own infrastructure.

### 6. Zero Vendor Lock-In
Open-source stack (Python, Flask, MySQL) with standard technologies. No proprietary platforms or APIs.

## Future Scope

The following enhancements are planned for future development:

### Short-Term Enhancements
- **Project Analytics** — Track views, downloads, and engagement per project
- **Advanced Search** — Fuzzy matching, stemming, and relevance ranking
- **Bulk Operations** — Admin ability to bulk-approve/reject projects
- **Email Notifications** — Notify students of review decisions and faculty of new submissions
- **Export Functionality** — Export project data as CSV/JSON for institutional reporting

### Medium-Term Enhancements
- **Project Versioning** — Allow students to submit updated versions of approved projects
- **Collaborative Filtering** — "Similar projects" recommendations
- **Department Analytics** — Department-specific dashboards showing trends and statistics
- **API Integration** — REST API for institutional systems integration
- **Rich Text Editor** — WYSIWYG editor for project abstracts and faculty feedback

### Long-Term Enhancements
- **Peer Review** — Optional student peer-review workflow before faculty review
- **Project Templates** — Pre-configured templates for common project types
- **Integration with LMS** — Direct integration with Canvas, Moodle, Blackboard
- **Machine Learning** — Auto-tagging of projects based on abstract/title content
- **Institutional Metrics** — Research trend analysis and technology adoption metrics

---

## Technical Highlights

- **78 files, ~8,500 lines of code** created during development
- **33 HTML templates** for complete UI coverage
- **32 Flask routes** across 6 blueprints
- **6 database tables** with proper foreign keys and indexes
- **Full-text MySQL search** on project title and abstract
- **Secure file handling** with type validation, size limits, and hash verification
- **Responsive CSS** supporting mobile, tablet, and desktop
- **Light and dark themes** with persistent user preference
- **Comprehensive error handling** with custom error pages
- **Automated test suite** for authentication and file uploads

---

## Deployment Requirements

### Environment Variables
See `.env.example` for required configuration:
- Database credentials (MySQL host, user, password)
- Secret key for session management
- File upload size limits
- Google OAuth credentials (optional)
- Admin account details

### Database Setup
1. MySQL 8.0+ with utf8mb4 support
2. Run `python init_db.py` to create schema and seed data

### Production Recommendations
- Use HTTPS (reverse proxy with SSL termination)
- Enable rate limiting
- Set up automated database backups
- Configure file storage limits based on capacity
- Use a secrets manager for production credentials

---

**CampusArchive** — Preserving student innovation for future generations.

Built with ❤️ for the Kiro Buildathon, August 2026
