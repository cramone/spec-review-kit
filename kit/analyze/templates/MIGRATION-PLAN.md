# Migration plan — `{{ANALYSIS_DATE}}`

Proposed mapping from existing content to spec-review-kit slots. Read-only output of `/init-spec-review analyze`. No file has been moved. Review the table, correct what the classifier got wrong, then run `/init-spec-review migrate` to apply decisions interactively.

**Project:** `{{PROJECT_NAME}}` · **Profile:** `{{PROFILE}}` · **Scope:** `{{ANALYZE_SCOPE}}`

## Summary

| Action | Count |
|---|---:|
| `move` | _(fill in)_ |
| `move+trim` | _(fill in)_ |
| `split` | _(fill in)_ |
| `merge` | _(fill in)_ |
| `keep` | _(fill in)_ |
| `delete` | _(fill in)_ |
| `tbd` | _(fill in)_ |
| **Total files** | _(fill in)_ |

## Rows

| Source | Target slot | Action | Confidence | Notes |
|---|---|---|---|---|
| _(fill in one row per file in scope)_ | _(slot path or `n/a`)_ | _(action)_ | _(high/medium/low)_ | _(classifier reasoning in one line)_ |

## Split groups

A source classified as `split` names its target slots here, one row per target. The migrate step walks each group's source once and asks the user to assign headings or paragraphs to each named target.

| Source | Targets | Notes |
|---|---|---|
| _(fill in)_ | _(comma-separated target slots)_ | _(classifier hint — "headings `## HTTP`, `## Errors`, `## State` → api, error-catalog, write-model respectively")_ |

## Merge groups

Sources that classify to the same target with `merge` action. The migrate step prompts the user per group to concatenate / dedupe / reconcile.

| Target slot | Sources | Notes |
|---|---|---|
| _(fill in: slot path)_ | _(comma-separated source paths)_ | _(classifier hint on reconciliation strategy)_ |

## Low-confidence rows

Rows marked `tbd` or `low` confidence need human judgment before migrate runs. The migrate step pauses on each and asks the user to pick a target.

| Source | Candidate slots | Why unclear |
|---|---|---|
| _(fill in)_ | _(comma-separated plausible slots)_ | _(what signals conflict)_ |

## Delete candidates

Files proposed for delete. Migrate prompts the user to confirm each before running `git rm`.

| Source | Reason |
|---|---|
| _(fill in)_ | _(obsolete / superseded / empty / duplicate — one of the forced-delete signals)_ |

---

## How to use this plan

1. Read it top to bottom. Correct any row where the classifier's action or target slot is wrong — edit the row inline. Edits here propagate to migrate.
2. For `tbd` rows, decide the action and target slot. Add a note to the Notes column so migrate skips the prompt.
3. For `split` rows, confirm the target slots or add more.
4. For `merge` rows, confirm the merge strategy in Notes.
5. For `delete` rows, strike through any you want to keep (the migrate step treats non-struck `delete` rows as user-confirmed).
6. Run `/init-spec-review migrate`.

## Guardrails observed

- `move+trim` only drops kit-forbidden content (dates, change history, attribution, build-status prose). It does not rewrite design statements.
- `split` is a text split, not a rewrite. Headings or paragraphs move to the named target as-is.
- `merge` is append + user-confirmed dedupe. The migrate step does not rewrite without approval.
- No row causes a `delete` without an explicit y/N prompt.
