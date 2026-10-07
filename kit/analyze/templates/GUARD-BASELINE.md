# docs-guard baseline — `{{ANALYSIS_DATE}}`

Current state of the repo against `docs_guard.py` **before** migration. Captures the pre-migration hit count per check as the baseline the user is working down from.

**Project:** `{{PROJECT_NAME}}`

## Current state

```
{{GUARD_OUTPUT}}
```

## Per-check totals

| Check | Hits | Scope |
|---|---:|---|
| `citations` | _(count)_ | `docs/` |
| `build-status` | _(count)_ | `{{SPEC_PATH}}/` |
| `dates` | _(count)_ | `{{SPEC_PATH}}/` |
| `editorial` | _(count)_ | `{{SPEC_PATH}}/` |
| `future-work` | _(count)_ | `{{SPEC_PATH}}/` |
| `backcompat` | _(count)_ | `{{SPEC_PATH}}/` |
| `links` | _(count)_ | `docs/` |
| `references` | _(count)_ | `{{SPEC_PATH}}/` |
| `truncation` | _(count)_ | `docs/` |
| `structure` | _(count)_ | `docs/` |

## Hits by file

Top offenders. Not an exhaustive list — the raw output above is authoritative.

| File | Total hits | Dominant check |
|---|---:|---|
| _(fill in: path)_ | _(count)_ | _(e.g. `editorial`, `dates`)_ |

## Expected trajectory

Migration itself does not reduce guard hits — it only re-organises files. Hit reduction happens via:

1. **`move+trim`** actions during migrate drop known-forbidden prose (change history, dates, attribution) as part of the move.
2. **`/spec-quality-audit`** run after migrate addresses remaining hits — either inline (if ≤ 5) or by opening a dated audit folder.
3. CLAUDE.md's guardrail section (installed with the kit) governs every subsequent edit; new content lands clean.

## Hard-zero target

`docs_guard` is a hard-zero check in CI. Until the baseline reaches zero, CI blocks any `docs/` change on branches that `docs-guard.yml` watches. For an existing repo mid-migration, consider:

- Running the workflow in `workflow_dispatch`-only mode until baseline hits zero
- Or: branching the migration (`migration/spec-review-kit-{{ANALYSIS_DATE}}`) so CI gates don't block `develop` until the migration lands

Record the chosen strategy in `MIGRATION-LOG.md` once migrate runs.
