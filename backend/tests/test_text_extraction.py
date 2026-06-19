from pathlib import Path

from fastapi.testclient import TestClient

from app.core.config import Settings, get_settings
from app.main import app


def make_client(storage_dir: Path) -> TestClient:
    def override_settings() -> Settings:
        return Settings(local_storage_dir=str(storage_dir))

    app.dependency_overrides[get_settings] = override_settings
    return TestClient(app)


def test_extract_text_from_uploaded_pdf(tmp_path: Path) -> None:
    client = make_client(tmp_path)
    pdf_bytes = build_text_pdf("DocuLedger Invoice Total 123.45")

    upload_response = client.post(
        "/documents/upload",
        files={"file": ("invoice.pdf", pdf_bytes, "application/pdf")},
    )
    assert upload_response.status_code == 201
    document_id = upload_response.json()["document_id"]

    response = client.post(f"/documents/{document_id}/extract-text")

    assert response.status_code == 200
    data = response.json()
    assert data["document_id"] == document_id
    assert data["page_count"] == 1
    assert "DocuLedger Invoice Total 123.45" in data["extracted_text"]
    assert data["per_page_text"][0]["page_number"] == 1
    assert "DocuLedger Invoice Total 123.45" in data["per_page_text"][0]["text"]
    assert data["extraction_method"] == "pdf_text"
    assert data["warnings"] == []
    assert Path(data["storage_key"]).is_absolute() is False


def test_extract_text_rejects_non_pdf_document(tmp_path: Path) -> None:
    client = make_client(tmp_path)

    upload_response = client.post(
        "/documents/upload",
        files={"file": ("receipt.png", b"\x89PNG sample", "image/png")},
    )
    assert upload_response.status_code == 201
    document_id = upload_response.json()["document_id"]

    response = client.post(f"/documents/{document_id}/extract-text")

    assert response.status_code == 400
    assert "text-based PDF" in response.json()["detail"]


def test_extract_text_missing_document_returns_safe_error(tmp_path: Path) -> None:
    client = make_client(tmp_path)

    response = client.post(
        "/documents/00000000-0000-0000-0000-000000000000/extract-text"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Document not found."


def build_text_pdf(text: str) -> bytes:
    escaped_text = (
        text.replace("\\", "\\\\")
        .replace("(", "\\(")
        .replace(")", "\\)")
    )
    content = f"BT /F1 12 Tf 72 720 Td ({escaped_text}) Tj ET"
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        (
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            b"/Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>"
        ),
        (
            f"<< /Length {len(content.encode('latin-1'))} >>\nstream\n"
            f"{content}\nendstream"
        ).encode("latin-1"),
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]

    output = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for index, obj in enumerate(objects, start=1):
        offsets.append(len(output))
        output.extend(f"{index} 0 obj\n".encode("ascii"))
        output.extend(obj)
        output.extend(b"\nendobj\n")

    xref_offset = len(output)
    output.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    output.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        output.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    output.extend(
        (
            f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref_offset}\n%%EOF\n"
        ).encode("ascii")
    )
    return bytes(output)


def teardown_function() -> None:
    app.dependency_overrides.clear()
