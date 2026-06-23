"use client";

import { useEffect, useMemo, useState } from "react";
import type {
  InvoiceData,
  ProcessingResponse,
  ReviewedInvoiceResponse,
  ReviewCorrection,
  ReviewRequest,
} from "@/lib/types";

type ReviewFormProps = {
  processing: ProcessingResponse | null;
  review: ReviewedInvoiceResponse | null;
  isSaving: boolean;
  error?: string | null;
  onSave: (payload: ReviewRequest) => void;
};

type EditableInvoice = Omit<InvoiceData, "line_items"> & {
  line_items: InvoiceData["line_items"];
};

const emptyInvoice: EditableInvoice = {
  vendor_name: "",
  invoice_number: "",
  invoice_date: "",
  due_date: "",
  subtotal: null,
  tax: null,
  total: null,
  currency: "",
  email: "",
  phone: "",
  line_items: [],
};

export function ReviewForm({
  processing,
  review,
  isSaving,
  error,
  onSave,
}: ReviewFormProps) {
  const sourceInvoice = useMemo(
    () => review?.reviewed_invoice ?? processing?.invoice ?? emptyInvoice,
    [processing?.invoice, review?.reviewed_invoice],
  );
  const [invoice, setInvoice] = useState<EditableInvoice>(sourceInvoice);
  const [reviewerNotes, setReviewerNotes] = useState(
    review?.reviewer_notes ?? "",
  );

  useEffect(() => {
    setInvoice(sourceInvoice);
    setReviewerNotes(review?.reviewer_notes ?? "");
  }, [review?.reviewer_notes, sourceInvoice]);

  if (!processing) {
    return (
      <section className="rounded-lg border border-line bg-panel p-5 shadow-sm">
        <p className="text-sm font-semibold uppercase tracking-wide text-accent">
          Review
        </p>
        <h2 className="mt-1 text-xl font-semibold">Approve the draft</h2>
        <p className="mt-2 text-sm leading-6 text-muted">
          Process a document first to review extracted fields.
        </p>
      </section>
    );
  }

  function updateField(field: keyof EditableInvoice, value: string) {
    setInvoice((current) => ({
      ...current,
      [field]: moneyFields.has(field) ? parseOptionalNumber(value) : value,
    }));
  }

  function handleSave() {
    if (!processing) {
      return;
    }

    onSave({
      invoice: normalizeInvoice(invoice),
      corrections: buildCorrections(processing.invoice, invoice),
      reviewer_notes: reviewerNotes || null,
      approved: true,
      original_extraction_method: processing.processing.invoice_extraction_method,
    });
  }

  return (
    <section className="rounded-lg border border-line bg-panel p-5 shadow-sm">
      <div className="flex flex-col gap-1">
        <p className="text-sm font-semibold uppercase tracking-wide text-accent">
          Review
        </p>
        <h2 className="text-xl font-semibold">Correct and approve</h2>
        <p className="text-sm leading-6 text-muted">
          Review every field before saving. Export unlocks after approval.
        </p>
      </div>

      <div className="mt-5 grid gap-4 md:grid-cols-2">
        <TextField
          label="Vendor name"
          value={invoice.vendor_name ?? ""}
          onChange={(value) => updateField("vendor_name", value)}
        />
        <TextField
          label="Invoice number"
          value={invoice.invoice_number ?? ""}
          onChange={(value) => updateField("invoice_number", value)}
        />
        <TextField
          label="Invoice date"
          type="date"
          value={invoice.invoice_date ?? ""}
          onChange={(value) => updateField("invoice_date", value)}
        />
        <TextField
          label="Due date"
          type="date"
          value={invoice.due_date ?? ""}
          onChange={(value) => updateField("due_date", value)}
        />
        <TextField
          label="Subtotal"
          type="number"
          value={numberValue(invoice.subtotal)}
          onChange={(value) => updateField("subtotal", value)}
        />
        <TextField
          label="Tax"
          type="number"
          value={numberValue(invoice.tax)}
          onChange={(value) => updateField("tax", value)}
        />
        <TextField
          label="Total"
          type="number"
          value={numberValue(invoice.total)}
          onChange={(value) => updateField("total", value)}
        />
        <TextField
          label="Currency"
          value={invoice.currency ?? ""}
          onChange={(value) => updateField("currency", value)}
        />
        <TextField
          label="Email"
          type="email"
          value={invoice.email ?? ""}
          onChange={(value) => updateField("email", value)}
        />
        <TextField
          label="Phone"
          value={invoice.phone ?? ""}
          onChange={(value) => updateField("phone", value)}
        />
      </div>

      {invoice.line_items.length ? (
        <div className="mt-5 overflow-x-auto">
          <p className="text-sm font-semibold">Line item draft</p>
          <table className="mt-2 w-full min-w-[560px] border-collapse text-sm">
            <thead>
              <tr className="border-b border-line text-left">
                <th className="py-2 pr-4">Description</th>
                <th className="py-2 pr-4">Qty</th>
                <th className="py-2 pr-4">Unit price</th>
                <th className="py-2 pr-4">Amount</th>
              </tr>
            </thead>
            <tbody>
              {invoice.line_items.map((item, index) => (
                <tr className="border-b border-line" key={`${item.description}-${index}`}>
                  <td className="py-2 pr-4">{item.description}</td>
                  <td className="py-2 pr-4">{item.quantity ?? ""}</td>
                  <td className="py-2 pr-4">{item.unit_price ?? ""}</td>
                  <td className="py-2 pr-4">{item.amount ?? ""}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : null}

      <label className="mt-5 block text-sm font-semibold">
        Reviewer notes
        <textarea
          className="focus-ring mt-2 min-h-24 w-full rounded-lg border border-line px-3 py-2 text-sm"
          value={reviewerNotes}
          onChange={(event) => setReviewerNotes(event.target.value)}
        />
      </label>

      <button
        className="focus-ring mt-5 rounded-lg bg-accent px-4 py-2 text-sm font-semibold text-white hover:bg-teal-800"
        type="button"
        disabled={isSaving}
        onClick={handleSave}
      >
        {isSaving ? "Saving review..." : "Approve and save review"}
      </button>

      {review?.approved ? (
        <div className="mt-4 rounded-lg border border-teal-200 bg-teal-50 px-4 py-3 text-sm text-teal-950">
          Review saved. Status: {review.status}
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

function TextField({
  label,
  value,
  onChange,
  type = "text",
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  type?: string;
}) {
  return (
    <label className="block text-sm font-semibold">
      {label}
      <input
        className="focus-ring mt-2 w-full rounded-lg border border-line px-3 py-2 text-sm"
        type={type}
        step={type === "number" ? "0.01" : undefined}
        value={value}
        onChange={(event) => onChange(event.target.value)}
      />
    </label>
  );
}

const moneyFields = new Set<keyof EditableInvoice>(["subtotal", "tax", "total"]);

function parseOptionalNumber(value: string): number | null {
  if (value.trim() === "") {
    return null;
  }
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}

function numberValue(value: number | null | undefined): string {
  return value === null || value === undefined ? "" : String(value);
}

function normalizeInvoice(invoice: EditableInvoice): InvoiceData {
  return {
    ...invoice,
    vendor_name: blankToNull(invoice.vendor_name),
    invoice_number: blankToNull(invoice.invoice_number),
    invoice_date: blankToNull(invoice.invoice_date),
    due_date: blankToNull(invoice.due_date),
    currency: blankToNull(invoice.currency),
    email: blankToNull(invoice.email),
    phone: blankToNull(invoice.phone),
    line_items: invoice.line_items,
  };
}

function buildCorrections(
  original: InvoiceData,
  edited: EditableInvoice,
): Record<string, ReviewCorrection> {
  const normalizedEdited = normalizeInvoice(edited);
  const fields: (keyof Omit<InvoiceData, "line_items">)[] = [
    "vendor_name",
    "invoice_number",
    "invoice_date",
    "due_date",
    "subtotal",
    "tax",
    "total",
    "currency",
    "email",
    "phone",
  ];

  return fields.reduce<Record<string, ReviewCorrection>>((corrections, field) => {
    if ((original[field] ?? null) !== (normalizedEdited[field] ?? null)) {
      corrections[field] = {
        original: original[field] ?? null,
        corrected: normalizedEdited[field] ?? null,
      };
    }
    return corrections;
  }, {});
}

function blankToNull(value: string | null | undefined): string | null {
  const trimmed = value?.trim() ?? "";
  return trimmed ? trimmed : null;
}
