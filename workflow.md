# CampusArchive Workflows

Complete workflow documentation for the CampusArchive platform.

---

## Overview

CampusArchive implements four distinct user workflows:
1. **Public Visitor Flow** — Browse and discover approved projects
2. **Student Flow** — Submit projects, track status, resubmit if needed
3. **Faculty Flow** — Review assigned projects, provide feedback, make decisions
4. **Admin Flow** — Manage users, departments, tags, and platform settings

---

## 1. Public Visitor Flow

### Entry Point
```
https://campusarchive.example.edu/
```

### Workflow Steps

#### Step 1: Landing Page
- Visitor arrives at homepage (`/`)
- Sees platform statistics:
  - Total approved projects
  - Number of departments
  - Number of technologies
  - Number of faculty guides
- Views recently approved projects (6 most recent)
- Can search projects from hero section

#### Step 2: Browse Projects
- Click "Explore Archive" or "Browse Projects" in navigation
- Navigates to `/projects/browse`
- Views all approved projects with pagination
- Can search by keyword (full-text search on title and abstract)
- Can filter by:
  - Department (dropdown)
  - Technology tags (multi-select)
  - Academic year (dropdown)

#### Step 3: View Project Details
- Click on any project card
- Navigates to `/projects/detail/<project_id>`
- Views complete project information:
  - Project title and abstract
  - Academic year and department
  - Team members (lead student + co-authors)
  - Faculty guide
  - Technology tags
  - Submission date
- Can download:
  - Project report PDF
  - Source code ZIP
  - Optional diagrams
- Download counters increment automatically

#### Step 4: Search and Filter
- Use search bar to find specific projects
- Apply department filter to see projects from specific department
- Click technology tags to see projects using that technology
- Filter by academic year to see historical projects

### No Authentication Required
Public visitors can browse, search, and download WITHOUT creating an account or logging in.

---

## 2. Student Flow

### Entry Point
```
/register or /login
```

### Workflow Steps

#### Step 1: Registration
**Route:** `/register`

**Process:**
1. Student clicks "Register" from navigation
2. Fills registration form:
   - Full name
   - Email address (validated for uniqueness)
   - Password (hashed with Werkzeug pbkdf2:sha256)
   - Confirm password
   - Role selection (Student)
   - Department selection
   - Roll number (student ID)
3. Submits form
4. Account created with `is_active=True` by default
5. Redirected to login page with success message

**Alternative: Google OAuth**
1. Click "Continue with Google"
2. Authorize institutional Google account
3. If first time: redirected to `/auth/complete-profile` to select department and roll number
4. Profile completed → redirected to student dashboard

#### Step 2: Login
**Route:** `/login`

**Process:**
1. Enter email and password
2. System validates credentials
3. Session created with `user_id` and `role`
4. Redirected to `/student/dashboard`

#### Step 3: Student Dashboard
**Route:** `/student/dashboard`

**Dashboard shows:**
- Welcome message with student name
- Statistics cards:
  - Total submissions
  - Pending review count
  - Approved count
  - Needs revision count
  - Rejected count
- Recent submissions table:
  - Project title
  - Department
  - Academic year
  - Status (badge with color)
  - Submission date
  - "View" action button

**Actions available:**
- "Submit New Project" button (top-right)
- "View All" link to see complete project list
- Click any project to view details

#### Step 4: Submit New Project
**Route:** `/student/submit-project`

**Form fields:**
1. **Project Information:**
   - Project title (required, max 255 characters)
   - Abstract (required, text area, min 100 characters)
   - Academic year (dropdown, current and previous years)
   - Department (dropdown, pre-populated from database)

2. **Team Information:**
   - Lead student (auto-filled with logged-in student)
   - Co-authors (comma-separated emails, optional)
   - Faculty guide (dropdown, shows active faculty from same department)

3. **Technology Tags:**
   - Multi-select checkbox list of active tags
   - Examples: Python, Flask, MySQL, React, Machine Learning, IoT

4. **File Uploads:**
   - **Project Report** (required):
     - Accepts: PDF only
     - Max size: 10MB (configurable via .env)
     - Validation: MIME type, extension, size
   - **Source Code** (required):
     - Accepts: ZIP only
     - Max size: 50MB (configurable via .env)
     - Validation: MIME type, extension, size
   - **Diagram** (optional):
     - Accepts: PNG, JPG, JPEG
     - Max size: 5MB
     - Validation: MIME type, extension, size

