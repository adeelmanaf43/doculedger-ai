from pydantic import BaseModel, Field


class InvoiceExtractionRequest(BaseModel):
    text: str
    source: str
    ocr_confidence: float | None = None


class InvoiceLineItem(BaseModel):
    description: str
    quantity: float | None = None
    unit_price: float | None = None
    amount: float | None = None


class ExtractedInvoice(BaseModel):
    vendor_name: str | None = None
    invoice_number: str | None = None
    invoice_date: str | None = None
    due_date: str | None = None
    subtotal: float | None = None
    tax: float | None = None
    total: float | None = None
    currency: str | None = None
    email: str | None = None
    phone: str | None = None
    line_items: list[InvoiceLineItem] = Field(default_factory=list)


class InvoiceExtractionResponse(BaseModel):
    invoice: ExtractedInvoice
    confidence: dict[str, float] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)
    extraction_method: str
    requires_review: bool
