import csv
from io import StringIO
from pathlib import Path

from fastapi.testclient import TestClient

from app.core.config import Settings, get_settings
from app.main import app


def make_client(tmp_path: Path) -> TestClient:
    def override_settings() -> Settings:
        return Settings(
            local_storage_dir=str(tmp_path / "storage"),
            database_url=f"sqlite:///{tmp_path / 'reviews.db'}",
        )

    app.dependency_overrides[get_settings] = override_settings
    return TestClient(app)


def upload_document(client: TestClient) -> str:
    response = client.post(
        "/documents/upload",
        files={"file": ("invoice.pdf", b"%PDF-1.4 sample", "application/pdf")},
    )
    assert response.status_code == 201
    return response.json()["document_id"]


def review_payload(approved: bool = True) -> dict:
    return {
        "invoice": {
            "vendor_name": "ABC Supplies Ltd",
            "invoice_number": "INV-1001",
            "invoice_date": "2026-06-20",
            "due_date": "2026-07-20",
            "subtotal": 100.0,
            "tax": 10.0,
            "total": 110.0,
            "currency": "USD",
            "email": "billing@example.com",
            "phone": "+1 555 123 4567",
            "line_items": [
                {
                    "description": "Reviewed services",
                    "quantity": 1,
                    "unit_price": 100.0,
                    "amount": 100.0,
                }
            ],
        },
        "corrections": {},
        "reviewer_notes": "Approved for export.",
        "approved": approved,
        "original_extraction_method": "rule_based",
    }


def save_review(client: TestClient, document_id: str, approved: bool = True) -> None:
    response = client.post(
        f"/documents/{document_id}/review",
        json=review_payload(approved=approved),
    )
    assert response.status_code == 200


def parse_csv(text: str) -> list[dict[str, str]]:
    return list(csv.DictReader(StringIO(text)))


def test_generic_csv_export_succeeds_for_reviewed_invoice(tmp_path: Path) -> None:
    client = make_client(tmp_path)
    document_id = upload_document(client)
    save_review(client, document_id)

    response = client.get(f"/documents/{document_id}/export?format=generic")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")
    rows = parse_csv(response.text)
    assert rows[0]["document_id"] == document_id
    assert rows[0]["vendor_name"] == "ABC Supplies Ltd"
    assert rows[0]["subtotal"] == "100.00"
    assert rows[0]["tax"] == "10.00"
    assert rows[0]["total"] == "110.00"
    assert rows[0]["status"] == "reviewed"


def test_quickbooks_csv_export_succeeds_for_reviewed_invoice(tmp_path: Path) -> None:
    client = make_client(tmp_path)
    document_id = upload_document(client)
    save_review(client, document_id)

    response = client.get(f"/documents/{document_id}/export?format=quickbooks")

    assert response.status_code == 200
    rows = parse_csv(response.text)
    assert rows[0]["Vendor"] == "ABC Supplies Ltd"
    assert rows[0]["Bill No."] == "INV-1001"
    assert rows[0]["Account"] == "Uncategorized Expense"
    assert rows[0]["Amount"] == "110.00"
    assert rows[0]["Tax Amount"] == "10.00"


def test_xero_csv_export_succeeds_for_reviewed_invoice(tmp_path: Path) -> None:
    client = make_client(tmp_path)
    document_id = upload_document(client)
    save_review(client, document_id)

    response = client.get(f"/documents/{document_id}/export?format=xero")

    assert response.status_code == 200
    rows = parse_csv(response.text)
    assert rows[0]["ContactName"] == "ABC Supplies Ltd"
    assert rows[0]["InvoiceNumber"] == "INV-1001"
    assert rows[0]["Description"] == "Reviewed services"
    assert rows[0]["Quantity"] == "1"
    assert rows[0]["UnitAmount"] == "100.00"
    assert rows[0]["Total"] == "110.00"


def test_review_required_invoice_cannot_be_exported(tmp_path: Path) -> None:
    client = make_client(tmp_path)
    document_id = upload_document(client)
    save_review(client, document_id, approved=False)

    response = client.get(f"/documents/{document_id}/export?format=generic")

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "Invoice must be reviewed and approved before export."
    )


def test_missing_review_returns_safe_404(tmp_path: Path) -> None:
    client = make_client(tmp_path)
    document_id = upload_document(client)

    response = client.get(f"/documents/{document_id}/export?format=generic")

    assert response.status_code == 404
    assert response.json()["detail"] == "Review not found."


def test_unsupported_format_returns_validation_error(tmp_path: Path) -> None:
    client = make_client(tmp_path)
    document_id = upload_document(client)
    save_review(client, document_id)

    response = client.get(f"/documents/{document_id}/export?format=unsupported")

    assert response.status_code == 422


def test_csv_response_includes_headers(tmp_path: Path) -> None:
    client = make_client(tmp_path)
    document_id = upload_document(client)
    save_review(client, document_id)

    response = client.get(f"/documents/{document_id}/export?format=generic")

    assert response.text.splitlines()[0] == (
        "document_id,vendor_name,invoice_number,invoice_date,due_date,"
        "subtotal,tax,total,currency,email,phone,status,reviewed_at,reviewer_notes"
    )


def test_csv_response_includes_safe_content_disposition_filename(
    tmp_path: Path,
) -> None:
    client = make_client(tmp_path)
    document_id = upload_document(client)
    save_review(client, document_id)

    response = client.get(f"/documents/{document_id}/export?format=xero")

    content_disposition = response.headers["content-disposition"]
    assert content_disposition == (
        f'attachment; filename="doculedger_{document_id}_xero.csv"'
    )
    assert "\\" not in content_disposition
    assert "/" not in content_disposition


def test_csv_output_does_not_contain_none_string(tmp_path: Path) -> None:
    client = make_client(tmp_path)
    document_id = upload_document(client)
    payload = review_payload()
    payload["invoice"]["due_date"] = None
    payload["invoice"]["phone"] = None
    payload["reviewer_notes"] = None
    response = client.post(f"/documents/{document_id}/review", json=payload)
    assert response.status_code == 200

    export_response = client.get(f"/documents/{document_id}/export?format=generic")

    assert "None" not in export_response.text


def test_formula_injection_values_are_sanitized(tmp_path: Path) -> None:
    client = make_client(tmp_path)
    document_id = upload_document(client)
    payload = review_payload()
    payload["invoice"]["vendor_name"] = "=Malicious Vendor"
    payload["invoice"]["invoice_number"] = "+INV-1001"
    payload["invoice"]["email"] = "@billing.example"
    payload["invoice"]["phone"] = "-15551234567"
    payload["reviewer_notes"] = "=Do not execute"
    response = client.post(f"/documents/{document_id}/review", json=payload)
    assert response.status_code == 200

    export_response = client.get(f"/documents/{document_id}/export?format=generic")
    rows = parse_csv(export_response.text)

    assert rows[0]["vendor_name"] == "'=Malicious Vendor"
    assert rows[0]["invoice_number"] == "'+INV-1001"
    assert rows[0]["email"] == "'@billing.example"
    assert rows[0]["phone"] == "'-15551234567"
    assert rows[0]["reviewer_notes"] == "'=Do not execute"


def test_export_response_does_not_expose_absolute_paths(tmp_path: Path) -> None:
    client = make_client(tmp_path)
    document_id = upload_document(client)
    save_review(client, document_id)

    response = client.get(f"/documents/{document_id}/export?format=generic")

    assert str(tmp_path) not in response.text
    assert "reviews.db" not in response.text
    assert str(tmp_path) not in response.headers["content-disposition"]


def teardown_function() -> None:
    app.dependency_overrides.clear()
