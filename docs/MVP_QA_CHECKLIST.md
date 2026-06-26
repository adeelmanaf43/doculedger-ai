# DocuLedger MVP QA Checklist

Use this before recording a demo or committing portfolio polish.

## Backend Health

- [ ] Start FastAPI locally.
- [ ] Open `/health`.
- [ ] Confirm `status` is `ok`.
- [ ] Confirm no paid providers are required.

## Upload

- [ ] Upload a PDF.
- [ ] Upload a PNG.
- [ ] Confirm unsupported files are rejected.
- [ ] Confirm oversized files are rejected.
- [ ] Confirm response returns `storage_key`, not an absolute path.

## Processing

- [ ] Process a text-based PDF.
- [ ] Process an image with OCR when Tesseract is installed.
- [ ] Confirm scanned PDF limitation returns a warning instead of crashing.
- [ ] Confirm response includes confidence scores and warnings.
- [ ] Confirm full raw text is not returned by default.

## Review Workflow

- [ ] Save an approved review.
- [ ] Retrieve the saved review.
- [ ] Confirm approved reviews return `status=reviewed`.
- [ ] Confirm unapproved reviews return `status=review_required`.
- [ ] Confirm missing documents return safe 404 responses.

## CSV Export

- [ ] Export Generic CSV after approval.
- [ ] Export QuickBooks-style CSV after approval.
- [ ] Export Xero-style CSV after approval.
- [ ] Confirm unreviewed invoices cannot be exported.
- [ ] Confirm missing values export as blank cells.
- [ ] Confirm CSV output does not expose absolute paths.

## Frontend Workflow

- [ ] Frontend starts at `http://localhost:3000`.
- [ ] Backend connection status appears.
- [ ] Upload, process, review, and export steps work in order.
- [ ] Export buttons are disabled before approval.
- [ ] Errors are shown clearly.

## Error Handling

- [ ] Backend-not-running error is clear.
- [ ] Invalid upload error is clear.
- [ ] Failed OCR error is clear.
- [ ] Missing review/export errors are clear.

## Privacy And Security

- [ ] No real invoices are included in demo data.
- [ ] No `.env` files are committed.
- [ ] No secrets are hard-coded.
- [ ] No full OCR/invoice text is logged unnecessarily.
- [ ] No sensitive data is stored in browser localStorage.

## Documentation

- [ ] Root README explains the project honestly.
- [ ] Backend README includes setup, endpoints, tests, OCR, SQLite, and CSV export.
- [ ] Frontend README includes setup, environment variable, workflow, build, and lint.
- [ ] Demo workflow is easy to follow.
- [ ] Portfolio case study is realistic.

## GitHub Readiness

- [ ] `python -m pytest` passes from `backend/`.
- [ ] `npm run build` passes from `frontend/`.
- [ ] `npm run lint` passes from `frontend/`.
- [ ] `git diff --check` has no whitespace errors.
- [ ] Commit excludes local DB, storage, caches, and `.env` files.
