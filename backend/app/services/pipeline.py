from fastapi import status

from app.core.config import Settings
from app.schemas.invoice import InvoiceExtractionRequest
from app.schemas.processing import (
    ProcessingMetadata,
    ProcessingRequest,
    ProcessingResponse,
    ProcessingWarning,
)
from app.services.extraction.pdf_text import PdfTextExtractor, TextExtractionError
from app.services.extractors.rule_based import RuleBasedInvoiceExtractor
from app.services.ocr.tesseract_ocr import OcrError, TesseractOcrProvider
from app.services.storage.local_storage import LocalDocumentStorage, StoredDocumentRef


TEXT_PREVIEW_LENGTH = 400
MIN_USEFUL_TEXT_LENGTH = 20


class ProcessingError(Exception):
    def __init__(self, status_code: int, detail: str) -> None:
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


class DocumentProcessingPipeline:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.storage = LocalDocumentStorage(settings)
        self.pdf_extractor = PdfTextExtractor()
        self.ocr_provider = TesseractOcrProvider(settings)
        self.invoice_extractor = RuleBasedInvoiceExtractor()

    def process(
        self,
        document_id: str,
        request: ProcessingRequest,
    ) -> ProcessingResponse:
        document = self.storage.get_stored_document(document_id)
        text_result = self._extract_text(document, request)
        invoice_result = self.invoice_extractor.extract(
            InvoiceExtractionRequest(
                text=text_result.text,
                source=text_result.method,
                ocr_confidence=text_result.ocr_confidence,
            )
        )

        processing_warnings = text_result.warnings + [
            _warning_from_invoice_warning(warning)
            for warning in invoice_result.warnings
        ]
        processing_warnings.append(
            ProcessingWarning(
                code="review_required",
                message="Human review is required before export or bookkeeping use.",
                severity="medium",
            )
        )

        return ProcessingResponse(
            document_id=document.document_id,
            status="review_required",
            requires_review=True,
            processing=ProcessingMetadata(
                text_extraction_method=text_result.method,
                invoice_extraction_method=invoice_result.extraction_method,
                page_count=text_result.page_count,
                text_length=len(text_result.text),
                warnings=processing_warnings,
            ),
            invoice=invoice_result.invoice,
            confidence=invoice_result.confidence,
            warnings=processing_warnings,
            text_preview=(
                _preview(text_result.text)
                if request.include_text_preview
                else None
            ),
        )

    def _extract_text(
        self,
        document: StoredDocumentRef,
        request: ProcessingRequest,
    ) -> "_PipelineTextResult":
        if document.content_type == "application/pdf":
            return self._extract_pdf_text(document, request)
        if document.content_type in {"image/png", "image/jpeg"}:
            return self._extract_image_text(document)
        raise ProcessingError(
            status.HTTP_400_BAD_REQUEST,
            "Document type is not supported for processing.",
        )

    def _extract_pdf_text(
        self,
        document: StoredDocumentRef,
        request: ProcessingRequest,
    ) -> "_PipelineTextResult":
        if request.force_ocr:
            ocr_result = self.ocr_provider.extract(document)
            return _PipelineTextResult(
                method="unsupported_scanned_pdf",
                page_count=ocr_result.page_count,
                text=ocr_result.extracted_text,
                warnings=[
                    _warning_from_text_layer(warning)
                    for warning in ocr_result.warnings
                ],
                ocr_confidence=ocr_result.confidence,
            )

        try:
            pdf_result = self.pdf_extractor.extract(document)
        except TextExtractionError as exc:
            raise ProcessingError(exc.status_code, exc.detail) from exc

        warnings = [_warning_from_text_layer(warning) for warning in pdf_result.warnings]
        method = pdf_result.extraction_method
        if len(pdf_result.extracted_text.strip()) < MIN_USEFUL_TEXT_LENGTH:
            method = "unsupported_scanned_pdf"
            warnings.append(
                ProcessingWarning(
                    code="scanned_pdf_not_supported_yet",
                    message=(
                        "No useful embedded PDF text was found. Scanned PDF page "
                        "conversion is not implemented yet."
                    ),
                    severity="medium",
                )
            )
            warnings.append(
                ProcessingWarning(
                    code="empty_extracted_text",
                    message="Extracted text is empty or too short for reliable field extraction.",
                    severity="high",
                )
            )

        return _PipelineTextResult(
            method=method,
            page_count=pdf_result.page_count,
            text=pdf_result.extracted_text,
            warnings=warnings,
            ocr_confidence=None,
        )

    def _extract_image_text(self, document: StoredDocumentRef) -> "_PipelineTextResult":
        try:
            ocr_result = self.ocr_provider.extract(document)
        except OcrError as exc:
            raise ProcessingError(exc.status_code, exc.detail) from exc

        warnings = [_warning_from_text_layer(warning) for warning in ocr_result.warnings]
        if ocr_result.confidence is not None and ocr_result.confidence < 70:
            warnings.append(
                ProcessingWarning(
                    code="low_ocr_confidence",
                    message="OCR confidence is low; review extracted fields carefully.",
                    severity="medium",
                )
            )
        if len(ocr_result.extracted_text.strip()) < MIN_USEFUL_TEXT_LENGTH:
            warnings.append(
                ProcessingWarning(
                    code="empty_extracted_text",
                    message="Extracted text is empty or too short for reliable field extraction.",
                    severity="high",
                )
            )

        return _PipelineTextResult(
            method=ocr_result.extraction_method,
            page_count=ocr_result.page_count,
            text=ocr_result.extracted_text,
            warnings=warnings,
            ocr_confidence=ocr_result.confidence,
        )


class _PipelineTextResult:
    def __init__(
        self,
        method: str,
        page_count: int,
        text: str,
        warnings: list[ProcessingWarning],
        ocr_confidence: float | None,
    ) -> None:
        self.method = method
        self.page_count = page_count
        self.text = text
        self.warnings = warnings
        self.ocr_confidence = ocr_confidence


def _preview(text: str) -> str:
    return text[:TEXT_PREVIEW_LENGTH]


def _warning_from_text_layer(message: str) -> ProcessingWarning:
    lowered = message.lower()
    if "pdf-to-image" in lowered or "scanned" in lowered:
        return ProcessingWarning(
            code="scanned_pdf_not_supported_yet",
            message=message,
            severity="medium",
        )
    if "no text" in lowered or "empty" in lowered:
        return ProcessingWarning(
            code="empty_extracted_text",
            message=message,
            severity="high",
        )
    return ProcessingWarning(
        code="text_extraction_warning",
        message=message,
        severity="medium",
    )


def _warning_from_invoice_warning(message: str) -> ProcessingWarning:
    warning_map = {
        "missing vendor": ("missing_vendor", "medium"),
        "missing invoice number": ("missing_invoice_number", "high"),
        "missing date": ("missing_invoice_date", "high"),
        "missing total": ("missing_total", "high"),
        "ambiguous date": ("ambiguous_date", "medium"),
        "subtotal/tax/total mismatch": ("total_mismatch", "high"),
        "empty or very short extracted text": ("empty_extracted_text", "high"),
    }
    code, severity = warning_map.get(message, ("invoice_extraction_warning", "medium"))
    return ProcessingWarning(code=code, message=message, severity=severity)
