from pydantic import BaseModel


class UploadedDocumentMetadata(BaseModel):
    document_id: str
    original_filename: str
    safe_filename: str
    content_type: str
    size_bytes: int
    storage_key: str
    status: str
