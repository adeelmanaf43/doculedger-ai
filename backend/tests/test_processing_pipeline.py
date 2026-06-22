from io import BytesIO
from pathlib import Path
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from PIL import Image

from app.core.config import Settings, get_settings
from app.main import app


def make_client(storage_dir: Path) -> TestClient:
    def override_settings() -> Settings:
        return Settings(local_storage_dir=str(storage_dir))

    app.dependency_overrides[get_settings] = override_settings
    return TestClient(app)


def test_process_uploaded_text_pdf_returns_structured_invoice(tmp_path: Path) -> None:
    client = make_client(tmp_path)
    pdf_bytes = build_text_pdf(
        "\n".join(
            [
                "Acme Supplies LLC",
                "Invoice Number: INV-321",
                "Invoice Date: 2026-06-01",
                "Subtotal: $100.00",
                "Tax: $8.00",
                "Amount Due: $108.00",
            ]
        )
    )

    upload_response = client.post(
        "/documents/upload",
        files={"file": ("invoice.pdf", pdf_bytes, "application/pdf")},
    )
    document_id = upload_response.json()["document_id"]

    response = client.post(
        f"/documents/{document_id}/process",
        json={"include_text_preview": True},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["document_id"] == document_id
    assert data["status"] == "review_required"
    assert data["requires_review"] is True
    assert data["processing"]["text_extraction_method"] == "pdf_text"
    assert data["processing"]["invoice_extraction_method"] == "rule_based"
    assert data["processing"]["page_count"] == 1
    assert data["processing"]["text_length"] > 0
    assert data["invoice"]["vendor_name"] == "Acme Supplies LLC"
    assert data["invoice"]["invoice_number"] == "INV-321"
    assert data["invoice"]["total"] == 108.0
    assert data["confidence"]["total"] == 0.95
    assert data["text_preview"]
    assert len(data["text_preview"]) <= 400
    assert not Path(data["text_preview"]).is_absolute()


def test_process_uploaded_image_uses_ocr_and_returns_invoice(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    client = make_client(tmp_path)
    monkeypatch.setattr(
        "app.services.ocr.tesseract_ocr.pytesseract.image_to_data",
        lambda image, output_type: {
            "text": [
                "Acme",
                "Supplies",
                "LLC",
                "Invoice",
                "Number:",
                "IMG-9",
                "Invoice",
                "Date:",
                "2026-06-01",
                "Total:",
                "$42.00",
            ],
            "conf": ["92", "92", "92", "90", "90", "90", "90", "90", "90", "88", "88"],
        },
    )

    upload_response = client.post(
        "/documents/upload",
        files={"file": ("receipt.png", build_png_bytes(), "image/png")},
    )
    document_id = upload_response.json()["document_id"]

    response = client.post(
        f"/documents/{document_id}/process",
        json={"include_text_preview": False},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["processing"]["text_extraction_method"] == "tesseract_ocr"
    assert data["invoice"]["invoice_number"] == "IMG-9"
    assert data["invoice"]["total"] == 42.0
    assert data["requires_review"] is True
    assert data["text_preview"] is None


def test_process_missing_document_returns_safe_404(tmp_path: Path) -> None:
    client = make_client(tmp_path)

    response = client.post("/documents/00000000-0000-0000-0000-000000000000/process")

    assert response.status_code == 404
    assert response.json()["detail"] == "Document not found."


def test_process_unsupported_document_type_returns_safe_error(tmp_path: Path) -> None:
    client = make_client(tmp_path)
    document_id = str(uuid4())
    document_dir = tmp_path / document_id
    document_dir.mkdir()
    (document_dir / "document.txt").write_text("not supported", encoding="utf-8")

    response = client.post(f"/documents/{document_id}/process")

    assert response.status_code == 400
    assert response.json()["detail"] == "Document type is not supported for processing."


def test_process_empty_pdf_text_returns_scanned_pdf_warning(tmp_path: Path) -> None:
    client = make_client(tmp_path)

    upload_response = client.post(
        "/documents/upload",
        files={"file": ("blank.pdf", build_blank_pdf(), "application/pdf")},
    )
    document_id = upload_response.json()["document_id"]

    response = client.post(f"/documents/{document_id}/process")

    assert response.status_code == 200
    data = response.json()
    assert data["processing"]["text_extraction_method"] == "unsupported_scanned_pdf"
    warning_codes = {warning["code"] for warning in data["warnings"]}
    assert "scanned_pdf_not_supported_yet" in warning_codes
    assert "empty_extracted_text" in warning_codes
    assert data["requires_review"] is True


def test_process_response_does_not_return_full_raw_text_by_default(tmp_path: Path) -> None:
    client = make_client(tmp_path)
    long_text = "Acme Supplies LLC\nInvoice Number: LONG-1\nTotal: $10.00\n" + ("x" * 700)

    upload_response = client.post(
        "/documents/upload",
        files={"file": ("invoice.pdf", build_text_pdf(long_text), "application/pdf")},
    )
    document_id = upload_response.json()["document_id"]

    response = client.post(f"/documents/{document_id}/process")

    assert response.status_code == 200
    data = response.json()
    assert data["processing"]["text_length"] > 400
    assert len(data["text_preview"]) == 400
    assert long_text not in str(data)


def build_png_bytes() -> bytes:
    output = BytesIO()
    image = Image.new("RGB", (240, 80), "white")
    image.save(output, format="PNG")
    return output.getvalue()


def build_text_pdf(text: str) -> bytes:
    escaped_text = text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    content = f"BT /F1 12 Tf 72 720 Td ({escaped_text}) Tj ET"
    return build_pdf_with_content(content)


def build_blank_pdf() -> bytes:
    return build_pdf_with_content("")


def build_pdf_with_content(content: str) -> bytes:
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
