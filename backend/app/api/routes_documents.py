from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.core.config import Settings, get_settings
from app.schemas.document import UploadedDocumentMetadata
from app.services.storage.local_storage import (
    DocumentUploadError,
    LocalDocumentStorage,
)


router = APIRouter(prefix="/documents", tags=["documents"])


@router.post(
    "/upload",
    response_model=UploadedDocumentMetadata,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    file: UploadFile = File(...),
    app_settings: Settings = Depends(get_settings),
) -> UploadedDocumentMetadata:
    storage = LocalDocumentStorage(app_settings)
    try:
        return await storage.save_upload(file)
    except DocumentUploadError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc
