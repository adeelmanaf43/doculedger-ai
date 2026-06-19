from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.core.config import Settings, get_settings
from app.main import app


def make_client(storage_dir: Path, max_upload_mb: int = 10) -> TestClient:
    def override_settings() -> Settings:
        return Settings(
            local_storage_dir=str(storage_dir),
            max_upload_mb=max_upload_mb,
        )

    app.dependency_overrides[get_settings] = override_settings
    return TestClient(app)


def test_valid_pdf_upload_is_stored(tmp_path: Path) -> None:
    client = make_client(tmp_path)

    response = client.post(
        "/documents/upload",
        files={"file": ("invoice.pdf", b"%PDF-1.4 sample", "application/pdf")},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["original_filename"] == "invoice.pdf"
    assert data["safe_filename"].endswith("_invoice.pdf")
    assert data["content_type"] == "application/pdf"
    assert data["size_bytes"] == len(b"%PDF-1.4 sample")
    assert data["status"] == "uploaded"
    assert Path(tmp_path, data["storage_key"]).exists()
    assert Path(data["storage_key"]).is_absolute() is False


@pytest.mark.parametrize(
    ("filename", "content", "content_type"),
    [
        ("receipt.png", b"\x89PNG sample", "image/png"),
        ("receipt.jpg", b"\xff\xd8 sample", "image/jpeg"),
        ("receipt.jpeg", b"\xff\xd8 sample", "image/jpeg"),
    ],
)
def test_valid_image_upload_is_stored(
    tmp_path: Path,
    filename: str,
    content: bytes,
    content_type: str,
) -> None:
    client = make_client(tmp_path)

    response = client.post(
        "/documents/upload",
        files={"file": (filename, content, content_type)},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["safe_filename"].endswith(f"_{filename}")
    assert data["content_type"] == content_type
    assert Path(tmp_path, data["storage_key"]).exists()


def test_unsupported_file_type_is_rejected(tmp_path: Path) -> None:
    client = make_client(tmp_path)

    response = client.post(
        "/documents/upload",
        files={"file": ("script.exe", b"not an invoice", "application/octet-stream")},
    )

    assert response.status_code == 400
    assert "Unsupported file type" in response.json()["detail"]


def test_oversized_file_is_rejected(tmp_path: Path) -> None:
    client = make_client(tmp_path, max_upload_mb=1)

    response = client.post(
        "/documents/upload",
        files={"file": ("large.pdf", b"x" * (1024 * 1024 + 1), "application/pdf")},
    )

    assert response.status_code == 413
    assert "upload limit" in response.json()["detail"]
    assert list(tmp_path.rglob("*")) == []


def test_dangerous_filename_is_sanitized(tmp_path: Path) -> None:
    client = make_client(tmp_path)

    response = client.post(
        "/documents/upload",
        files={
            "file": (
                "..\\..\\evil invoice.pdf",
                b"%PDF-1.4 sample",
                "application/pdf",
            )
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["original_filename"] == "..\\..\\evil invoice.pdf"
    assert ".." not in data["safe_filename"]
    assert "\\" not in data["safe_filename"]
    assert "/" not in data["safe_filename"]
    assert data["safe_filename"].endswith("_evil_invoice.pdf")
    assert Path(tmp_path, data["storage_key"]).exists()


def teardown_function() -> None:
    app.dependency_overrides.clear()
