export type ExportFormat = "generic" | "quickbooks" | "xero";

export type ApiError = {
  message: string;
  status?: number;
};

export type UploadResponse = {
  document_id: string;
  original_filename: string;
  safe_filename: string;
  content_type: string;
  size_bytes: number;
  storage_key: string;
  status: string;
};

export type InvoiceLineItem = {
  description: string;
  quantity?: number | null;
  unit_price?: number | null;
  amount?: number | null;
};

export type InvoiceData = {
  vendor_name?: string | null;
  invoice_number?: string | null;
  invoice_date?: string | null;
  due_date?: string | null;
  subtotal?: number | null;
  tax?: number | null;
  total?: number | null;
  currency?: string | null;
  email?: string | null;
  phone?: string | null;
  line_items: InvoiceLineItem[];
};

export type ProcessingWarning = {
  code: string;
  message: string;
  severity: string;
};

export type ProcessingResponse = {
  document_id: string;
  status: string;
  requires_review: boolean;
  processing: {
    text_extraction_method: string;
    invoice_extraction_method: string;
    page_count: number;
    text_length: number;
    warnings: ProcessingWarning[];
  };
  invoice: InvoiceData;
  confidence: Record<string, number>;
  warnings: ProcessingWarning[];
  text_preview?: string | null;
};

export type ReviewCorrection = {
  original?: unknown;
  corrected?: unknown;
};

export type ReviewRequest = {
  invoice: InvoiceData;
  corrections?: Record<string, ReviewCorrection>;
  reviewer_notes?: string | null;
  approved: boolean;
  original_extraction_method?: string | null;
};

export type ReviewedInvoiceResponse = {
  document_id: string;
  status: string;
  requires_review: boolean;
  reviewed_invoice: InvoiceData;
  corrections: Record<string, ReviewCorrection>;
  corrected_fields: string[];
  approved: boolean;
  reviewed_at: string;
  reviewer_notes?: string | null;
  original_extraction_method?: string | null;
  message: string;
};

export type DocumentReviewStatusResponse = {
  document_id: string;
  status: string;
  requires_review: boolean;
};

export type HealthResponse = {
  status: string;
  service: string;
  environment: string;
  free_first: boolean;
};

export type CsvDownload = {
  blob: Blob;
  filename: string;
};
