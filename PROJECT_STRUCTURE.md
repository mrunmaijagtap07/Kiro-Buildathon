# CampusArchive - Complete Folder Structure

```
CampusArchive/
│
├── 📄 Root Files
│   ├── .env                                    # Environment variables (SECRET)
│   ├── .env.example                           # Environment template
│   ├── .gitignore                             # Git ignore rules
│   ├── app.py                                 # Flask application entry point
│   ├── config.py                              # Configuration management
│   ├── init_db.py                             # Database initialization script
│   ├── requirements.txt                       # Python dependencies
│   ├── smoke_test.py                          # Quick functionality test
│   ├── Schema_DDL.sql                         # Database schema DDL
│   │
│   └── 📚 Documentation Files
│       ├── README.md                          # Main project documentation
│       ├── QUICKSTART.md                      # Quick start guide
│       ├── TESTING_GUIDE.md                   # Testing instructions
│       ├── IMPLEMENTATION_SUMMARY.md          # Implementation details
│       ├── FRONTEND_REDESIGN_COMPLETE.md      # Redesign completion summary
│       ├── FRONTEND_REDESIGN_DOCUMENTATION.md # Complete redesign documentation
│       ├── REDESIGN_SUMMARY.md                # Quick redesign summary
│       └── CHANGELOG_FRONTEND.md              # Frontend changes log
│
├── 📂 .kiro/                                   # Kiro CLI configuration
│   ├── agents/
│   └── settings/
│       └── cli.json
│
├── 📂 .kiro-workspace/                         # Kiro workspace data
│   ├── cli_chat/
│   │   └── .kiro/
│   │       ├── agents/
│   │       └── settings/
│   │           └── cli.json
│   └── _bg/
│       └── .kiro/
│           ├── agents/
│           └── settings/
│               └── cli.json
│
├── 📂 .pytest_cache/                           # Pytest cache directory
│   ├── .gitignore
│   ├── CACHEDIR.TAG
│   ├── README.md
│   └── v/
│       └── cache/
│           └── nodeids
│
├── 📂 database/                                # Database scripts
│   ├── schema.sql                             # Database schema DDL
│   ├── seed.sql                               # Initial seed data
│   └── migrations/                            # Future schema migrations (empty)
│
├── 📂 routes/                                  # Flask blueprints (API routes)
│   ├── __init__.py                            # Routes package initializer
│   ├── admin.py                               # Admin routes
│   ├── auth.py                                # Authentication routes
│   ├── faculty.py                             # Faculty routes
│   ├── projects.py                            # Project browsing routes
│   ├── student.py                             # Student routes
│   └── __pycache__/                           # Python bytecode cache
│       ├── __init__.cpython-313.pyc
│       ├── admin.cpython-313.pyc
│       ├── auth.cpython-313.pyc
│       ├── faculty.cpython-313.pyc
│       ├── projects.cpython-313.pyc
│       └── student.cpython-313.pyc
│
├── 📂 static/                                  # Static assets
│   │
│   ├── 📂 css/                                # Stylesheets
│   │   ├── themes.css                         # Theme system (light/dark mode)
│   │   └── style.css                          # Main stylesheet
│   │
│   ├── 📂 icons/                              # Icon assets (empty)
│   │
│   ├── 📂 images/                             # Image assets (empty)
│   │
│   └── 📂 js/                                 # JavaScript files
│       ├── main.js                            # Main UI utilities
│       └── theme.js                           # Theme toggle functionality
│
├── 📂 templates/                               # Jinja2 HTML templates
│   │
│   ├── 📄 Base Templates
│   │   ├── base.html                          # Authenticated pages layout (sidebar)
│   │   ├── public_base.html                   # Public pages layout (navbar)
│   │   └── auth_base.html                     # Authentication pages layout
│   │
│   ├── 📄 Main Pages
│   │   ├── home.html                          # Landing page
│   │   └── about.html                         # About page
│   │
│   ├── 📂 admin/                              # Admin dashboard pages
│   │   ├── dashboard.html                     # Admin dashboard home
│   │   ├── departments.html                   # Department management
│   │   ├── statistics.html                    # Platform statistics
│   │   ├── tags.html                          # Technology tags management
│   │   └── users.html                         # User management
│   │
│   ├── 📂 auth/                               # Authentication pages
│   │   ├── login.html                         # Login page
│   │   ├── register.html                      # Registration page
│   │   └── complete_profile.html              # OAuth profile completion
│   │
│   ├── 📂 components/                         # Reusable components (empty)
│   │
│   ├── 📂 errors/                             # Error pages
│   │   ├── 400.html                           # Bad Request
│   │   ├── 403.html                           # Forbidden (Access Denied)
│   │   ├── 404.html                           # Not Found
│   │   ├── 413.html                           # Payload Too Large
│   │   ├── 500.html                           # Internal Server Error
│   │   └── error_styles.html                  # Shared error page styles
│   │
│   ├── 📂 faculty/                            # Faculty dashboard pages
│   │   ├── dashboard.html                     # Faculty dashboard home
│   │   ├── reviews.html                       # Review queue list
│   │   └── review.html                        # Individual project review
│   │
│   ├── 📂 projects/                           # Public project pages
│   │   ├── browse.html                        # Browse/search projects
│   │   └── detail.html                        # Project detail view
│   │
│   └── 📂 student/                            # Student dashboard pages
│       ├── dashboard.html                     # Student dashboard home
│       ├── my_projects.html                   # Student's project list
│       ├── project_detail.html                # Student's project detail view
│       ├── submit_project.html                # New project submission form
│       └── resubmit.html                      # Project resubmission form
│
├── 📂 tests/                                   # Automated tests
│   ├── __init__.py                            # Tests package initializer
│   ├── test_auth.py                           # Authentication tests
│   ├── test_uploads.py                        # File upload tests
│   └── __pycache__/                           # Python bytecode cache
│       ├── __init__.cpython-313.pyc
│       └── test_uploads.cpython-313-pytest-9.1.1.pyc
│
├── 📂 uploads/                                 # User uploaded files (NOT in Git)
│   ├── diagrams/                              # Optional project diagrams
│   │   └── .gitkeep
│   ├── reports/                               # Project report PDFs
│   │   └── .gitkeep
│   └── source/                                # Source code ZIP files
│       └── .gitkeep
│
├── 📂 utils/                                   # Helper utilities
│   ├── __init__.py                            # Utils package initializer
│   ├── auth.py                                # Authentication helpers
│   ├── database.py                            # Database connection & queries
│   ├── decorators.py                          # Route decorators (@login_required)
│   ├── file_handler.py                        # Secure file upload/download
│   ├── helpers.py                             # Miscellaneous utilities
│   ├── validators.py                          # Input validation functions
│   └── __pycache__/                           # Python bytecode cache
│       ├── __init__.cpython-313.pyc
│       ├── auth.cpython-313.pyc
│       ├── database.cpython-313.pyc
│       ├── decorators.cpython-313.pyc
│       ├── file_handler.cpython-313.pyc
│       ├── helpers.cpython-313.pyc
│       └── validators.cpython-313.pyc
│
└── 📂 __pycache__/                             # Root Python bytecode cache
    ├── app.cpython-313.pyc
    ├── config.cpython-313.pyc
    └── init_db.cpython-313.pyc
```

