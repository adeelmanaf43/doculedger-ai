"use client";

import type { ProcessingResponse } from "@/lib/types";

type ProcessingPanelProps = {
  documentId?: string;
  processing: ProcessingResponse | null;
  isProcessing: boolean;
  error?: string | null;
  onProcess: () => void;
};

export function ProcessingPanel({
  documentId,
  processing,
  isProcessing,
  error,
  onProcess,
}: ProcessingPanelProps) {
  return (
    <section className="rounded-lg border border-line bg-panel p-5 shadow-sm">
      <div className="flex flex-col gap-1">
        <p className="text-sm font-semibold uppercase tracking-wide text-accent">
          Process
        </p>
        <h2 className="text-xl font-semibold">Create a draft</h2>
        <p className="text-sm leading-6 text-muted">
          The backend extracts text, runs OCR when supported, and creates a
          review-required invoice draft.
        </p>
      </div>

      <button
        className="focus-ring mt-5 rounded-lg bg-ink px-4 py-2 text-sm font-semibold text-white hover:bg-slate-800"
        type="button"
        disabled={!documentId || isProcessing}
        onClick={onProcess}
      >
        {isProcessing ? "Processing..." : "Process document"}
      </button>

      {processing ? (
        <div className="mt-5 grid gap-4">
          <div className="grid gap-3 md:grid-cols-3">
            <Metric label="Status" value={processing.status} />
            <Metric
              label="Text method"
              value={processing.processing.text_extraction_method}
            />
            <Metric
              label="Invoice method"
              value={processing.processing.invoice_extraction_method}
            />
          </div>

          <div className="rounded-lg border border-line bg-paper px-4 py-3">
            <p className="text-sm font-semibold">
              Requires review: {processing.requires_review ? "Yes" : "No"}
            </p>
          </div>

          {Object.keys(processing.confidence).length ? (
            <div>
              <p className="text-sm font-semibold">Confidence</p>
              <div className="mt-2 flex flex-wrap gap-2">
                {Object.entries(processing.confidence).map(([field, score]) => (
                  <span
                    className="rounded-full border border-line bg-white px-3 py-1 text-xs"
                    key={field}
                  >
                    {field}: {confidenceLabel(score)}
                  </span>
                ))}
              </div>
            </div>
          ) : null}

          {processing.warnings.length ? (
            <div>
              <p className="text-sm font-semibold">Warnings</p>
              <div className="mt-2 grid gap-2">
                {processing.warnings.map((warning, index) => (
                  <div
                    className="rounded-lg border border-amber-200 bg-amber-50 px-3 py-2 text-sm text-amber-950"
                    key={`${warning.code}-${index}`}
                  >
                    <span className="font-semibold">{warning.code}</span>
                    <span> - {warning.message}</span>
                  </div>
                ))}
              </div>
            </div>
          ) : null}

          {processing.text_preview ? (
            <details className="rounded-lg border border-line bg-white px-4 py-3">
              <summary className="cursor-pointer text-sm font-semibold">
                Text preview
              </summary>
              <p className="mt-3 whitespace-pre-wrap text-sm leading-6 text-muted">
                {processing.text_preview}
              </p>
            </details>
          ) : null}
        </div>
      ) : null}

      {error ? (
        <div className="mt-4 rounded-lg border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-950">
          {error}
        </div>
      ) : null}
    </section>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg border border-line bg-white px-4 py-3">
      <p className="text-xs font-semibold uppercase tracking-wide text-muted">
        {label}
      </p>
      <p className="mt-1 break-words text-sm font-semibold">{value}</p>
    </div>
  );
}

function confidenceLabel(score: number) {
  if (score >= 0.85) {
    return "high";
  }
  if (score >= 0.6) {
    return "medium";
  }
  return "low";
}
