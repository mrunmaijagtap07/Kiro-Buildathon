#!/usr/bin/env python
"""
smoke_test.py — Quick smoke test to verify the app structure.
Doesn't require MySQL — just imports and checks the app can be created.

Run with:  python smoke_test.py
"""

import sys
import os

def main():
    print("=" * 60)
    print("CampusArchive — Smoke Test")
    print("=" * 60)
    
    errors = []
    
    # 1. Check .env exists
    print("\n[1/7] Checking .env file...")
    if os.path.exists(".env"):
        print("  [OK] .env found")
    else:
        print("  [FAIL] .env NOT found -- copy .env.example to .env and fill in values")
        errors.append(".env missing")
    
    # 2. Import config
    print("\n[2/7] Importing config...")
    try:
        from config import ActiveConfig
        print(f"  [OK] Config loaded (FLASK_ENV={os.getenv('FLASK_ENV', 'development')})")
    except Exception as e:
        print(f"  ✗ Config import failed: {e}")
        errors.append("config import")
    
    # 3. Import utils
    print("\n[3/7] Importing utils...")
    try:
        from utils.database import get_db
        from utils.decorators import login_required
        from utils.file_handler import save_upload
        from utils.validators import validate_registration
        from utils.helpers import academic_year_choices
        print("  ✓ All utils imported successfully")
    except Exception as e:
        print(f"  ✗ Utils import failed: {e}")
        errors.append("utils import")
    
    # 4. Import routes
    print("\n[4/7] Importing routes...")
    try:
        from routes.auth import auth_bp
        from routes.student import student_bp
        from routes.faculty import faculty_bp
        from routes.admin import admin_bp
        from routes.projects import projects_bp
        print("  ✓ All routes imported successfully")
    except Exception as e:
        print(f"  ✗ Routes import failed: {e}")
        errors.append("routes import")
    
    # 5. Create Flask app
    print("\n[5/7] Creating Flask app...")
    try:
        from app import create_app
        app = create_app()
        print(f"  ✓ Flask app created")
        print(f"    Blueprints: {sorted(app.blueprints.keys())}")
        print(f"    Routes: {len(list(app.url_map.iter_rules()))}")
    except Exception as e:
        print(f"  ✗ App creation failed: {e}")
        errors.append("app creation")
    
    # 6. Check uploads/ directory
    print("\n[6/7] Checking uploads directory...")
    if os.path.exists("uploads/reports") and os.path.exists("uploads/source"):
        print("  ✓ Upload directories exist")
    else:
        print("  ⚠ Upload directories missing (they'll be created on first run)")
    
    # 7. Check database schema
    print("\n[7/7] Checking database schema file...")
    if os.path.exists("database/schema.sql"):
        print("  ✓ schema.sql found")
    else:
        print("  ✗ database/schema.sql NOT found")
        errors.append("schema.sql missing")
    
    # Summary
    print("\n" + "=" * 60)
    if errors:
        print(f"❌ Smoke test FAILED ({len(errors)} error{'s' if len(errors) != 1 else ''})")
        for e in errors:
            print(f"   - {e}")
        print("\nFix the errors above, then run: python app.py")
        return 1
    else:
        print("✅ Smoke test PASSED — all core components OK")
        print("\nNext steps:")
        print("  1. Ensure MySQL is running")
        print("  2. Update DB credentials in .env")
        print("  3. Run: python init_db.py")
        print("  4. Run: python app.py")
        print("  5. Open: http://127.0.0.1:5000")
        return 0

if __name__ == "__main__":
    sys.exit(main())
