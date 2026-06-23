"use client";

import type { ChangeEvent } from "react";
import type { UploadResponse } from "@/lib/types";

type UploadPanelProps = {
  selectedFile: File | null;
  upload: UploadResponse | null;
  isUploading: boolean;
  error?: string | null;
  onFileChange: (file: File | null) => void;
  onUpload: () => void;
};

export function UploadPanel({
  selectedFile,
  upload,
  isUploading,
  error,
  onFileChange,
  onUpload,
}: UploadPanelProps) {
  function handleFileChange(event: ChangeEvent<HTMLInputElement>) {
    onFileChange(event.target.files?.[0] ?? null);
  }

  return (
    <section className="rounded-lg border border-line bg-panel p-5 shadow-sm">
      <div className="flex flex-col gap-1">
        <p className="text-sm font-semibold uppercase tracking-wide text-accent">
          Upload
        </p>
        <h2 className="text-xl font-semibold">Add an invoice or receipt</h2>
        <p className="text-sm leading-6 text-muted">
          PDF, PNG, JPG, or JPEG. Default backend limit is 10 MB.
        </p>
      </div>

      <div className="mt-5 grid gap-3">
        <input
          className="focus-ring w-full rounded-lg border border-line bg-white px-3 py-3 text-sm"
          type="file"
          accept=".pdf,.png,.jpg,.jpeg,application/pdf,image/png,image/jpeg"
          onChange={handleFileChange}
        />
        {selectedFile ? (
          <p className="text-sm text-muted">Selected: {selectedFile.name}</p>
        ) : null}
        <button
          className="focus-ring w-fit rounded-lg bg-accent px-4 py-2 text-sm font-semibold text-white hover:bg-teal-800"
          type="button"
          disabled={!selectedFile || isUploading}
          onClick={onUpload}
        >
          {isUploading ? "Uploading..." : "Upload document"}
        </button>
      </div>

      {upload ? (
        <div className="mt-4 rounded-lg border border-teal-200 bg-teal-50 px-4 py-3 text-sm text-teal-950">
          <p className="font-semibold">Upload complete</p>
          <p className="mt-1 break-all">Document ID: {upload.document_id}</p>
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
