"""
tests/test_uploads.py — File upload validation tests.
These test the utils/file_handler.py logic using a real
temporary Flask app context.

Run with:  python -m pytest tests/test_uploads.py -v
"""

import pytest
import io
import os
import sys
import tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app import create_app
from config import Config
from utils.file_handler import FileValidationError


class TestConfig(Config):
    TESTING = True
    SECRET_KEY = "test-key"
    MAX_REPORT_SIZE_MB = 1
    MAX_SOURCE_SIZE_MB = 2
    MAX_DIAGRAM_SIZE_MB = 1


def make_file(content: bytes, filename: str):
    """Create a werkzeug FileStorage-like object."""
    from werkzeug.datastructures import FileStorage
    return FileStorage(
        stream=io.BytesIO(content),
        filename=filename,
        content_type="application/octet-stream",
    )


@pytest.fixture
def app_ctx():
    """Provide a Flask app context with a temp upload dir."""
    with tempfile.TemporaryDirectory() as tmpdir:
        cfg = TestConfig()
        cfg.UPLOAD_FOLDER = tmpdir
        application = create_app(cfg)
        with application.app_context():
            # Create subdirectories
            for sub in ("reports", "source", "diagrams"):
                os.makedirs(os.path.join(tmpdir, sub), exist_ok=True)
            yield application


class TestFileValidation:

    def test_valid_pdf_accepted(self, app_ctx):
        from utils.file_handler import save_upload
        f = make_file(b"%PDF-1.4 fake pdf content", "report.pdf")
        result = save_upload(f, "REPORT_PDF")
        assert result["original_name"] == "report.pdf"
        assert result["file_size_bytes"] > 0
        assert result["file_hash"] is not None
        assert result["stored_file_path"].startswith("reports/")

    def test_valid_zip_accepted(self, app_ctx):
        from utils.file_handler import save_upload
        # Minimal valid zip magic bytes
        zip_content = b"PK\x03\x04" + b"\x00" * 20
        f = make_file(zip_content, "source.zip")
        result = save_upload(f, "SOURCE_ZIP")
        assert result["stored_file_path"].startswith("source/")

    def test_wrong_extension_rejected(self, app_ctx):
        from utils.file_handler import save_upload
        f = make_file(b"some content", "report.docx")
        with pytest.raises(FileValidationError) as exc:
            save_upload(f, "REPORT_PDF")
        assert "pdf" in str(exc.value).lower()

    def test_zip_extension_required_for_source(self, app_ctx):
        from utils.file_handler import save_upload
        f = make_file(b"some content", "source.tar.gz")
        with pytest.raises(FileValidationError):
            save_upload(f, "SOURCE_ZIP")

    def test_empty_file_rejected(self, app_ctx):
        from utils.file_handler import save_upload
        f = make_file(b"", "empty.pdf")
        with pytest.raises(FileValidationError) as exc:
            save_upload(f, "REPORT_PDF")
        assert "empty" in str(exc.value).lower()

    def test_oversized_file_rejected(self, app_ctx):
        from utils.file_handler import save_upload
        # 1 MB limit in TestConfig, send 1.1 MB
        big_content = b"A" * (1024 * 1024 + 100)
        f = make_file(big_content, "big.pdf")
        with pytest.raises(FileValidationError) as exc:
            save_upload(f, "REPORT_PDF")
        assert "too large" in str(exc.value).lower()

    def test_no_filename_rejected(self, app_ctx):
        from utils.file_handler import save_upload
        f = make_file(b"content", "")
        with pytest.raises(FileValidationError):
            save_upload(f, "REPORT_PDF")

    def test_path_traversal_blocked(self, app_ctx):
        from utils.file_handler import get_absolute_path
        with pytest.raises(ValueError):
            get_absolute_path("../../etc/passwd")

    def test_diagram_accepts_png(self, app_ctx):
        from utils.file_handler import save_upload
        # PNG magic bytes
        png_content = b"\x89PNG\r\n\x1a\n" + b"\x00" * 20
        f = make_file(png_content, "diagram.png")
        result = save_upload(f, "DIAGRAM")
        assert result["stored_file_path"].startswith("diagrams/")

    def test_stored_filename_differs_from_original(self, app_ctx):
        """Verify we never use the original filename as storage name."""
        from utils.file_handler import save_upload
        f = make_file(b"%PDF-1.4 content", "my_report.pdf")
        result = save_upload(f, "REPORT_PDF")
        stored = os.path.basename(result["stored_file_path"])
        assert stored != "my_report.pdf"

    def test_sha256_hash_computed(self, app_ctx):
        from utils.file_handler import save_upload
        import hashlib
        content = b"%PDF-1.4 deterministic content"
        expected = hashlib.sha256(content).hexdigest()
        f = make_file(content, "test.pdf")
        result = save_upload(f, "REPORT_PDF")
        assert result["file_hash"] == expected
