from fastapi import status

from app.core.config import Settings
from app.repositories.reviewed_invoice_repository import (
    ReviewNotFoundError,
    ReviewedInvoiceRepository,
)
from app.schemas.review import (
    DocumentReviewStatusResponse,
    ReviewedInvoiceResponse,
    ReviewRequest,
)
from app.services.storage.local_storage import LocalDocumentStorage


class ReviewError(Exception):
    def __init__(self, status_code: int, detail: str) -> None:
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


class ReviewService:
    def __init__(self, settings: Settings) -> None:
        self.storage = LocalDocumentStorage(settings)
        self.repository = ReviewedInvoiceRepository(settings)

    def save_review(
        self,
        document_id: str,
        request: ReviewRequest,
    ) -> ReviewedInvoiceResponse:
        document = self.storage.get_stored_document(document_id)
        corrected_fields = sorted(request.corrections.keys())
        saved = self.repository.save_review(
            document_id=document.document_id,
            reviewed_invoice=request.invoice.model_dump(),
            corrections={
                field: correction.model_dump()
                for field, correction in request.corrections.items()
            },
            reviewer_notes=request.reviewer_notes,
            approved=request.approved,
            original_extraction_method=request.original_extraction_method,
            corrected_fields=corrected_fields,
        )
        return _review_response(saved, "Reviewed invoice saved successfully.")

    def get_review(self, document_id: str) -> ReviewedInvoiceResponse:
        self.storage.get_stored_document(document_id)
        try:
            saved = self.repository.get_review(document_id)
        except ReviewNotFoundError as exc:
            raise ReviewError(status.HTTP_404_NOT_FOUND, "Review not found.") from exc
        return _review_response(saved, "Reviewed invoice retrieved successfully.")

    def get_status(self, document_id: str) -> DocumentReviewStatusResponse:
        self.storage.get_stored_document(document_id)
        saved_status = self.repository.get_status(document_id)
        status_value = saved_status or "uploaded"
        return DocumentReviewStatusResponse(
            document_id=document_id,
            status=status_value,
            requires_review=status_value != "reviewed",
        )


def _review_response(saved: dict, message: str) -> ReviewedInvoiceResponse:
    return ReviewedInvoiceResponse(
        document_id=saved["document_id"],
        status=saved["status"],
        requires_review=saved["status"] != "reviewed",
        reviewed_invoice=saved["reviewed_invoice"],
        corrections=saved["corrections"],
        corrected_fields=saved["corrected_fields"],
        approved=saved["approved"],
        reviewed_at=saved["reviewed_at"],
        reviewer_notes=saved["reviewer_notes"],
        original_extraction_method=saved["original_extraction_method"],
        message=message,
    )
