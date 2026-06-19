from fastapi import status
from PIL import Image, UnidentifiedImageError
from pypdf import PdfReader
import pytesseract
from pytesseract import Output, TesseractError, TesseractNotFoundError

from app.core.config import Settings
from app.schemas.document import OcrExtractionResult, PageText
from app.services.storage.local_storage import StoredDocumentRef


SUPPORTED_IMAGE_TYPES = {"image/png", "image/jpeg"}
PDF_OCR_LIMITATION = (
    "Scanned PDF OCR requires PDF-to-image conversion, which is not implemented yet. "
    "Upload page images as PNG, JPG, or JPEG for local OCR."
)


class OcrError(Exception):
    def __init__(self, status_code: int, detail: str) -> None:
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


class TesseractOcrProvider:
    extraction_method = "tesseract_ocr"

    def __init__(self, settings: Settings) -> None:
        if settings.tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = settings.tesseract_cmd

    def extract(self, document: StoredDocumentRef) -> OcrExtractionResult:
        if document.content_type == "application/pdf":
            return self._pdf_limitation_result(document)

        if document.content_type not in SUPPORTED_IMAGE_TYPES:
            raise OcrError(
                status.HTTP_400_BAD_REQUEST,
                "OCR currently supports PNG, JPG, JPEG, and scanned PDF limitation notices only.",
            )

        try:
            with Image.open(document.path) as image:
                image.load()
                data = pytesseract.image_to_data(image, output_type=Output.DICT)
        except TesseractNotFoundError as exc:
            raise OcrError(
                status.HTTP_503_SERVICE_UNAVAILABLE,
                "Tesseract is not installed or DOCULEDGER_TESSERACT_CMD is not configured.",
            ) from exc
        except TesseractError as exc:
            raise OcrError(
                status.HTTP_502_BAD_GATEWAY,
                "Tesseract OCR failed while processing the image.",
            ) from exc
        except UnidentifiedImageError as exc:
            raise OcrError(
                status.HTTP_400_BAD_REQUEST,
                "Unable to read image for OCR.",
            ) from exc

        extracted_text = _join_ocr_words(data.get("text", []))
        confidence = _average_confidence(data.get("conf", []))
        warnings: list[str] = []
        if not extracted_text:
            warnings.append("No text was extracted from this image.")
        if confidence is None:
            warnings.append("OCR confidence was not available.")

        return OcrExtractionResult(
            document_id=document.document_id,
            storage_key=document.storage_key,
            page_count=1,
            extracted_text=extracted_text,
            per_page_text=[PageText(page_number=1, text=extracted_text)],
            extraction_method=self.extraction_method,
            confidence=confidence,
            warnings=warnings,
        )

    def _pdf_limitation_result(self, document: StoredDocumentRef) -> OcrExtractionResult:
        page_count = 0
        try:
            page_count = len(PdfReader(document.path).pages)
        except Exception:
            page_count = 0

        return OcrExtractionResult(
            document_id=document.document_id,
            storage_key=document.storage_key,
            page_count=page_count,
            extracted_text="",
            per_page_text=[
                PageText(page_number=page_number, text="")
                for page_number in range(1, page_count + 1)
            ],
            extraction_method=self.extraction_method,
            confidence=None,
            warnings=[PDF_OCR_LIMITATION],
        )


def _join_ocr_words(words: list[str]) -> str:
    return " ".join(word.strip() for word in words if word and word.strip())


def _average_confidence(confidences: list[str | int | float]) -> float | None:
    values: list[float] = []
    for confidence in confidences:
        try:
            value = float(confidence)
        except (TypeError, ValueError):
            continue
        if value >= 0:
            values.append(value)
    if not values:
        return None
    return round(sum(values) / len(values), 2)
