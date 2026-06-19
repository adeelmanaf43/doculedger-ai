# TESTING.md

## Testing principle

Every feature must be proven with tests or a recorded manual verification path. The MVP handles financial documents, so silent failures are unacceptable.

## Backend tests

Expected backend test command:

```bash
cd backend
pytest
```

Test areas:

- Health endpoint.
- Upload validation.
- Rejected file types.
- File size limits.
- Safe filename/path handling.
- OCR service success/failure.
- Rule-based extraction.
- Confidence scoring.
- CSV export mapping.
- Duplicate detection.
- Error responses.

## Frontend tests

Expected frontend commands after setup:

```bash
cd frontend
npm run lint
npm test
```

Manual frontend checks:

- Upload screen loads.
- Invalid file shows useful error.
- Valid file starts processing.
- Extraction result is displayed.
- Low confidence fields are visible.
- User can edit fields.
- User can save reviewed fields.
- CSV export downloads.
- Layout works on laptop and mobile widths.

## End-to-end MVP checks

Before calling the MVP ready:

- [ ] App starts locally without paid APIs.
- [ ] User can upload at least 10 sample invoices.
- [ ] Extracted fields are shown in review UI.
- [ ] Low-confidence fields are marked.
- [ ] Human correction works.
- [ ] Reviewed values are saved.
- [ ] QuickBooks CSV export works.
- [ ] Xero CSV export works.
- [ ] Generic CSV export works.
- [ ] Batch summary report works.
- [ ] Uploaded files follow retention/deletion rules.
- [ ] No secrets are committed.
- [ ] README setup instructions are correct.

## Codex testing instruction

After each coding task, Codex must report:

```text
Commands run:
Tests passed:
Manual checks:
Known failures:
Files changed:
Remaining risks:
```

