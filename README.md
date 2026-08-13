# CampusArchive

**Institutional Student Project Repository**

A centralized web application for archiving, reviewing, and discovering student capstone projects, research work, and innovations. Built with Python, Flask, and MySQL.

---

## 📚 Overview

CampusArchive solves the problem of scattered, lost student projects. Every semester, students build impressive work — web applications, machine learning models, IoT systems, and more — but once the semester ends, these projects often disappear: stored on personal drives, forgotten in email attachments, or simply lost.

**CampusArchive provides:**
- Centralized institutional project repository
- Faculty review workflow with approve/reject/revision
- Searchable archive of approved projects
- Student dashboard for submission tracking
- Admin tools for user, department, and tag management

---

## ✨ Features

### For Students
- **Submit Projects**: Upload project metadata, team members, report PDF, source code ZIP
- **Track Status**: Real-time status updates (pending/approved/rejected/revision)
- **Faculty Feedback**: View review comments and resubmit revisions
- **Browse Archive**: Discover past approved projects to avoid duplication

### For Faculty
- **Review Queue**: See all projects assigned to you
- **Review Workflow**: Approve, reject, or request revisions with comments
- **Download Files**: Access project reports and source code
- **Review History**: Track all decisions made on each project

### For Admins
- **User Management**: Activate/deactivate accounts
- **Department Management**: Add and manage departments
- **Tag Management**: Configure technology tags
- **Statistics Dashboard**: View platform-wide metrics

### Security & Quality
- ✅ Email/password authentication with secure password hashing
- ✅ Google OAuth 2.0 login support
- ✅ Role-based access control (Student/Faculty/Admin)
- ✅ File upload validation (extension, size, MIME type)
- ✅ Path traversal protection
- ✅ SQL injection prevention (parameterized queries)
- ✅ Session management
- ✅ CSRF protection
- ✅ Light/dark theme support

---

## 🛠 Technology Stack

**Backend:**
- Python 3.13
- Flask 3.0.3
- PyMySQL 1.1.1
- Werkzeug 3.0.3

**Frontend:**
- HTML5, CSS3 (CSS custom properties for theming)
- Vanilla JavaScript (ES6+)
- Responsive design (mobile, tablet, desktop)

**Database:**
- MySQL 8.0
- utf8mb4 character set
- InnoDB engine

**Authentication:**
- Email/password (Werkzeug password hashing)
- Google OAuth 2.0

---

## 📂 Project Structure

```
CampusArchive/
│
├── app.py                  # Flask application entry point
├── config.py               # Configuration management
├── init_db.py              # Database initialization script
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (NOT in Git)
├── .env.example            # Environment template
├── .gitignore              # Git ignore rules
├── README.md               # This file
│
├── database/
│   ├── schema.sql          # Database schema DDL
│   ├── seed.sql            # Initial data (departments, tags)
│   └── migrations/         # Future schema migrations
│
├── routes/                 # Flask blueprints
│   ├── auth.py             # Registration, login, logout, OAuth
│   ├── student.py          # Student dashboard, project submission
│   ├── faculty.py          # Faculty dashboard, review workflow
│   ├── admin.py            # Admin dashboard, management
│   └── projects.py         # Public project browsing, detail
│
├── templates/              # Jinja2 HTML templates
│   ├── base.html           # Authenticated layout (sidebar)
│   ├── public_base.html    # Public layout (navbar)
│   ├── auth_base.html      # Auth pages layout (centered)
│   ├── home.html           # Landing page
│   ├── about.html          # About page
│   ├── auth/               # Login, register, OAuth
│   ├── student/            # Student views
│   ├── faculty/            # Faculty views
│   ├── admin/              # Admin views
│   ├── projects/           # Browse, detail
│   └── errors/             # Error pages (400, 403, 404, 413, 500)
│
├── static/
│   ├── css/
│   │   ├── themes.css      # CSS custom properties (light/dark)
│   │   └── style.css       # Main stylesheet
│   └── js/
│       ├── theme.js        # Theme toggle & persistence
│       └── main.js         # UI utilities (toast, modal, etc.)
│
├── uploads/                # Uploaded files (NOT in Git)
│   ├── reports/            # Project report PDFs
│   ├── source/             # Source code ZIPs
│   └── diagrams/           # Optional diagrams
│
├── utils/                  # Helper modules
│   ├── database.py         # Database connection & query helpers
│   ├── decorators.py       # @login_required, @role_required
│   ├── file_handler.py     # Secure file upload/download
│   ├── validators.py       # Input validation
│   └── helpers.py          # Misc utilities
│
└── tests/                  # Automated tests
    ├── test_auth.py        # Authentication tests
    └── test_uploads.py     # File upload validation tests
```