5. **Submit:**
   - Click "Submit Project"
   - Files uploaded to `/uploads/` subdirectories
   - Files stored with hash-based names (security)
   - Project record created with `status='PENDING'`
   - Redirected to student dashboard with success message

**Validation:**
- All required fields must be filled
- Email must be valid format
- Files must meet type and size requirements
- Faculty guide must be active faculty from same department

#### Step 5: Track Submission Status
**Route:** `/student/my-projects` or `/student/project/<project_id>`

**Status values:**
- **PENDING** — Awaiting faculty review (yellow badge)
- **APPROVED** — Faculty approved, now in public archive (green badge)
- **REJECTED** — Faculty rejected with feedback (red badge)
- **NEEDS_REVISION** — Faculty requested changes (blue badge)

**For each status:**
- **PENDING:** "Your project is under review by [Faculty Name]"
- **APPROVED:** "Congratulations! Your project is now part of the archive"
- **REJECTED:** View faculty feedback, no resubmission allowed
- **NEEDS_REVISION:** View faculty feedback, "Resubmit" button available

#### Step 6: View Faculty Feedback
**Route:** `/student/project/<project_id>`

**Displays:**
- Complete project details
- Current status
- Faculty review history:
  - Reviewer name
  - Review date
  - Decision (Approved/Rejected/Needs Revision)
  - Feedback comments (full text)

**For multi-submission projects:**
- Shows all previous reviews
- Most recent review at top

#### Step 7: Resubmit Project (if NEEDS_REVISION)
**Route:** `/student/resubmit/<project_id>`

**Process:**
1. Click "Resubmit Project" from project detail page
2. Pre-filled form with existing data
3. Can update:
   - Project title
   - Abstract
   - Technology tags
   - Replace uploaded files (optional)
   - Update team members (optional)
4. **Cannot change:**
   - Department
   - Faculty guide
   - Academic year
5. Submit resubmission
6. `status` changes back to 'PENDING'
7. `submitted_at` timestamp updated
8. Faculty sees updated project in review queue

---

## 3. Faculty Flow

### Entry Point
```
/login (with faculty credentials)
```

### Workflow Steps

#### Step 1: Login
**Route:** `/login`

**Process:**
1. Enter email and password
2. System validates credentials and checks `role='FACULTY'`
3. Session created
4. Redirected to `/faculty/dashboard`

#### Step 2: Faculty Dashboard
**Route:** `/faculty/dashboard`

**Dashboard shows:**
- Welcome message with faculty name
- Statistics cards:
  - Total projects assigned as guide
  - Pending review count
  - Approved count
  - Rejected count
  - Needs revision count
- Recent activity:
  - Recent submissions requiring review
  - Recent reviews completed

**Actions available:**
- "Review Queue" navigation link
- Quick links to projects by status

#### Step 3: Review Queue
**Route:** `/faculty/reviews`

**Displays table of all projects where logged-in faculty is the assigned guide:**

**Columns:**
- Project title
- Department
- Lead student name
- Submission date
- Current status
- "Review" action button

**Filtering:**
- Filter by status dropdown (All/Pending/Needs Revision/Approved/Rejected)
- Sort by submission date (newest first by default)

**Only projects assigned to THIS faculty are shown.**

#### Step 4: Review Individual Project
**Route:** `/faculty/review/<project_id>`

**Page sections:**

**A. Project Information:**
- Title and abstract
- Academic year and department
- Submission date

**B. Team Information:**
- Lead student (name, email, roll number)
- Co-authors list
- Faculty guide (self)

**C. Technology Tags:**
- List of selected tags

**D. Files:**
- Download project report PDF
- Download source code ZIP
- Download diagram (if uploaded)
- View file sizes and upload dates

**E. Review History (if resubmission):**
- Previous reviews listed chronologically
- Each review shows:
  - Reviewer name
  - Review date
  - Decision
  - Feedback provided

**F. Review Form:**
- **Decision radio buttons:**
  - ✅ Approve — Project is acceptable, add to archive
  - ❌ Reject — Project is not acceptable, provide feedback
  - 📝 Request Revision — Project needs changes, provide specific feedback
- **Feedback textarea:**
  - Required for Reject and Request Revision
  - Optional for Approve (can provide positive comments)
  - Character limit: 2000 characters
