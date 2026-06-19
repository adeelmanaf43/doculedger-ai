from pydantic import BaseModel


class UploadedDocumentMetadata(BaseModel):
    document_id: str
    original_filename: str
    safe_filename: str
    content_type: str
    size_bytes: int
    storage_key: str
    status: str


class PageText(BaseModel):
    page_number: int
    text: str


class TextExtractionResult(BaseModel):
    document_id: str
    storage_key: str
    page_count: int
    extracted_text: str
    per_page_text: list[PageText]
    extraction_method: str
    warnings: list[str]


class OcrExtractionResult(BaseModel):
    document_id: str
    storage_key: str
    page_count: int
    extracted_text: str
    per_page_text: list[PageText]
    extraction_method: str
    confidence: float | None
    warnings: list[str]
