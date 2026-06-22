from pydantic import BaseModel, Field

from app.schemas.invoice import ExtractedInvoice


class ProcessingRequest(BaseModel):
    force_ocr: bool = False
    include_text_preview: bool = True


class ProcessingWarning(BaseModel):
    code: str
    message: str
    severity: str


class ProcessingMetadata(BaseModel):
    text_extraction_method: str
    invoice_extraction_method: str
    page_count: int
    text_length: int
    warnings: list[ProcessingWarning] = Field(default_factory=list)


class ProcessingResponse(BaseModel):
    document_id: str
    status: str
    requires_review: bool
    processing: ProcessingMetadata
    invoice: ExtractedInvoice
    confidence: dict[str, float] = Field(default_factory=dict)
    warnings: list[ProcessingWarning] = Field(default_factory=list)
    text_preview: str | None = None
