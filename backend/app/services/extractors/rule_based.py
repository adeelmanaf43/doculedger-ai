from datetime import datetime
import re

from app.schemas.invoice import (
    ExtractedInvoice,
    InvoiceExtractionRequest,
    InvoiceExtractionResponse,
    InvoiceLineItem,
)
from app.services.extractors.base import InvoiceExtractor


INVOICE_NUMBER_PATTERN = re.compile(
    r"\b(?:invoice\s*(?:no\.?|number|#)|inv\s*no\.?|bill\s*no\.?|reference)\s*[:#-]?\s*([A-Z0-9][A-Z0-9._/-]{1,40})",
    re.IGNORECASE,
)
EMAIL_PATTERN = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
PHONE_PATTERN = re.compile(
    r"(?:\+?\d{1,3}[\s.-]?)?(?:\(?\d{3}\)?[\s.-]?)\d{3}[\s.-]?\d{4}"
)
DATE_PATTERN = re.compile(
    r"\b(\d{4}[-/]\d{1,2}[-/]\d{1,2}|\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|[A-Z][a-z]{2,8}\s+\d{1,2},?\s+\d{4})\b"
)
MONEY_VALUE_PATTERN = re.compile(
    r"(?:(USD|EUR|GBP|CAD|AUD)\s*)?([$\u00a3\u20ac])?\s*(-?\d{1,3}(?:,\d{3})*(?:\.\d{2})|-?\d+(?:\.\d{2})?)",
    re.IGNORECASE,
)
LINE_ITEM_PATTERN = re.compile(
    r"^(.{3,}?)\s+(\d+(?:\.\d+)?)\s+([$\u00a3\u20ac]?\s*\d+(?:\.\d{2})?)\s+([$\u00a3\u20ac]?\s*\d+(?:\.\d{2})?)$"
)

DATE_LABELS = {
    "invoice_date": (
        "invoice date",
        "date",
    ),
    "due_date": (
        "due date",
        "payment due",
    ),
}
MONEY_LABELS = {
    "subtotal": ("subtotal", "sub total"),
    "tax": ("sales tax", "vat", "gst", "tax"),
    "total": ("amount due", "balance due", "grand total", "total"),
}
SKIP_VENDOR_TERMS = (
    "invoice",
    "date",
    "total",
    "tax",
    "email",
    "phone",
    "www.",
    "http",
    "@",
)
CURRENCY_BY_SYMBOL = {"$": "USD", "\u20ac": "EUR", "\u00a3": "GBP"}


class RuleBasedInvoiceExtractor(InvoiceExtractor):
    extraction_method = "rule_based"

    def extract(self, request: InvoiceExtractionRequest) -> InvoiceExtractionResponse:
        text = request.text or ""
        lines = _meaningful_lines(text)
        warnings: list[str] = []
        confidence = _default_confidence()

        if len(text.strip()) < 20:
            warnings.append("empty or very short extracted text")

        invoice = ExtractedInvoice()
        invoice.vendor_name = _extract_vendor(lines)
        if invoice.vendor_name:
            confidence["vendor_name"] = 0.65
        else:
            warnings.append("missing vendor")

        invoice.invoice_number = _extract_invoice_number(text)
        if invoice.invoice_number:
            confidence["invoice_number"] = 0.95
        else:
            warnings.append("missing invoice number")

        invoice.invoice_date, invoice_date_warning = _extract_labeled_date(
            text, DATE_LABELS["invoice_date"]
        )
        if invoice.invoice_date:
            confidence["invoice_date"] = 0.9
        else:
            warnings.append("missing date")
        if invoice_date_warning:
            warnings.append(invoice_date_warning)

        invoice.due_date, due_date_warning = _extract_labeled_date(
            text, DATE_LABELS["due_date"]
        )
        if invoice.due_date:
            confidence["due_date"] = 0.9
        if due_date_warning:
            warnings.append(due_date_warning)

        invoice.subtotal = _extract_labeled_money(text, MONEY_LABELS["subtotal"])
        if invoice.subtotal is not None:
            confidence["subtotal"] = 0.9
        invoice.tax = _extract_labeled_money(text, MONEY_LABELS["tax"])
        if invoice.tax is not None:
            confidence["tax"] = 0.9
        invoice.total = _extract_labeled_money(text, MONEY_LABELS["total"])
        if invoice.total is not None:
            confidence["total"] = 0.95
        else:
            warnings.append("missing total")

        invoice.currency = _detect_currency(text)
        if invoice.currency:
            confidence["currency"] = 0.75

        invoice.email = _first_match(EMAIL_PATTERN, text)
        if invoice.email:
            confidence["email"] = 0.9

        invoice.phone = _first_match(PHONE_PATTERN, text)
        if invoice.phone:
            confidence["phone"] = 0.85

        invoice.line_items = _extract_line_items(lines)
        if invoice.line_items:
            confidence["line_items"] = 0.45

        if _has_total_mismatch(invoice.subtotal, invoice.tax, invoice.total):
            warnings.append("subtotal/tax/total mismatch")

        return InvoiceExtractionResponse(
            invoice=invoice,
            confidence=confidence,
            warnings=_dedupe_warnings(warnings),
            extraction_method=self.extraction_method,
            requires_review=True,
        )