---

## 🚀 Installation & Setup

### Prerequisites

- **Python 3.9+** (tested with Python 3.13)
- **MySQL 8.0+** (or MariaDB 10.5+)
- **pip** (Python package manager)

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd CampusArchive
```

### 2. Install Python Dependencies

```bash
# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate       # On Linux/macOS
venv\Scripts\activate          # On Windows

# Install packages
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and fill in your values:
# - Generate a SECRET_KEY: python -c "import secrets; print(secrets.token_hex(32))"
# - Set your MySQL credentials (DB_HOST, DB_USER, DB_PASSWORD)
# - Set admin account details (ADMIN_EMAIL, ADMIN_PASSWORD, ADMIN_NAME)
# - Optionally configure Google OAuth (GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)
```

**Important `.env` fields:**

```env
SECRET_KEY=<generate-a-strong-random-key>
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=campus_repository
DB_USER=root
DB_PASSWORD=<your-mysql-password>

ADMIN_EMAIL=admin@campusarchive.local
ADMIN_PASSWORD=<choose-a-strong-password>
ADMIN_NAME=System Administrator
```

### 4. Setup MySQL Database

Make sure MySQL is running, then initialize the database:

```bash
python init_db.py
```

This script will:
1. Create the `campus_repository` database
2. Create all tables (users, projects, departments, tags, etc.)
3. Seed initial data (departments, technology tags)
4. Create the admin account from your `.env`

### 5. Run the Application

```bash
python app.py
```

The application will start on **http://127.0.0.1:5000**

---

## 🔑 Google OAuth Setup (Optional)

If you want to enable "Continue with Google" login:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Navigate to **APIs & Services → Credentials**
4. Create **OAuth 2.0 Client ID** (Application type: Web application)
5. Set **Authorized redirect URIs** to:
   ```
   http://localhost:5000/auth/google/callback
   ```
6. Copy the **Client ID** and **Client Secret** to your `.env`:
   ```env
   GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=your-client-secret
   GOOGLE_REDIRECT_URI=http://localhost:5000/auth/google/callback
   ```

If Google OAuth is not configured, users can still register and log in with email/password.

---

## 🧪 Testing

### Run All Tests

```bash
# Install pytest if not already installed
pip install pytest

# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_auth.py -v
python -m pytest tests/test_uploads.py -v
```

### Manual End-to-End Test

**Recommended workflow to verify everything works:**

1. **Register as Student** → http://127.0.0.1:5000/register
   - Create a student account
2. **Log in** → Submit a test project with real PDF and ZIP files
3. **Log out** → Register as Faculty (different email)
4. **Log in as Faculty** → Review the project, approve it
5. **Browse Projects** → Verify the approved project is publicly visible
6. **Log in as Admin** (credentials from `.env`) → Check admin dashboard

---

## 📊 Database Schema

**Key Tables:**

- **`users`**: Students, faculty, admins (email/password + OAuth)
- **`departments`**: Academic departments
- **`projects`**: Project metadata + status workflow
- **`project_authors`**: Many-to-many (projects ↔ students)
- **`project_attachments`**: Uploaded files (PDF, ZIP, diagrams)
- **`tags`**: Technology tags (Python, Flask, etc.)
- **`project_tags`**: Many-to-many (projects ↔ tags)
- **`faculty_reviews`**: Review history (decision + comments)

**Status Workflow:**

```
PENDING → (faculty review) → APPROVED
                           → REJECTED
                           → NEEDS_REVISION → (student resubmit) → PENDING
