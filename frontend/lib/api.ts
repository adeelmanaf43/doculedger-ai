import type {
  CsvDownload,
  DocumentReviewStatusResponse,
  ExportFormat,
  HealthResponse,
  ProcessingResponse,
  ReviewedInvoiceResponse,
  ReviewRequest,
  UploadResponse,
} from "./types";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_DOCULEDGER_API_BASE_URL ?? "http://localhost:8000";

export async function checkHealth(): Promise<HealthResponse> {
  return requestJson<HealthResponse>("/health");
}

export async function uploadDocument(file: File): Promise<UploadResponse> {
  const body = new FormData();
  body.append("file", file);

  return requestJson<UploadResponse>("/documents/upload", {
    method: "POST",
    body,
  });
}

export async function processDocument(
  documentId: string,
): Promise<ProcessingResponse> {
  return requestJson<ProcessingResponse>(`/documents/${documentId}/process`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      include_text_preview: true,
    }),
  });
}

export async function saveReview(
  documentId: string,
  payload: ReviewRequest,
): Promise<ReviewedInvoiceResponse> {
  return requestJson<ReviewedInvoiceResponse>(`/documents/${documentId}/review`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
}

export async function getReview(
  documentId: string,
): Promise<ReviewedInvoiceResponse> {
  return requestJson<ReviewedInvoiceResponse>(`/documents/${documentId}/review`);
}

export async function getStatus(
  documentId: string,
): Promise<DocumentReviewStatusResponse> {
  return requestJson<DocumentReviewStatusResponse>(
    `/documents/${documentId}/status`,
  );
}

export async function exportCsv(
  documentId: string,
  format: ExportFormat,
): Promise<CsvDownload> {
  const response = await fetch(
    `${API_BASE_URL}/documents/${documentId}/export?format=${format}`,
  );
  if (!response.ok) {
    throw await toApiError(response);
  }

  return {
    blob: await response.blob(),
    filename:
      filenameFromContentDisposition(response.headers.get("content-disposition")) ??
      `doculedger_${documentId}_${format}.csv`,
  };
}

async function requestJson<T>(path: string, init?: RequestInit): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}${path}`, init);
  } catch {
    throw {
      message:
        "Could not reach the DocuLedger backend. Make sure the FastAPI server is running.",
    };
  }

  if (!response.ok) {
    throw await toApiError(response);
  }

  return response.json() as Promise<T>;
}

async function toApiError(response: Response) {
  let message = `Request failed with status ${response.status}.`;
  try {
    const data = (await response.json()) as { detail?: unknown };
    if (typeof data.detail === "string") {
      message = data.detail;
    } else if (Array.isArray(data.detail)) {
      message = "Some submitted fields are invalid. Please review the form.";
    }
  } catch {
    message = response.statusText || message;
  }
  return { message, status: response.status };
}

function filenameFromContentDisposition(header: string | null): string | null {
  if (!header) {
    return null;
  }

  const match = header.match(/filename="?([^";]+)"?/i);
  return match?.[1] ?? null;
}
