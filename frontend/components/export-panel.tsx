"use client";

import type { ExportFormat, ReviewedInvoiceResponse } from "@/lib/types";

type ExportPanelProps = {
  documentId?: string;
  review: ReviewedInvoiceResponse | null;
  activeFormat: ExportFormat | null;
  error?: string | null;
  onExport: (format: ExportFormat) => void;
};

const formats: { format: ExportFormat; label: string }[] = [
  { format: "generic", label: "Download Generic CSV" },
  { format: "quickbooks", label: "Download QuickBooks CSV" },
  { format: "xero", label: "Download Xero CSV" },
];

export function ExportPanel({
  documentId,
  review,
  activeFormat,
  error,
  onExport,
}: ExportPanelProps) {
  const canExport = Boolean(documentId && review?.approved && review.status === "reviewed");

  return (
    <section className="rounded-lg border border-line bg-panel p-5 shadow-sm">
      <div className="flex flex-col gap-1">
        <p className="text-sm font-semibold uppercase tracking-wide text-accent">
          Export
        </p>
        <h2 className="text-xl font-semibold">Download CSV</h2>
        <p className="text-sm leading-6 text-muted">
          Export buttons unlock after the reviewed invoice is approved.
        </p>
      </div>

      <div className="mt-5 flex flex-wrap gap-3">
        {formats.map(({ format, label }) => (
          <button
            className="focus-ring rounded-lg border border-line bg-white px-4 py-2 text-sm font-semibold text-ink hover:border-accent"
            type="button"
            key={format}
            disabled={!canExport || activeFormat === format}
            onClick={() => onExport(format)}
          >
            {activeFormat === format ? "Preparing..." : label}
          </button>
        ))}
      </div>

      {!canExport ? (
        <p className="mt-4 text-sm text-muted">
          Review and approve the invoice before exporting.
        </p>
      ) : null}

      {error ? (
        <div className="mt-4 rounded-lg border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-950">
          {error}
        </div>
      ) : null}
    </section>
  );
}
