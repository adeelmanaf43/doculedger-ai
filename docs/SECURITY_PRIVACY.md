# SECURITY_PRIVACY.md

## Security position

DocuLedger processes sensitive financial documents. Security and privacy must be designed into the MVP, even if the first version is simple.

## Required controls for MVP

- Validate file type.
- Validate file size.
- Sanitize filenames.
- Store files outside public frontend paths.
- Auto-delete uploads based on retention settings.
- Never log full document text.
- Never log full invoice data in production.
- Use environment variables for secrets.
- Add `.env.example`, but never commit `.env`.
- Keep paid external APIs disabled by default.
- Require explicit opt-in before sending sensitive document text to external providers.

## Upload rules

Allowed initial file types:

- PDF
- PNG
- JPG/JPEG

Reject:

- executables
- scripts
- archives
- unknown MIME types
- files over configured size limit
- filenames with path traversal patterns

## External provider rule

Paid providers must not be active unless:

1. Environment variable enables the provider.
2. API key is configured.
3. Usage limit is configured.
4. Documentation explains what data is sent.
5. Tests confirm local/free fallback still works.

## Audit events

Log metadata-only audit events for:

- document uploaded
- OCR completed
- extraction completed
- field corrected
- invoice reviewed
- CSV exported
- report generated
- source file deleted
- external provider used
- accounting sync attempted

Do not log full invoice contents.

## Retention policy

MVP default:

- Store uploaded source files temporarily.
- Keep extracted/reviewed structured data for history.
- Allow configurable source-file deletion window.

Suggested environment variables:

```text
DOCULEDGER_FILE_RETENTION_HOURS=24
DOCULEDGER_MAX_UPLOAD_MB=10
DOCULEDGER_EXTERNAL_AI_ENABLED=false
```

## Security checklist before demo

- [ ] `.env` is ignored by Git.
- [ ] `.env.example` contains no real secrets.
- [ ] Upload validation works.
- [ ] Large files are rejected.
- [ ] Dangerous filenames are rejected/sanitized.
- [ ] Full OCR text is not printed in logs.
- [ ] External provider mode is disabled by default.
- [ ] Source file deletion path is tested.
- [ ] Error messages do not expose internal paths or secrets.