- **Submit Review button**

#### Step 5: Submit Review
**Process:**
1. Faculty selects decision (Approve/Reject/Request Revision)
2. Provides feedback (required for Reject/Revision, optional for Approve)
3. Clicks "Submit Review"
4. System:
   - Updates `projects.status` to selected decision
   - Creates `faculty_reviews` record with:
     - `reviewer_id` (logged-in faculty)
     - `project_id`
     - `decision`
     - `comments` (feedback text)
     - `reviewed_at` (timestamp)
   - If Approved: Project becomes visible in public browse
   - If Rejected: Student can view feedback but cannot resubmit
   - If Needs Revision: Student can view feedback and resubmit
5. Redirected to review queue with success message

#### Step 6: View Review History
**Route:** `/faculty/reviews` filtered by "Reviewed"

**Shows all completed reviews:**
- Projects reviewed
- Decision made
- Date reviewed
- Can re-open project to view details (read-only if already decided)

---

## 4. Admin Flow

### Entry Point
```
/login (with admin credentials)
```

### Workflow Steps

#### Step 1: Login
**Route:** `/login`

**Process:**
1. Enter admin email and password (from .env: ADMIN_EMAIL, ADMIN_PASSWORD)
2. System validates credentials and checks `role='ADMIN'`
3. Session created
4. Redirected to `/admin/dashboard`

#### Step 2: Admin Dashboard
**Route:** `/admin/dashboard`

**Platform Statistics:**
- Total users (Students/Faculty/Admins breakdown)
- Total projects (by status)
- Total departments
- Total technology tags
- Recent activity feed

**Quick Actions:**
- Manage Users
- Manage Departments
- Manage Tags
- View Statistics

#### Step 3: User Management
**Route:** `/admin/users`

**Displays table of all users:**

**Columns:**
- Full name
- Email
- Role (Student/Faculty/Admin)
- Department
- Roll/Employee ID
- Status (Active/Inactive)
- Registration date
- "Activate/Deactivate" toggle

**Actions:**
- Filter by role (All/Student/Faculty/Admin)
- Filter by department
- Search by name or email
- Activate/deactivate users
- View user details (projects submitted, reviews completed)

**Activate/Deactivate:**
- Click toggle button
- Updates `is_active` flag in database
- Inactive users cannot log in
- Confirmation prompt before deactivation

#### Step 4: Department Management
**Route:** `/admin/departments`

**Displays table of all departments:**

**Columns:**
- Department code
- Department name
- Status (Active/Inactive)
- Project count
- Created date
- "Edit" and "Activate/Deactivate" buttons

**Actions:**
- **Add New Department:**
  - Click "Add Department"
  - Fill form (department code, department name)
  - Submit → Department created as active
- **Edit Department:**
  - Click "Edit"
  - Update name or code
  - Submit → Department updated
- **Activate/Deactivate:**
  - Toggle status
  - Inactive departments hidden from dropdowns in submission forms

#### Step 5: Technology Tag Management
**Route:** `/admin/tags`

**Displays table of all tags:**

**Columns:**
- Tag name
- Status (Active/Inactive)
- Project count (how many projects use this tag)
- Created date
- "Edit" and "Activate/Deactivate" buttons

**Actions:**
- **Add New Tag:**
  - Click "Add Tag"
  - Enter tag name (e.g., "Python", "Machine Learning", "IoT")
  - Submit → Tag created as active
- **Edit Tag:**
  - Click "Edit"
  - Update tag name
  - Submit → Tag updated
- **Activate/Deactivate:**
  - Toggle status
  - Inactive tags hidden from submission forms and filters

#### Step 6: Platform Statistics
**Route:** `/admin/statistics`

**Comprehensive metrics:**
- Projects per department (bar chart or table)
- Projects per technology (sorted by popularity)
- Projects per academic year
- Approval rate (approved vs total submitted)
- Most active faculty (by review count)
- Most active students (by submission count)
- Monthly submission trends

---

## 5. Authentication Flow

### Email/Password Authentication

**Registration Flow:**
```
User → /register
     → Fill form (name, email, password, role, department, ID)
     → Submit
     → System:
        - Validates email uniqueness
        - Hashes password (Werkzeug pbkdf2:sha256)
        - Creates user record with is_active=True
        - Redirects to /login
```

