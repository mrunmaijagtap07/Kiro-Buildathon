"""
init_db.py — Initialize the CampusArchive database.

Run this once (or whenever you need to reset):
    python init_db.py

What it does:
  1. Reads database credentials from .env
  2. Creates/refreshes the schema (schema.sql)
  3. Seeds reference data (seed.sql)
  4. Creates an admin account from ADMIN_EMAIL / ADMIN_PASSWORD in .env

Admin credentials must be set in .env:
    ADMIN_EMAIL=admin@example.com
    ADMIN_PASSWORD=your_secure_password
    ADMIN_NAME=System Administrator
"""

import os
import sys
import pymysql
from pathlib import Path
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

load_dotenv()

DB_HOST     = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT     = int(os.getenv("DB_PORT", "3306"))
DB_NAME     = os.getenv("DB_NAME", "campus_repository")
DB_USER     = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

ADMIN_EMAIL    = os.getenv("ADMIN_EMAIL", "")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "")
ADMIN_NAME     = os.getenv("ADMIN_NAME", "System Administrator")




def run_sql_file(cursor, path: Path) -> None:
    """Execute every SQL statement in a .sql file, ignoring comments safely."""
    sql = path.read_text(encoding="utf-8")

    # Remove SQL single-line comments before splitting statements.
    lines = []
    for line in sql.splitlines():
        stripped = line.strip()
        if stripped.startswith("--"):
            continue
        lines.append(line)

    sql = "\n".join(lines)

    # Split remaining SQL statements on semicolons.
    statements = [s.strip() for s in sql.split(";") if s.strip()]

    for stmt in statements:
        try:
            cursor.execute(stmt)
        except pymysql.err.Warning:
            pass  # Ignore non-fatal warnings


def main():
    print("=" * 60)
    print("CampusArchive — Database Initializer")
    print("=" * 60)

    # ── Connect ────────────────────────────────────────────────
    try:
        conn = pymysql.connect(
            host=DB_HOST, port=DB_PORT,
            user=DB_USER, password=DB_PASSWORD,
            charset="utf8mb4", autocommit=True,
        )
        print(f"✓ Connected to MySQL at {DB_HOST}:{DB_PORT}")
    except pymysql.Error as e:
        print(f"✗ Cannot connect to MySQL: {e}")
        print("\nTroubleshooting:")
        print("  1. Is MySQL running?  → Run: net start MySQL80  (or your service name)")
        print("  2. Check DB_HOST, DB_PORT, DB_USER, DB_PASSWORD in your .env file.")
        sys.exit(1)

    base_dir = Path(__file__).parent

    with conn.cursor() as cursor:
        # ── Schema ─────────────────────────────────────────────
        print("\n→ Applying schema.sql …")
        run_sql_file(cursor, base_dir / "database" / "schema.sql")
        print("  ✓ Schema applied.")

        # ── Seed data ──────────────────────────────────────────
        print("→ Applying seed.sql …")
        run_sql_file(cursor, base_dir / "database" / "seed.sql")
        print("  ✓ Seed data applied.")

        # ── Admin account ──────────────────────────────────────
        if not ADMIN_EMAIL or not ADMIN_PASSWORD:
            print(
                "\n⚠  Admin account NOT created.\n"
                "   Add these to your .env to create one:\n"
                "     ADMIN_EMAIL=you@example.com\n"
                "     ADMIN_PASSWORD=YourSecurePassword\n"
                "     ADMIN_NAME=Your Name"
            )
        else:
            cursor.execute("USE campus_repository")
            existing = None
            cursor.execute("SELECT user_id FROM users WHERE email=%s", (ADMIN_EMAIL.lower(),))
            existing = cursor.fetchone()

            if existing:
                print(f"\n→ Admin account already exists for {ADMIN_EMAIL} — skipping.")
            else:
                # Use department_id=1 (IT) as default — admin doesn't really need a dept
                cursor.execute("SELECT department_id FROM departments LIMIT 1")
                dept = cursor.fetchone()
                dept_id = dept["department_id"] if isinstance(dept, dict) else dept[0]

                pw_hash = generate_password_hash(ADMIN_PASSWORD)
                cursor.execute(
                    """INSERT INTO users (full_name, email, password_hash, role, department_id, auth_provider)
                       VALUES (%s, %s, %s, 'ADMIN', %s, 'LOCAL')""",
                    (ADMIN_NAME, ADMIN_EMAIL.lower(), pw_hash, dept_id)
                )
                print(f"\n  ✓ Admin account created: {ADMIN_EMAIL}")

    conn.close()

    print("\n" + "=" * 60)
    print("Database initialization complete.")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Copy .env.example to .env and fill in your values.")
    print("  2. Run: python app.py")
    print("  3. Open: http://127.0.0.1:5000")


if __name__ == "__main__":
    main()