def _meaningful_lines(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.strip()]


def _default_confidence() -> dict[str, float]:
    fields = (
        "vendor_name",
        "invoice_number",
        "invoice_date",
        "due_date",
        "subtotal",
        "tax",
        "total",
        "currency",
        "email",
        "phone",
        "line_items",
    )
    return {field: 0.0 for field in fields}


def _extract_vendor(lines: list[str]) -> str | None:
    for line in lines[:8]:
        lowered = line.lower()
        if any(term in lowered for term in SKIP_VENDOR_TERMS):
            continue
        if MONEY_VALUE_PATTERN.search(line):
            continue
        if len(line) < 3:
            continue
        return line[:120]
    return None


def _extract_invoice_number(text: str) -> str | None:
    match = INVOICE_NUMBER_PATTERN.search(text)
    return match.group(1).strip(" .,:;#") if match else None


def _extract_labeled_date(text: str, labels: tuple[str, ...]) -> tuple[str | None, str | None]:
    lines = _meaningful_lines(text)
    for label in labels:
        label_pattern = _label_pattern(label)
        for line in lines:
            lowered_line = line.lower()
            if label == "date" and any(
                term in lowered_line for term in ("due date", "payment due")
            ):
                continue
            if not label_pattern.search(line):
                continue
            date_match = DATE_PATTERN.search(line)
            if date_match:
                return _normalize_date(date_match.group(1))
    return None, None


def _normalize_date(value: str) -> tuple[str | None, str | None]:
    cleaned = value.strip().replace(",", "")
    formats = (
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%m/%d/%Y",
        "%m-%d-%Y",
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%m/%d/%y",
        "%d/%m/%y",
        "%b %d %Y",
        "%B %d %Y",
    )
    possible_dates: list[datetime] = []
    for date_format in formats:
        try:
            parsed = datetime.strptime(cleaned, date_format)
        except ValueError:
            continue
        possible_dates.append(parsed)

    unique_dates = {date.date().isoformat() for date in possible_dates}
    if len(unique_dates) == 1:
        return unique_dates.pop(), None
    if len(unique_dates) > 1:
        return None, "ambiguous date"
    return None, "ambiguous date"


def _extract_labeled_money(text: str, labels: tuple[str, ...]) -> float | None:
    lines = _meaningful_lines(text)
    for label in labels:
        label_pattern = _label_pattern(label)
        for line in lines:
            if not label_pattern.search(line):
                continue
            values = _money_values(line)
            if values:
                return values[-1]
    return None


def _label_pattern(label: str) -> re.Pattern[str]:
    return re.compile(rf"(?<![A-Za-z]){re.escape(label)}(?![A-Za-z])", re.IGNORECASE)


def _money_values(text: str) -> list[float]:
    values: list[float] = []
    for match in MONEY_VALUE_PATTERN.finditer(text):
        raw_value = match.group(3).replace(",", "")
        try:
            values.append(round(float(raw_value), 2))
        except ValueError:
            continue
    return values


def _detect_currency(text: str) -> str | None:
    code_match = re.search(r"\b(USD|EUR|GBP|CAD|AUD)\b", text, re.IGNORECASE)
    if code_match:
        return code_match.group(1).upper()
    for symbol, code in CURRENCY_BY_SYMBOL.items():
        if symbol in text:
            return code
    return None


def _first_match(pattern: re.Pattern[str], text: str) -> str | None:
    match = pattern.search(text)
    return match.group(0) if match else None


def _extract_line_items(lines: list[str]) -> list[InvoiceLineItem]:
    line_items: list[InvoiceLineItem] = []
    for line in lines:
        if any(
            term in line.lower()
            for term in ("subtotal", "total", "tax", "balance due")
        ):
            continue
        match = LINE_ITEM_PATTERN.match(line)
        if not match:
            continue
        line_items.append(
            InvoiceLineItem(
                description=match.group(1).strip(),
                quantity=_safe_float(match.group(2)),
                unit_price=_money_values(match.group(3))[0],
                amount=_money_values(match.group(4))[0],
            )
        )
    return line_items[:20]


def _safe_float(value: str) -> float | None:
    try:
        return float(value)
    except ValueError:
        return None


def _has_total_mismatch(
    subtotal: float | None,
    tax: float | None,
    total: float | None,
) -> bool:
    if subtotal is None or tax is None or total is None:
        return False
    return abs((subtotal + tax) - total) > 0.02


def _dedupe_warnings(warnings: list[str]) -> list[str]:
    deduped: list[str] = []
    for warning in warnings:
        if warning not in deduped:
            deduped.append(warning)
    return deduped