---

## 📊 File Count Summary

### By Type
- **HTML Templates:** 33 files
  - Base templates: 3
  - Main pages: 2
  - Admin pages: 5
  - Auth pages: 3
  - Error pages: 6
  - Faculty pages: 3
  - Project pages: 2
  - Student pages: 5
  - Components: 0 (directory exists but empty)

- **Python Files:** 18 files
  - Root: 4 (app.py, config.py, init_db.py, smoke_test.py)
  - Routes: 6 (+ __init__.py)
  - Utils: 7 (+ __init__.py)
  - Tests: 3 (+ __init__.py)

- **CSS Files:** 2 files
  - themes.css (theme system)
  - style.css (main styles)

- **JavaScript Files:** 2 files
  - main.js (UI utilities)
  - theme.js (theme toggle)

- **SQL Files:** 3 files
  - schema.sql (database)
  - seed.sql (database)
  - Schema_DDL.sql (root)

- **Documentation Files:** 8 files
  - README.md
  - QUICKSTART.md
  - TESTING_GUIDE.md
  - IMPLEMENTATION_SUMMARY.md
  - FRONTEND_REDESIGN_COMPLETE.md
  - FRONTEND_REDESIGN_DOCUMENTATION.md
  - REDESIGN_SUMMARY.md
  - CHANGELOG_FRONTEND.md

- **Configuration Files:** 3 files
  - .env (secret)
  - .env.example
  - requirements.txt

### Total Count
- **Source Files:** 69 files (excluding cache/bytecode)
- **Cache Files:** ~15 .pyc files
- **Total Files:** ~84 files

---

## 🎯 Key Frontend Files (HTML Templates)

