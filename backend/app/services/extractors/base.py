from abc import ABC, abstractmethod

from app.schemas.invoice import InvoiceExtractionRequest, InvoiceExtractionResponse


class InvoiceExtractor(ABC):
    extraction_method: str

    @abstractmethod
    def extract(self, request: InvoiceExtractionRequest) -> InvoiceExtractionResponse:
        raise NotImplementedError
