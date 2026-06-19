# AGENTS.md

## Project identity

DocuLedger is a free-first, review-assisted invoice and receipt processing product for small bookkeepers, CPA firms, ecommerce operators, property managers, and small businesses that manually process invoices.

The first sellable version must help a user:

1. Upload invoices or receipt PDFs/images.
2. Extract text with free/local OCR first.
3. Extract bookkeeping fields with rule-based logic first.
4. Show confidence scores and warnings.
5. Let a human review and correct extracted fields.
6. Export clean CSV for QuickBooks, Xero, and generic Excel workflows.
7. Produce a simple client-ready summary report.

This is not autonomous bookkeeping. Always position the product as review-assisted automation.

## Non-negotiable business constraints

- Build free-first.
- Do not require OpenAI, Claude, Google Vision, Stripe, QuickBooks, Xero, paid hosting, or paid storage for the MVP.
- Keep paid providers behind interfaces/adapters and disabled by default.
- Do not remove CSV export even after direct accounting integrations are added.
- Prioritize a sellable workflow over fancy SaaS features.
- The first client offer is a free 20-invoice trial, then a paid setup fee and monthly processing retainer.

## Recommended stack

- Backend: FastAPI, Python, Pydantic, pytest.
- Frontend: Next.js, TypeScript, TailwindCSS, Shadcn/UI.
- OCR: Tesseract plus PDF/image preprocessing.
- Extraction: rule-based extractor first; paid LLM extractor later behind feature flags.
- Database: SQLite local MVP; Postgres/Supabase later.
- Storage: local temporary storage first; R2/S3 later.
- Reports: CSV first; PDF summary report later.

## Engineering rules

- Inspect the repository before editing.
- Keep changes small and scoped to the requested task.
- Do not rewrite large parts of the project unless explicitly asked.
- Do not add production dependencies without explaining why.
- Never hard-code secrets, API keys, tokens, credentials, or client financial data.
- Use environment variables for provider selection and external integrations.
- Keep code modular: API routes, schemas, services, adapters, exporters, and tests should be separated.
- Prefer simple, readable implementation over over-engineered abstractions.
- Add type hints in Python and strong types in TypeScript.
- Validate file type, size, upload path, and dangerous filenames.
- Handle errors with useful messages and safe logs.
- Update relevant docs when setup, commands, architecture, or behavior changes.

## Privacy and security rules

- Uploaded source files are sensitive financial documents.
- Store the minimum data needed for processing, history, exports, and reports.
- Auto-delete uploaded source files according to configurable retention rules.
- Do not send full financial documents to external APIs unless explicitly enabled and documented.
- Add audit logs for upload, extraction, review correction, export, delete, and sync actions.
- Use signed URLs and lifecycle deletion when object storage is added.
- Never log full document text or full extracted financial data in production logs.

## Repository structure target

```text
doculedger/
  backend/
    app/
      api/
      core/
      schemas/
      services/
        ocr/
        extractors/
        categorization/
        exporters/
        reports/
        storage/
      tests/
  frontend/
    app/
    components/
    lib/
  docs/
  demo/
  sales/
  prompts/
  AGENTS.md
  README.md
```

## Validation expectations

After every implementation task:

1. Run relevant tests.
2. Run lint/type checks if configured.
3. Manually verify the changed workflow when possible.
4. Review the diff for unrelated changes.
5. Summarize files changed, commands run, tests passed, and remaining risks.

## Definition of done

A feature is done only when:

- It works end to end in free/local mode.
- It does not require paid services.
- It has focused tests or a clearly documented manual verification path.
- It handles invalid inputs safely.
- It follows the review-assisted workflow.
- Relevant documentation is updated.
- No unrelated files are changed.

## Codex behavior

For large or unclear work, plan before coding. Ask clarifying questions only when the answer would materially change implementation.

For each feature, use this sequence:

1. Read relevant files.
2. Explain current understanding.
3. Propose a small implementation plan.
4. Implement after approval.
5. Test and fix failures.
6. Review the diff.
7. Update docs/task status.

