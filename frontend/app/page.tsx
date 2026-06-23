"use client";

import { useEffect, useState } from "react";
import { ExportPanel } from "@/components/export-panel";
import { ProcessingPanel } from "@/components/processing-panel";
import { ReviewForm } from "@/components/review-form";
import { StatusAlert } from "@/components/status-alert";
import { UploadPanel } from "@/components/upload-panel";
import {
  checkHealth,
  exportCsv,
  processDocument,
  saveReview,
  uploadDocument,
} from "@/lib/api";
import type {
  ApiError,
  ExportFormat,
  HealthResponse,
  ProcessingResponse,
  ReviewedInvoiceResponse,
  ReviewRequest,
  UploadResponse,
} from "@/lib/types";

export default function Home() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [healthError, setHealthError] = useState<string | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [upload, setUpload] = useState<UploadResponse | null>(null);
  const [processing, setProcessing] = useState<ProcessingResponse | null>(null);
  const [review, setReview] = useState<ReviewedInvoiceResponse | null>(null);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const [processError, setProcessError] = useState<string | null>(null);
  const [reviewError, setReviewError] = useState<string | null>(null);
  const [exportError, setExportError] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isSavingReview, setIsSavingReview] = useState(false);
  const [activeExport, setActiveExport] = useState<ExportFormat | null>(null);

  useEffect(() => {
    checkHealth()
      .then((result) => {
        setHealth(result);
        setHealthError(null);
      })
      .catch((error: ApiError) => {
        setHealth(null);
        setHealthError(error.message);
      });
  }, []);

  async function handleUpload() {
    if (!selectedFile) {
      return;
    }

    setIsUploading(true);
    setUploadError(null);
    setProcessing(null);
    setReview(null);
    try {
      const result = await uploadDocument(selectedFile);
      setUpload(result);
    } catch (error) {
      setUpload(null);
      setUploadError(errorMessage(error));
    } finally {
      setIsUploading(false);
    }
  }

  async function handleProcess() {
    if (!upload?.document_id) {
      return;
    }

    setIsProcessing(true);
    setProcessError(null);
    setReview(null);
    try {
      const result = await processDocument(upload.document_id);
      setProcessing(result);
    } catch (error) {
      setProcessing(null);
      setProcessError(errorMessage(error));
    } finally {
      setIsProcessing(false);
    }
  }

  async function handleSaveReview(payload: ReviewRequest) {
    if (!upload?.document_id) {
      return;
    }

    setIsSavingReview(true);
    setReviewError(null);
    try {
      const result = await saveReview(upload.document_id, payload);
      setReview(result);
    } catch (error) {
      setReviewError(errorMessage(error));
    } finally {
      setIsSavingReview(false);
    }
  }

  async function handleExport(format: ExportFormat) {
    if (!upload?.document_id) {
      return;
    }

    setActiveExport(format);
    setExportError(null);
    try {
      const download = await exportCsv(upload.document_id, format);
      triggerDownload(download.blob, download.filename);
    } catch (error) {
      setExportError(errorMessage(error));
    } finally {
      setActiveExport(null);
    }
  }

  return (
    <main className="min-h-screen bg-paper">
      <header className="border-b border-line bg-white">
        <div className="mx-auto flex max-w-6xl flex-col gap-4 px-5 py-6 md:flex-row md:items-end md:justify-between">
          <div>
            <p className="text-sm font-semibold uppercase tracking-wide text-accent">
              DocuLedger
            </p>
            <h1 className="mt-2 max-w-3xl text-3xl font-semibold tracking-normal text-ink md:text-4xl">
              Review-assisted invoice processing for bookkeeping workflows
            </h1>
            <p className="mt-3 max-w-2xl text-sm leading-6 text-muted">
              Upload a document, create a local extraction draft, review the
              fields, then download a clean CSV.
            </p>
          </div>
          <div className="min-w-64">
            {health ? (
              <StatusAlert
                tone="success"
                title="Backend connected"
                message={`${health.service} is running in ${health.environment} mode.`}
              />
            ) : (
              <StatusAlert
                tone="warning"
                title="Backend status"
                message={
                  healthError ??
                  "Checking the FastAPI backend connection at startup."
                }
              />
            )}
          </div>
        </div>
      </header>

      <div className="mx-auto grid max-w-6xl gap-5 px-5 py-6">
        <WorkflowSteps
          uploaded={Boolean(upload)}
          processed={Boolean(processing)}
          reviewed={Boolean(review?.approved)}
        />

        <div className="grid gap-5 lg:grid-cols-[minmax(0,0.9fr)_minmax(0,1.1fr)]">
          <div className="grid content-start gap-5">
            <UploadPanel
              selectedFile={selectedFile}
              upload={upload}
              isUploading={isUploading}
              error={uploadError}
              onFileChange={setSelectedFile}
              onUpload={handleUpload}
            />
            <ProcessingPanel
              documentId={upload?.document_id}
              processing={processing}
              isProcessing={isProcessing}
              error={processError}
              onProcess={handleProcess}
            />
            <ExportPanel
              documentId={upload?.document_id}
              review={review}
              activeFormat={activeExport}
              error={exportError}
              onExport={handleExport}
            />
          </div>

          <ReviewForm
            processing={processing}
            review={review}
            isSaving={isSavingReview}
            error={reviewError}
            onSave={handleSaveReview}
          />
        </div>
      </div>
    </main>
  );
}

function WorkflowSteps({
  uploaded,
  processed,
  reviewed,
}: {
  uploaded: boolean;
  processed: boolean;
  reviewed: boolean;
}) {
  const steps = [
    { label: "Upload", done: uploaded },
    { label: "Process", done: processed },
    { label: "Review", done: reviewed },
    { label: "Export", done: reviewed },
  ];

  return (
    <div className="grid gap-2 rounded-lg border border-line bg-white p-3 md:grid-cols-4">
      {steps.map((step) => (
        <div
          className={`rounded-lg px-3 py-2 text-sm font-semibold ${
            step.done ? "bg-teal-50 text-teal-950" : "bg-paper text-muted"
          }`}
          key={step.label}
        >
          {step.label}
        </div>
      ))}
    </div>
  );
}

function errorMessage(error: unknown): string {
  if (typeof error === "object" && error && "message" in error) {
    const message = (error as { message?: unknown }).message;
    if (typeof message === "string") {
      return message;
    }
  }
  return "Something went wrong. Please try again.";
}

function triggerDownload(blob: Blob, filename: string) {
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}
