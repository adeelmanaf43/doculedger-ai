from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.core.config import Settings, get_settings
from app.schemas.document import (
    OcrExtractionResult,
    TextExtractionResult,
    UploadedDocumentMetadata,
)
from app.schemas.processing import ProcessingRequest, ProcessingResponse
from app.services.extraction.pdf_text import PdfTextExtractor, TextExtractionError
from app.services.ocr.tesseract_ocr import OcrError, TesseractOcrProvider
from app.services.pipeline import DocumentProcessingPipeline, ProcessingError
from app.services.storage.local_storage import (
    DocumentStorageError,
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


@router.post(
    "/{document_id}/extract-text",
    response_model=TextExtractionResult,
)
def extract_document_text(
    document_id: str,
    app_settings: Settings = Depends(get_settings),
) -> TextExtractionResult:
    storage = LocalDocumentStorage(app_settings)
    extractor = PdfTextExtractor()
    try:
        document = storage.get_stored_document(document_id)
        return extractor.extract(document)
    except (DocumentStorageError, TextExtractionError) as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc


@router.post(
    "/{document_id}/ocr",
    response_model=OcrExtractionResult,
)
def ocr_document(
    document_id: str,
    app_settings: Settings = Depends(get_settings),
) -> OcrExtractionResult:
    storage = LocalDocumentStorage(app_settings)
    ocr_provider = TesseractOcrProvider(app_settings)
    try:
        document = storage.get_stored_document(document_id)
        return ocr_provider.extract(document)
    except (DocumentStorageError, OcrError) as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc


@router.post(
    "/{document_id}/process",
    response_model=ProcessingResponse,
)
def process_document(
    document_id: str,
    request: ProcessingRequest | None = None,
    app_settings: Settings = Depends(get_settings),
) -> ProcessingResponse:
    pipeline = DocumentProcessingPipeline(app_settings)
    try:
        return pipeline.process(document_id, request or ProcessingRequest())
    except (DocumentStorageError, ProcessingError) as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc
