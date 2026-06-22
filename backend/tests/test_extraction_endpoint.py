from fastapi.testclient import TestClient

from app.main import app


def test_invoice_extraction_endpoint_returns_structured_json() -> None:
    client = TestClient(app)

    response = client.post(
        "/extractions/invoice",
        json={
            "text": "\n".join(
                [
                    "Acme Supplies LLC",
                    "Invoice Number: INV-900",
                    "Invoice Date: 2026-06-01",
                    "Due Date: 2026-06-30",
                    "Subtotal: USD 100.00",
                    "VAT: USD 5.00",
                    "Amount Due: USD 105.00",
                    "billing@acme.example",
                    "+1 555-123-4567",
                ]
            ),
            "source": "pdf_text",
            "ocr_confidence": None,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["extraction_method"] == "rule_based"
    assert data["requires_review"] is True
    assert data["invoice"]["vendor_name"] == "Acme Supplies LLC"
    assert data["invoice"]["invoice_number"] == "INV-900"
    assert data["invoice"]["invoice_date"] == "2026-06-01"
    assert data["invoice"]["due_date"] == "2026-06-30"
    assert data["invoice"]["subtotal"] == 100.0
    assert data["invoice"]["tax"] == 5.0
    assert data["invoice"]["total"] == 105.0
    assert data["invoice"]["currency"] == "USD"
    assert data["invoice"]["email"] == "billing@acme.example"
    assert data["invoice"]["phone"] == "+1 555-123-4567"
    assert data["confidence"]["total"] == 0.95
    assert data["warnings"] == []
