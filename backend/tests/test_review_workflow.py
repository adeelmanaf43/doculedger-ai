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


def valid_review_payload(approved: bool = True) -> dict:
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
            "line_items": [],
        },
        "corrections": {
            "vendor_name": {
                "original": "ABC Supplles",
                "corrected": "ABC Supplies Ltd",
            },
            "total": {
                "original": 100.0,
                "corrected": 110.0,
            },
        },
        "reviewer_notes": "Corrected vendor name and total.",
        "approved": approved,
        "original_extraction_method": "rule_based",
    }


def test_save_reviewed_invoice_successfully(tmp_path: Path) -> None:
    client = make_client(tmp_path)
    document_id = upload_document(client)

    response = client.post(
        f"/documents/{document_id}/review",
        json=valid_review_payload(),
    )

    assert response.status_code == 200
    data = response.json()
    assert data["document_id"] == document_id
    assert data["status"] == "reviewed"
    assert data["requires_review"] is False
    assert data["reviewed_invoice"]["vendor_name"] == "ABC Supplies Ltd"
    assert data["message"] == "Reviewed invoice saved successfully."


def test_retrieve_reviewed_invoice_successfully(tmp_path: Path) -> None:
    client = make_client(tmp_path)
    document_id = upload_document(client)
    client.post(f"/documents/{document_id}/review", json=valid_review_payload())

    response = client.get(f"/documents/{document_id}/review")

    assert response.status_code == 200
    data = response.json()
    assert data["reviewed_invoice"]["invoice_number"] == "INV-1001"
    assert data["status"] == "reviewed"


def test_approved_true_returns_reviewed_status(tmp_path: Path) -> None:
    client = make_client(tmp_path)
    document_id = upload_document(client)

    response = client.post(
        f"/documents/{document_id}/review",
        json=valid_review_payload(approved=True),
    )
    status_response = client.get(f"/documents/{document_id}/status")

    assert response.json()["status"] == "reviewed"
    assert response.json()["requires_review"] is False
    assert status_response.json()["status"] == "reviewed"
    assert status_response.json()["requires_review"] is False


def test_approved_false_returns_review_required_status(tmp_path: Path) -> None:
    client = make_client(tmp_path)
    document_id = upload_document(client)

    response = client.post(
        f"/documents/{document_id}/review",
        json=valid_review_payload(approved=False),
    )
    status_response = client.get(f"/documents/{document_id}/status")

    assert response.json()["status"] == "review_required"
    assert response.json()["requires_review"] is True
    assert status_response.json()["status"] == "review_required"
    assert status_response.json()["requires_review"] is True


def test_missing_document_returns_safe_404(tmp_path: Path) -> None:
    client = make_client(tmp_path)

    response = client.post(
        "/documents/00000000-0000-0000-0000-000000000000/review",
        json=valid_review_payload(),
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Document not found."


def test_missing_review_returns_safe_404(tmp_path: Path) -> None:
    client = make_client(tmp_path)
    document_id = upload_document(client)

    response = client.get(f"/documents/{document_id}/review")

    assert response.status_code == 404
    assert response.json()["detail"] == "Review not found."


def test_invalid_invoice_payload_returns_validation_error(tmp_path: Path) -> None:
    client = make_client(tmp_path)
    document_id = upload_document(client)
    payload = valid_review_payload()
    payload["invoice"] = {"total": "not-a-number"}

    response = client.post(f"/documents/{document_id}/review", json=payload)

    assert response.status_code == 422


def test_corrections_are_saved(tmp_path: Path) -> None:
    client = make_client(tmp_path)
    document_id = upload_document(client)

    response = client.post(
        f"/documents/{document_id}/review",
        json=valid_review_payload(),
    )

    data = response.json()
    assert data["corrected_fields"] == ["total", "vendor_name"]
    assert data["corrections"]["vendor_name"]["corrected"] == "ABC Supplies Ltd"
    assert data["corrections"]["total"]["corrected"] == 110.0


def test_reviewer_notes_are_saved(tmp_path: Path) -> None:
    client = make_client(tmp_path)
    document_id = upload_document(client)

    client.post(f"/documents/{document_id}/review", json=valid_review_payload())
    response = client.get(f"/documents/{document_id}/review")

    assert response.json()["reviewer_notes"] == "Corrected vendor name and total."


def test_review_response_does_not_expose_absolute_file_paths(tmp_path: Path) -> None:
    client = make_client(tmp_path)
    document_id = upload_document(client)

    response = client.post(
        f"/documents/{document_id}/review",
        json=valid_review_payload(),
    )

    assert response.status_code == 200
    response_text = response.text
    assert str(tmp_path) not in response_text
    assert "reviews.db" not in response_text


def teardown_function() -> None:
    app.dependency_overrides.clear()