```

---

## 🔒 Security Considerations

✅ **Implemented:**
- Passwords hashed with Werkzeug's `pbkdf2:sha256`
- SQL queries use parameterized statements (no concatenation)
- File uploads validated by extension, size, and hash
- Uploaded filenames are sanitized (never use original filename as storage name)
- Path traversal protection (`get_absolute_path` checks)
- Role-based authorization via decorators
- Session cookies are HttpOnly + SameSite=Lax
- Secrets stored in `.env` (not in Git)
- `.gitignore` prevents committing sensitive files

⚠ **For Production:**
- Use HTTPS (set `SESSION_COOKIE_SECURE=True`)
- Run behind a reverse proxy (Nginx, Apache)
- Enable CSRF protection for state-changing forms
- Set up rate limiting (Flask-Limiter)
- Use a secrets manager for production credentials
- Enable MySQL SSL connections
- Implement logging and monitoring
- Regular database backups

---

## 🎨 Customization

### Change College Name / Logo

- Edit `templates/base.html`, `templates/public_base.html`, and `templates/auth_base.html`
- Replace the logo icon and text in `.sidebar-logo`, `.nav-brand`, and `.auth-logo`

### Modify Departments

- Run `init_db.py` after editing `database/seed.sql`, OR
- Use the Admin → Departments page to add/remove departments

### Add Technology Tags

- Admin → Tags page (add new tags dynamically)
- OR edit `database/seed.sql` and re-run `init_db.py`

### Theme Colors

Edit `static/css/themes.css` to customize light/dark mode color palettes.

---

## 🐛 Troubleshooting

### "Cannot connect to MySQL"

- Verify MySQL is running:
  ```bash
  # Windows
  net start MySQL80

  # Linux/macOS
  sudo systemctl start mysql
  ```
- Check `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD` in `.env`
- Test connection: `mysql -h 127.0.0.1 -u root -p`

### "SECRET_KEY is not set"

- Make sure `.env` exists in the project root
- Copy `.env.example` to `.env` and generate a SECRET_KEY:
  ```bash
  python -c "import secrets; print(secrets.token_hex(32))"
  ```

### "File too large" (413 error)

- Increase `MAX_REPORT_SIZE_MB` or `MAX_SOURCE_SIZE_MB` in `.env`
- Restart the Flask app after changing `.env`

### Google OAuth not working

- Verify `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` in `.env`
- Check that the redirect URI in Google Console matches your `.env`:
  ```
  http://localhost:5000/auth/google/callback
  ```
- Ensure the OAuth consent screen is configured

### Uploaded files not appearing

- Check that `uploads/` directory and subdirectories exist
- Verify file permissions (Flask process must be able to write)
- Check Flask logs for file validation errors

---

## 👥 Team

CampusArchive was designed and built by a team of 5 second-year BTech IT students as our semester capstone project.

---

## 📄 License

This project is open-source and available for educational use.

---

## 🙏 Acknowledgments

- Flask documentation: https://flask.palletsprojects.com/
- PyMySQL: https://pymysql.readthedocs.io/
- Google OAuth 2.0: https://developers.google.com/identity/protocols/oauth2

---

## 📞 Support

For questions, issues, or feature requests:
1. Check the **Troubleshooting** section above
2. Review the code comments in `routes/`, `utils/`, and `templates/`
3. Open an issue on the project repository

---

**Happy Archiving! 🎓📁**
