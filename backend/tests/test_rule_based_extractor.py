from app.schemas.invoice import InvoiceExtractionRequest
from app.services.extractors.rule_based import RuleBasedInvoiceExtractor


def extract(text: str) -> dict:
    request = InvoiceExtractionRequest(text=text, source="pdf_text")
    response = RuleBasedInvoiceExtractor().extract(request)
    return response.model_dump()


def test_extracts_invoice_number_from_common_labels() -> None:
    result = extract(
        """
        Acme Supplies LLC
        Invoice No: INV-1001
        Invoice Date: 2026-06-01
        Total: $125.00
        """
    )

    assert result["invoice"]["invoice_number"] == "INV-1001"
    assert result["confidence"]["invoice_number"] == 0.95


def test_extracts_invoice_date_and_due_date() -> None:
    result = extract(
        """
        Acme Supplies LLC
        Invoice Number: A-42
        Invoice Date: June 1, 2026
        Due Date: 2026-06-30
        Total: USD 200.00
        """
    )

    assert result["invoice"]["invoice_date"] == "2026-06-01"
    assert result["invoice"]["due_date"] == "2026-06-30"


def test_extracts_subtotal_tax_total_and_currency() -> None:
    result = extract(
        """
        Acme Supplies LLC
        Invoice #: INV-200
        Date: 2026-06-01
        Subtotal: $100.00
        Sales Tax: $8.00
        Grand Total: $108.00
        """
    )

    invoice = result["invoice"]
    assert invoice["subtotal"] == 100.0
    assert invoice["tax"] == 8.0
    assert invoice["total"] == 108.0
    assert invoice["currency"] == "USD"
    assert "subtotal/tax/total mismatch" not in result["warnings"]


def test_creates_warnings_for_missing_fields() -> None:
    result = extract("Thank you for your business")

    assert "missing invoice number" in result["warnings"]
    assert "missing date" in result["warnings"]
    assert "missing total" in result["warnings"]
    assert result["requires_review"] is True


def test_handles_empty_text_safely() -> None:
    result = extract("")

    assert result["invoice"]["vendor_name"] is None
    assert "empty or very short extracted text" in result["warnings"]
    assert "missing vendor" in result["warnings"]
    assert result["extraction_method"] == "rule_based"


def test_detects_ambiguous_date_and_total_mismatch() -> None:
    result = extract(
        """
        Acme Supplies LLC
        Invoice No: INV-300
        Invoice Date: 03/04/2026
        Subtotal: $100.00
        Tax: $10.00
        Total: $105.00
        """
    )

    assert "ambiguous date" in result["warnings"]
    assert "subtotal/tax/total mismatch" in result["warnings"]


def test_extracts_basic_line_item_draft() -> None:
    result = extract(
        """
        Acme Supplies LLC
        Invoice No: INV-400
        Invoice Date: 2026-06-01
        Consulting Services 2 50.00 100.00
        Total: $100.00
        """
    )

    assert result["invoice"]["line_items"] == [
        {
            "description": "Consulting Services",
            "quantity": 2.0,
            "unit_price": 50.0,
            "amount": 100.0,
        }
    ]
