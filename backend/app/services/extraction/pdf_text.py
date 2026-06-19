from pypdf import PdfReader

from fastapi import status

from app.schemas.document import PageText, TextExtractionResult
from app.services.storage.local_storage import StoredDocumentRef


class TextExtractionError(Exception):
    def __init__(self, status_code: int, detail: str) -> None:
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


class PdfTextExtractor:
    extraction_method = "pdf_text"

    def extract(self, document: StoredDocumentRef) -> TextExtractionResult:
        if document.content_type != "application/pdf":
            raise TextExtractionError(
                status.HTTP_400_BAD_REQUEST,
                "Text extraction currently supports text-based PDF files only.",
            )

        try:
            reader = PdfReader(document.path)
        except Exception as exc:
            raise TextExtractionError(
                status.HTTP_400_BAD_REQUEST,
                "Unable to read PDF for text extraction.",
            ) from exc

        warnings: list[str] = []
        per_page_text: list[PageText] = []

        for index, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text() or ""
            if not page_text.strip():
                warnings.append(f"Page {index} did not contain extractable text.")
            per_page_text.append(PageText(page_number=index, text=page_text))

        extracted_text = "\n\n".join(page.text for page in per_page_text).strip()
        if not extracted_text:
            warnings.append(
                "No text was extracted. This may be a scanned image PDF that needs OCR."
            )

        return TextExtractionResult(
            document_id=document.document_id,
            storage_key=document.storage_key,
            page_count=len(reader.pages),
            extracted_text=extracted_text,
            per_page_text=per_page_text,
            extraction_method=self.extraction_method,
            warnings=warnings,
        )