### Public-Facing Pages (7 files)
1. `templates/home.html` - Landing page with hero, stats, featured projects
2. `templates/about.html` - About page with feature sections
3. `templates/projects/browse.html` - Browse/search projects with filters
4. `templates/projects/detail.html` - Individual project detail view
5. `templates/auth/login.html` - User login page
6. `templates/auth/register.html` - New user registration
7. `templates/auth/complete_profile.html` - OAuth profile completion

### Error Pages (6 files)
8. `templates/errors/404.html` - Page not found
9. `templates/errors/403.html` - Access denied
10. `templates/errors/400.html` - Bad request
11. `templates/errors/500.html` - Server error
12. `templates/errors/413.html` - File too large
13. `templates/errors/error_styles.html` - Shared error styles

### Student Dashboard (5 files)
14. `templates/student/dashboard.html` - Student home dashboard
15. `templates/student/my_projects.html` - List of student's projects
16. `templates/student/project_detail.html` - Student's project detail view
17. `templates/student/submit_project.html` - New project submission form
18. `templates/student/resubmit.html` - Project resubmission form

### Faculty Dashboard (3 files)
19. `templates/faculty/dashboard.html` - Faculty home dashboard
20. `templates/faculty/reviews.html` - Review queue (projects to review)
21. `templates/faculty/review.html` - Individual project review page

### Admin Dashboard (5 files)
22. `templates/admin/dashboard.html` - Admin home dashboard
23. `templates/admin/users.html` - User management
24. `templates/admin/departments.html` - Department management
25. `templates/admin/tags.html` - Technology tags management
26. `templates/admin/statistics.html` - Platform-wide statistics

### Base Templates (3 files)
27. `templates/base.html` - Authenticated layout with sidebar
28. `templates/public_base.html` - Public layout with navbar
29. `templates/auth_base.html` - Auth pages layout (centered card)

---

## 🎨 Frontend Assets

### CSS Files (2 files)
- `static/css/themes.css` - Theme variables (light/dark mode colors)
- `static/css/style.css` - Main stylesheet (~1500+ lines)

### JavaScript Files (2 files)
- `static/js/theme.js` - Theme toggle and persistence
- `static/js/main.js` - UI utilities (toasts, modals, etc.)

### Asset Directories
- `static/icons/` - Icon assets (currently empty)
- `static/images/` - Image assets (currently empty)

---

## 🔧 Backend Structure

### Routes (Flask Blueprints) - 6 files
- `routes/auth.py` - Registration, login, logout, OAuth
- `routes/student.py` - Student dashboard and project submission
- `routes/faculty.py` - Faculty dashboard and review workflow
- `routes/admin.py` - Admin dashboard and management
- `routes/projects.py` - Public project browsing and detail
- `routes/__init__.py` - Package initializer

### Utilities - 7 files
- `utils/database.py` - Database connection & query helpers
- `utils/decorators.py` - @login_required, @role_required decorators
- `utils/file_handler.py` - Secure file upload/download
- `utils/validators.py` - Input validation functions
- `utils/helpers.py` - Miscellaneous utilities
- `utils/auth.py` - Authentication helpers
- `utils/__init__.py` - Package initializer

### Database - 2 files + migrations directory
- `database/schema.sql` - Complete database schema
- `database/seed.sql` - Initial seed data (departments, tags)
- `database/migrations/` - Future schema migrations (empty)

### Tests - 3 files
- `tests/test_auth.py` - Authentication flow tests
- `tests/test_uploads.py` - File upload validation tests
- `tests/__init__.py` - Package initializer

---

## 📁 Directory Purpose

| Directory | Purpose | File Count |
|-----------|---------|------------|
| `/` | Root configuration and entry points | 16 files |
| `database/` | Database scripts and migrations | 2 files |
| `routes/` | Flask blueprints (API endpoints) | 6 files |
| `static/css/` | Stylesheets | 2 files |
| `static/js/` | JavaScript | 2 files |
| `templates/` | HTML templates | 33 files |
| `templates/admin/` | Admin dashboard pages | 5 files |
| `templates/auth/` | Authentication pages | 3 files |
| `templates/errors/` | Error pages | 6 files |
| `templates/faculty/` | Faculty dashboard pages | 3 files |
| `templates/projects/` | Public project pages | 2 files |
| `templates/student/` | Student dashboard pages | 5 files |
| `tests/` | Automated tests | 3 files |
| `uploads/` | User uploaded files | 3 .gitkeep |
| `utils/` | Helper utilities | 7 files |

---

**Total Project Files:** ~84 files (excluding cache)  
**Frontend HTML Templates:** 33 files  
**Backend Python Files:** 18 files  
**CSS Files:** 2 files  
**JavaScript Files:** 2 files  
**Documentation Files:** 8 files

---

Generated: August 13, 2026, 8:32 PM IST