**Login Flow:**
```
User → /login
     → Enter email and password
     → System:
        - Queries user by email
        - Verifies password hash
        - Checks is_active=True
        - Creates session (user_id, role, full_name)
        - Redirects to role-specific dashboard:
          - Student → /student/dashboard
          - Faculty → /faculty/dashboard
          - Admin → /admin/dashboard
```

**Logout Flow:**
```
User → Click "Logout"
     → System clears session
     → Redirects to homepage (/)
```

### Google OAuth 2.0 Authentication

**Configuration:**
- Requires `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` in .env
- Redirect URI: `/auth/google/callback`

**First-Time OAuth Flow:**
```
User → /login
     → Click "Continue with Google"
     → Redirected to Google OAuth consent screen
     → User authorizes institutional account
     → Google redirects to /auth/google/callback with code
     → System:
        - Exchanges code for access token
        - Fetches user profile (email, name, google_id)
        - Checks if google_id exists in database
        - If NEW user:
          - Creates user record:
            - email, full_name from Google
            - google_id stored
            - password_hash=NULL
            - auth_provider='GOOGLE'
            - department_id=NULL (to be completed)
            - role=NULL (to be completed)
          - Redirects to /auth/complete-profile
        - If EXISTING user:
          - Updates last_login_at
          - Creates session
          - Redirects to role-specific dashboard
```

**Profile Completion Flow (OAuth):**
```
User → /auth/complete-profile (pre-populated: email, name)
     → Select role (Student/Faculty)
     → Select department
     → Enter roll/employee ID
     → Submit
     → System:
        - Updates user record with role, department, roll_id
        - Redirects to role-specific dashboard
```

**Subsequent OAuth Logins:**
```
User → /login → "Continue with Google"
     → OAuth flow completes
     → System finds existing google_id
     → Session created
     → Redirects to dashboard
```

---

## 6. Data Flow Architecture

### Frontend → Backend → Database Flow

```
[Browser]
   ↓ HTTP Request (form submission, link click)
[Flask Route] (e.g., routes/student.py)
   ↓ Parse request, validate session (@login_required decorator)
[Route Handler Function]
   ↓ Call database utility
[utils/database.py] (query_one, query_all, execute_query)
   ↓ Execute parameterized SQL query
[MySQL Database] (campus_repository)
   ↓ Return result rows
[utils/database.py]
   ↓ Return dict/list to route
[Route Handler]
   ↓ Pass data to template
[Jinja2 Template] (templates/*.html)
   ↓ Render HTML with data
[HTTP Response]
   ↓
[Browser] displays page
```

### File Upload Flow

```
[Student Browser]
   ↓ Selects files (PDF, ZIP) in form
   ↓ Submits form with multipart/form-data
[Flask Route] /student/submit-project
   ↓ Receives file objects from request.files
[utils/file_handler.py::upload_file()]
   ↓ Validates file:
     - Check extension (.pdf, .zip)
     - Check MIME type
     - Check file size (< MAX_SIZE)
   ↓ Generate secure filename:
     - Hash file content (SHA-256)
     - Use hash as filename (prevents collisions, path traversal)
   ↓ Save file to /uploads/reports/ or /uploads/source/
   ↓ Return file metadata (path, size, hash)
[Flask Route]
   ↓ Store file metadata in project_attachments table:
     - project_id
     - file_type (REPORT_PDF, SOURCE_ZIP, DIAGRAM)
     - original_name (user's filename)
     - stored_file_path (hash-based path)
     - file_size_bytes
     - file_hash
[MySQL Database]
   ↓ Record saved
[Response]
   ↓ Success message to student
```

### File Download Flow

```
[User Browser]
   ↓ Clicks "Download Report" button
[Flask Route] /projects/download/<attachment_id>
   ↓ Queries project_attachments table
   ↓ Validates:
     - Attachment exists
     - Project is APPROVED (for public downloads)
     OR
     - User is project author/guide (for private downloads)
[utils/file_handler.py::download_file()]
   ↓ Checks file exists on disk
   ↓ Increments downloads_count in projects table
   ↓ Returns Flask send_file() with:
     - File path
     - Original filename (as_attachment=True)
     - MIME type
[HTTP Response]
   ↓ Browser downloads file
```

### Session Management Flow

