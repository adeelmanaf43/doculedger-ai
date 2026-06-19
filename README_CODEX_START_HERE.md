# README_CODEX_START_HERE.md

Use these files before writing application code.

## How to start with Codex

1. Create a new GitHub/local repo named `doculedger`.
2. Put all files from this starter pack at the repo root.
3. Open the repo in Codex.
4. Start with `prompts/00_START_PROJECT_WITH_CODEX.md`.
5. Do not ask Codex to build the full product in one prompt.

## Recommended first Codex command

```text
Read AGENTS.md, PROJECT_BRIEF.md, docs/ARCHITECTURE.md, docs/ROADMAP.md, docs/TASKS.md, docs/TESTING.md, docs/SECURITY_PRIVACY.md, docs/DECISIONS.md, and docs/ENVIRONMENT.md.

Do not write code yet.

First explain:
1. Your understanding of DocuLedger
2. The MVP scope
3. The architecture you will use
4. The first milestone
5. The first 5 implementation tasks
6. Risks and assumptions

Wait for my approval before creating or editing code files.
```

## Daily workflow

Every work session should follow this pattern:

1. Pick one task from `docs/TASKS.md`.
2. Ask Codex to inspect relevant files.
3. Ask Codex to plan.
4. Approve or correct the plan.
5. Let Codex implement.
6. Run tests.
7. Fix failures.
8. Ask Codex to review its own diff.
9. Commit.

## Do not do this

Avoid prompts like:

```text
Build complete DocuLedger.
```

Use task prompts like:

```text
Build the backend upload endpoint only. Follow AGENTS.md. Add tests. Done when a PDF/image upload is validated, saved in local temp storage, and metadata is returned.
```

