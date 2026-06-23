from enum import StrEnum

from pydantic import BaseModel


class ExportFormat(StrEnum):
    generic = "generic"
    quickbooks = "quickbooks"
    xero = "xero"


class CSVExportResult(BaseModel):
    csv_content: str
    filename: str
    content_type: str
    format: ExportFormat