```
[User Login]
   ↓ Successful authentication
[Flask Session]
   ↓ Store in session cookie:
     - session['user_id'] = user.user_id
     - session['role'] = user.role
     - session['full_name'] = user.full_name
     - session['department_id'] = user.department_id (if applicable)
   ↓ Cookie signed with SECRET_KEY
   ↓ Cookie sent to browser
[Browser]
   ↓ Stores session cookie
   ↓ Sends cookie with every subsequent request
[Flask @login_required decorator]
   ↓ On each protected route:
     - Checks session['user_id'] exists
     - If missing → redirect to /login
     - If present → continue to route handler
[Flask @role_required('FACULTY') decorator]
   ↓ Checks session['role'] matches required role
     - If mismatch → return 403 Forbidden
     - If match → continue to route handler
```

---

## 7. Search and Filter Flow

### Keyword Search

```
[User] enters search term "machine learning" in search bar
   ↓
[Browser] submits GET request: /projects/browse?q=machine+learning
   ↓
[Flask Route] projects.browse()
   ↓ Extracts query parameter: q='machine learning'
   ↓ Builds SQL query with FULLTEXT search:
     SELECT * FROM projects
     WHERE status='APPROVED'
       AND MATCH(title, abstract) AGAINST ('machine learning' IN NATURAL LANGUAGE MODE)
   ↓ Executes query via utils/database.py
   ↓
[MySQL] returns matching projects sorted by relevance
   ↓
[Flask] renders browse.html with results
   ↓
[Browser] displays matching projects
```

### Department Filter

```
[User] selects "Computer Science" from department dropdown
   ↓
[Browser] submits GET request: /projects/browse?dept=3
   ↓
[Flask Route] projects.browse()
   ↓ Extracts dept parameter
   ↓ Builds SQL query:
     SELECT * FROM projects
     WHERE status='APPROVED' AND department_id=3
   ↓
[MySQL] returns projects from CS department
   ↓
[Browser] displays filtered results
```

### Technology Tag Filter

```
[User] selects "Python" and "Flask" checkboxes
   ↓
[Browser] submits GET request: /projects/browse?tags=Python,Flask
   ↓
[Flask Route] projects.browse()
   ↓ Parses tags parameter → ['Python', 'Flask']
   ↓ Builds SQL query with JOIN:
     SELECT p.* FROM projects p
     JOIN project_tags pt ON p.project_id = pt.project_id
     JOIN tags t ON pt.tag_id = t.tag_id
     WHERE p.status='APPROVED'
       AND t.tag_name IN ('Python', 'Flask')
     GROUP BY p.project_id
     HAVING COUNT(DISTINCT t.tag_id) = 2  -- both tags present
   ↓
[MySQL] returns projects using both Python AND Flask
   ↓
[Browser] displays filtered results
```

---

## 8. Error Handling Flow

### Form Validation Errors

```
[User] submits form with missing required fields
   ↓
[Flask Route] validates input
   ↓ Validation fails (e.g., title is empty)
   ↓ Adds flash message: "Project title is required"
   ↓ Re-renders form with flash message and previous input
   ↓
[Browser] shows error message at top of form, fields pre-filled
```

### File Upload Errors

```
[User] uploads 100MB ZIP file (exceeds 50MB limit)
   ↓
[utils/file_handler.py::upload_file()]
   ↓ Checks file size
   ↓ Size exceeds limit
   ↓ Raises ValueError("File too large")
   ↓
[Flask Route] catches exception
   ↓ Adds flash message: "Source code file exceeds 50MB limit"
   ↓ Re-renders form
   ↓
[Browser] shows error message
```

### HTTP Error Pages

```
[User] navigates to /projects/detail/999999 (non-existent project)
   ↓
[Flask Route] projects.detail(999999)
   ↓ Queries database for project_id=999999
   ↓ Returns None (not found)
   ↓ Calls abort(404)
   ↓
[Flask @app.errorhandler(404)]
   ↓ Renders templates/errors/404.html
   ↓
[Browser] displays custom 404 error page
```

---

## Summary

CampusArchive implements complete workflows for all user types:

- **Public visitors** can browse and discover without friction
- **Students** submit projects and track review progress
- **Faculty** review projects with structured feedback workflow
- **Admins** manage platform configuration and users

Each workflow is designed to match real academic processes, with appropriate access controls, validation, and feedback at every step.

---

**CampusArchive** — Built for the Kiro Buildathon, August 2026
