from io import BytesIO
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from PIL import Image

from app.core.config import Settings, get_settings
from app.main import app
from app.services.ocr.tesseract_ocr import OcrError, TesseractOcrProvider
from app.services.storage.local_storage import StoredDocumentRef


def make_client(storage_dir: Path) -> TestClient:
    def override_settings() -> Settings:
        return Settings(local_storage_dir=str(storage_dir))

    app.dependency_overrides[get_settings] = override_settings
    return TestClient(app)


def test_ocr_image_upload_returns_text(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = make_client(tmp_path)
    monkeypatch.setattr(
        "app.services.ocr.tesseract_ocr.pytesseract.image_to_data",
        lambda image, output_type: {
            "text": ["", "Invoice", "Total", "42.00"],
            "conf": ["-1", "96", "94", "86"],
        },
    )

    upload_response = client.post(
        "/documents/upload",
        files={"file": ("receipt.png", build_png_bytes(), "image/png")},
    )
    assert upload_response.status_code == 201
    document_id = upload_response.json()["document_id"]

    response = client.post(f"/documents/{document_id}/ocr")

    assert response.status_code == 200
    data = response.json()
    assert data["document_id"] == document_id
    assert data["page_count"] == 1
    assert data["extracted_text"] == "Invoice Total 42.00"
    assert data["per_page_text"] == [
        {"page_number": 1, "text": "Invoice Total 42.00"}
    ]
    assert data["extraction_method"] == "tesseract_ocr"
    assert data["confidence"] == 92.0
    assert data["warnings"] == []
    assert Path(data["storage_key"]).is_absolute() is False


def test_ocr_pdf_returns_scanned_pdf_limitation(tmp_path: Path) -> None:
    client = make_client(tmp_path)

    upload_response = client.post(
        "/documents/upload",
        files={"file": ("scan.pdf", b"%PDF-1.4 scanned placeholder", "application/pdf")},
    )
    assert upload_response.status_code == 201
    document_id = upload_response.json()["document_id"]

    response = client.post(f"/documents/{document_id}/ocr")

    assert response.status_code == 200
    data = response.json()
    assert data["document_id"] == document_id
    assert data["extracted_text"] == ""
    assert data["confidence"] is None
    assert data["extraction_method"] == "tesseract_ocr"
    assert "PDF-to-image conversion" in data["warnings"][0]


def test_ocr_unsupported_file_type_is_rejected(tmp_path: Path) -> None:
    unsupported_path = tmp_path / "document.txt"
    unsupported_path.write_text("not an image", encoding="utf-8")
    document = StoredDocumentRef(
        document_id="00000000-0000-0000-0000-000000000001",
        storage_key="00000000-0000-0000-0000-000000000001/document.txt",
        path=unsupported_path,
        safe_filename="document.txt",
        content_type="text/plain",
    )
    provider = TesseractOcrProvider(Settings())

    with pytest.raises(OcrError) as error:
        provider.extract(document)

    assert error.value.status_code == 400
    assert "OCR currently supports" in error.value.detail


def test_ocr_missing_document_returns_safe_error(tmp_path: Path) -> None:
    client = make_client(tmp_path)

    response = client.post("/documents/00000000-0000-0000-0000-000000000000/ocr")

    assert response.status_code == 404
    assert response.json()["detail"] == "Document not found."


def build_png_bytes() -> bytes:
    output = BytesIO()
    image = Image.new("RGB", (240, 80), "white")
    image.save(output, format="PNG")
    return output.getvalue()


def teardown_function() -> None:
    app.dependency_overrides.clear()
