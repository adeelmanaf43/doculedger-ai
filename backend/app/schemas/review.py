from typing import Any

from pydantic import BaseModel, Field

from app.schemas.invoice import ExtractedInvoice


class ReviewCorrection(BaseModel):
    original: Any = None
    corrected: Any = None


class ReviewRequest(BaseModel):
    invoice: ExtractedInvoice
    corrections: dict[str, ReviewCorrection] = Field(default_factory=dict)
    reviewer_notes: str | None = None
    approved: bool = True
    original_extraction_method: str | None = None


class ReviewedInvoiceResponse(BaseModel):
    document_id: str
    status: str
    requires_review: bool
    reviewed_invoice: ExtractedInvoice
    corrections: dict[str, ReviewCorrection] = Field(default_factory=dict)
    corrected_fields: list[str] = Field(default_factory=list)
    approved: bool
    reviewed_at: str
    reviewer_notes: str | None = None
    original_extraction_method: str | None = None
    message: str


class DocumentReviewStatusResponse(BaseModel):
    document_id: str
    status: str
    requires_review: bool
