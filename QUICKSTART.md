# CampusArchive — Quick Start Guide

**Get the application running in 5 minutes.**

---

## Prerequisites Check

Before you begin, ensure you have:

- [x] **Python 3.9+** installed (`python --version`)
- [x] **MySQL 8.0+** installed and running
- [x] **pip** available (`pip --version`)

---

## Step-by-Step Setup

### 1. Install Dependencies

```bash
cd CampusArchive
pip install -r requirements.txt
```

Expected packages: Flask, PyMySQL, Werkzeug, python-dotenv, requests

---

### 2. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env    # Linux/macOS
copy .env.example .env  # Windows

# Edit .env with your favorite editor
notepad .env            # Windows
nano .env               # Linux/macOS
```

**Required changes in `.env`:**

```env
# 1. Generate a strong secret key
SECRET_KEY=<run: python -c "import secrets; print(secrets.token_hex(32))">

# 2. Set your MySQL password
DB_PASSWORD=your_actual_mysql_password

# 3. Set admin account (for first login)
ADMIN_EMAIL=admin@yourdomain.com
ADMIN_PASSWORD=ChooseAStrongPassword123

# 4. (Optional) Google OAuth — leave blank to skip
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
```

---

### 3. Initialize Database

Make sure MySQL is running, then:

```bash
python init_db.py
```

**What this does:**
- Creates `campus_repository` database
- Creates all tables (users, projects, departments, tags, reviews)
- Seeds 8 departments (IT, CS, EC, ME, CE, EE, AIDS, CSBS)
- Seeds 48 technology tags (Python, Flask, Java, React, etc.)
- Creates your admin account from `.env`

**Expected output:**
```
✓ Connected to MySQL at 127.0.0.1:3306
→ Applying schema.sql ...
  ✓ Schema applied.
→ Applying seed.sql ...
  ✓ Seed data applied.
  ✓ Admin account created: admin@yourdomain.com
Database initialization complete.
```

---

### 4. Start the Application

```bash
python app.py
```

**Expected output:**
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

---

### 5. Open in Browser

Navigate to: **http://127.0.0.1:5000**

You should see the CampusArchive landing page.

---

## First Login & Testing

### Test the Admin Account

1. Go to **http://127.0.0.1:5000/login**
2. Log in with:
   - Email: `ADMIN_EMAIL` from your `.env`
   - Password: `ADMIN_PASSWORD` from your `.env`
3. You'll land on the **Admin Dashboard**

### Create a Student Account

1. Click **Register** from the home page
2. Fill in the form:
   - Full Name: `Test Student`
   - Email: `student@test.com`
   - Password: `Student123`
   - Role: **Student**
   - Department: Select any
   - Roll/Employee ID: `22IT001` (optional)
3. Click **Create Account**
4. Log in with the new credentials

### Submit a Test Project

1. From the student dashboard, click **Submit New Project**
2. Fill in the form:
   - Title: `Sample Project`
   - Abstract: At least 50 characters describing the project
   - Academic Year: Select current year
   - Department: Select your department
   - Faculty Guide: Select any faculty (you'll need to create one first)
   - Technology Tags: Select relevant tags
   - Upload a real PDF file as the report
   - Upload a real ZIP file as source code
3. Click **Submit Project**

### Create a Faculty Account & Review

1. Log out, then register again as **Faculty**
2. Log in as faculty
3. Go to **Faculty Dashboard** → **Review Queue**
4. Click **Review** on the pending project
5. Select **Approve** and add a comment
6. Click **Submit Review**

### Browse Approved Projects

1. Go to **Browse Projects** (from navbar)
2. The approved project should now appear
3. Click on it to view details
4. Download the report PDF

---

## Troubleshooting

### "Cannot connect to MySQL"

**Solution:**
- Verify MySQL is running:
  ```bash
  # Windows
  net start MySQL80
  
  # Linux
  sudo systemctl start mysql
  ```
- Check `DB_PASSWORD` in `.env` matches your MySQL root password

### "SECRET_KEY is not set"

**Solution:**
- Generate a key: `python -c "import secrets; print(secrets.token_hex(32))"`
- Paste it into `.env` as `SECRET_KEY=...`
- Restart the app

### "File too large" (413 error)

**Solution:**
- Increase limits in `.env`:
  ```env
  MAX_REPORT_SIZE_MB=20
  MAX_SOURCE_SIZE_MB=50
  ```
- Restart the app

### Google OAuth not working

**Solution:**
- Either configure proper Google OAuth credentials in `.env`, OR
- Leave `GOOGLE_CLIENT_ID` blank and use email/password login only

### Port 5000 already in use

**Solution:**
- Change the port in `app.py` (last line):
  ```python
  app.run(host="127.0.0.1", port=5001, debug=...)
  ```

---

## Next Steps

Once the application is running:

1. **Read the full README.md** for detailed documentation
2. **Review IMPLEMENTATION_SUMMARY.md** to understand what was built
3. **Check the code comments** in `routes/`, `utils/`, and `templates/`
4. **Customize** departments, tags, and branding to match your college
5. **Deploy** to a production server for your hackathon demo

---

## Quick Command Reference

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database (run once)
python init_db.py

# Start application
python app.py

# Run tests
pip install pytest
python -m pytest tests/ -v

# Smoke test (check everything imports)
python smoke_test.py
```

---

## Support

- **Documentation:** `README.md`
- **Implementation Details:** `IMPLEMENTATION_SUMMARY.md`
- **Code Comments:** Check `routes/`, `utils/`, `templates/`

---

**Happy Archiving! 🎓📁**
