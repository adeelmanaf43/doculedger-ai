from fastapi import APIRouter, Depends, File, HTTPException, Response, UploadFile, status

from app.core.config import Settings, get_settings
from app.schemas.document import (
    OcrExtractionResult,
    TextExtractionResult,
    UploadedDocumentMetadata,
)
from app.schemas.export import ExportFormat
from app.schemas.processing import ProcessingRequest, ProcessingResponse
from app.schemas.review import (
    DocumentReviewStatusResponse,
    ReviewedInvoiceResponse,
    ReviewRequest,
)
from app.services.extraction.pdf_text import PdfTextExtractor, TextExtractionError
from app.services.exporters.csv_exporter import CSVExporter
from app.services.ocr.tesseract_ocr import OcrError, TesseractOcrProvider
from app.services.pipeline import DocumentProcessingPipeline, ProcessingError
from app.services.review_service import ReviewError, ReviewService
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


@router.post(
    "/{document_id}/review",
    response_model=ReviewedInvoiceResponse,
)
def save_document_review(
    document_id: str,
    request: ReviewRequest,
    app_settings: Settings = Depends(get_settings),
) -> ReviewedInvoiceResponse:
    review_service = ReviewService(app_settings)
    try:
        return review_service.save_review(document_id, request)
    except (DocumentStorageError, ReviewError) as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc


@router.get(
    "/{document_id}/review",
    response_model=ReviewedInvoiceResponse,
)
def get_document_review(
    document_id: str,
    app_settings: Settings = Depends(get_settings),
) -> ReviewedInvoiceResponse:
    review_service = ReviewService(app_settings)
    try:
        return review_service.get_review(document_id)
    except (DocumentStorageError, ReviewError) as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc


@router.get(
    "/{document_id}/status",
    response_model=DocumentReviewStatusResponse,
)
def get_document_status(
    document_id: str,
    app_settings: Settings = Depends(get_settings),
) -> DocumentReviewStatusResponse:
    review_service = ReviewService(app_settings)
    try:
        return review_service.get_status(document_id)
    except DocumentStorageError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc


@router.get("/{document_id}/export")
def export_document_review(
    document_id: str,
    format: ExportFormat = ExportFormat.generic,
    app_settings: Settings = Depends(get_settings),
) -> Response:
    review_service = ReviewService(app_settings)
    exporter = CSVExporter()
    try:
        review = review_service.get_review(document_id)
    except (DocumentStorageError, ReviewError) as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc

    if review.status != "reviewed" or not review.approved:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Invoice must be reviewed and approved before export.",
        )

    export_result = exporter.export_reviewed_invoice(
        document_id=review.document_id,
        reviewed_invoice=review.reviewed_invoice.model_dump(),
        status=review.status,
        approved=review.approved,
        reviewed_at=review.reviewed_at,
        reviewer_notes=review.reviewer_notes,
        export_format=format,
    )
    return Response(
        content=export_result.csv_content,
        media_type=export_result.content_type,
        headers={
            "Content-Disposition": f'attachment; filename="{export_result.filename}"',
        },
    )
