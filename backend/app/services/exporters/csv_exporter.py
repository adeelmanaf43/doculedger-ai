import csv
from io import StringIO
from typing import Any

from app.schemas.export import CSVExportResult, ExportFormat


CSV_CONTENT_TYPE = "text/csv; charset=utf-8"
FORMULA_PREFIXES = ("=", "+", "-", "@")


class CSVExporter:
    def export_reviewed_invoice(
        self,
        *,
        document_id: str,
        reviewed_invoice: dict[str, Any],
        status: str,
        approved: bool,
        reviewed_at: str,
        reviewer_notes: str | None,
        export_format: ExportFormat,
    ) -> CSVExportResult:
        rows = self._build_rows(
            document_id=document_id,
            reviewed_invoice=reviewed_invoice,
            status=status,
            reviewed_at=reviewed_at,
            reviewer_notes=reviewer_notes,
            export_format=export_format,
        )
        csv_content = _write_csv(rows)
        return CSVExportResult(
            csv_content=csv_content,
            filename=_safe_filename(document_id, export_format),
            content_type=CSV_CONTENT_TYPE,
            format=export_format,
        )

    def _build_rows(
        self,
        *,
        document_id: str,
        reviewed_invoice: dict[str, Any],
        status: str,
        reviewed_at: str,
        reviewer_notes: str | None,
        export_format: ExportFormat,
    ) -> list[dict[str, str]]:
        if export_format == ExportFormat.generic:
            return _build_generic_rows(
                document_id,
                reviewed_invoice,
                status,
                reviewed_at,
                reviewer_notes,
            )
        if export_format == ExportFormat.quickbooks:
            return _build_quickbooks_rows(reviewed_invoice, reviewer_notes)
        if export_format == ExportFormat.xero:
            return _build_xero_rows(reviewed_invoice)
        raise ValueError("Unsupported CSV export format.")


def _build_generic_rows(
    document_id: str,
    invoice: dict[str, Any],
    status: str,
    reviewed_at: str,
    reviewer_notes: str | None,
) -> list[dict[str, str]]:
    return [
        {
            "document_id": _sanitize_csv_cell(document_id),
            "vendor_name": _sanitize_csv_cell(invoice.get("vendor_name")),
            "invoice_number": _sanitize_csv_cell(invoice.get("invoice_number")),
            "invoice_date": _sanitize_csv_cell(invoice.get("invoice_date")),
            "due_date": _sanitize_csv_cell(invoice.get("due_date")),
            "subtotal": _format_money(invoice.get("subtotal")),
            "tax": _format_money(invoice.get("tax")),
            "total": _format_money(invoice.get("total")),
            "currency": _sanitize_csv_cell(invoice.get("currency")),
            "email": _sanitize_csv_cell(invoice.get("email")),
            "phone": _sanitize_csv_cell(invoice.get("phone")),
            "status": _sanitize_csv_cell(status),
            "reviewed_at": _sanitize_csv_cell(reviewed_at),
            "reviewer_notes": _sanitize_csv_cell(reviewer_notes),
        }
    ]


def _build_quickbooks_rows(
    invoice: dict[str, Any],
    reviewer_notes: str | None,
) -> list[dict[str, str]]:
    memo = reviewer_notes or "Imported from DocuLedger"
    return [
        {
            "Vendor": _sanitize_csv_cell(invoice.get("vendor_name")),
            "Bill No.": _sanitize_csv_cell(invoice.get("invoice_number")),
            "Bill Date": _sanitize_csv_cell(invoice.get("invoice_date")),
            "Due Date": _sanitize_csv_cell(invoice.get("due_date")),
            "Terms": "",
            "Account": _sanitize_csv_cell("Uncategorized Expense"),
            "Memo": _sanitize_csv_cell(memo),
            "Amount": _format_money(invoice.get("total")),
            "Tax Amount": _format_money(invoice.get("tax")),
            "Currency": _sanitize_csv_cell(invoice.get("currency")),
        }
    ]


def _build_xero_rows(invoice: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "ContactName": _sanitize_csv_cell(invoice.get("vendor_name")),
            "InvoiceNumber": _sanitize_csv_cell(invoice.get("invoice_number")),
            "InvoiceDate": _sanitize_csv_cell(invoice.get("invoice_date")),
            "DueDate": _sanitize_csv_cell(invoice.get("due_date")),
            "Description": _sanitize_csv_cell(_xero_description(invoice)),
            "Quantity": "1",
            "UnitAmount": _format_money(invoice.get("subtotal") or invoice.get("total")),
            "TaxAmount": _format_money(invoice.get("tax")),
            "Total": _format_money(invoice.get("total")),
            "Currency": _sanitize_csv_cell(invoice.get("currency")),
        }
    ]


def _xero_description(invoice: dict[str, Any]) -> str:
    line_items = invoice.get("line_items") or []
    if line_items and isinstance(line_items[0], dict):
        description = line_items[0].get("description")
        if description:
            return str(description)
    return "Reviewed invoice import"


def _write_csv(rows: list[dict[str, str]]) -> str:
    output = StringIO()
    fieldnames = list(rows[0].keys())
    writer = csv.DictWriter(output, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


def _sanitize_csv_cell(value: Any) -> str:
    if value is None:
        return ""
    text = str(value)
    if text.startswith(FORMULA_PREFIXES):
        return f"'{text}"
    return text


def _format_money(value: Any) -> str:
    if value is None:
        return ""
    try:
        return f"{float(value):.2f}"
    except (TypeError, ValueError):
        return _sanitize_csv_cell(value)


def _safe_filename(document_id: str, export_format: ExportFormat) -> str:
    return f"doculedger_{document_id}_{export_format.value}.csv"
