from fastapi import APIRouter

from app.schemas.invoice import InvoiceExtractionRequest, InvoiceExtractionResponse
from app.services.extractors.rule_based import RuleBasedInvoiceExtractor


router = APIRouter(prefix="/extractions", tags=["extractions"])


@router.post("/invoice", response_model=InvoiceExtractionResponse)
def extract_invoice(request: InvoiceExtractionRequest) -> InvoiceExtractionResponse:
    extractor = RuleBasedInvoiceExtractor()
    return extractor.extract(request)
