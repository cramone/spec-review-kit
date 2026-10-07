# Dependency gaps

Workstreams tracking gaps between the specification and the deployed system — platform SDK capabilities missing, infrastructure not yet provisioned, code not yet aligned to the spec. Each theme is a folder with its own INDEX.md; each gap is a file `Fnnn-<slug>.md`.

A finding raised in a spec audit that duplicates an existing gap is held: the finding's file carries `held-by: dependency-gaps/Fnnn`. The audit protocol consults this register as part of every iteration's pre-flight.

## Themes

| Theme | Scope |
|---|---|
| _(fill in: theme name)_ | _(what gaps this theme carries — e.g. "SDK capabilities missing", "infrastructure not provisioned", "code-to-spec divergence")_ |

## Gap register

The register is populated as spec audits raise findings that match existing gaps or as new gaps are identified. Each entry names its id, theme, title, and the workstream carrying delivery.

| Id | Theme | Title | Workstream |
|---|---|---|---|

_(fill in as gaps accrue. The register is a convenience view over the per-theme INDEX.md files; those are the source of truth.)_

## Pre-flight procedure (consulted by every `/spec-audit-next` iteration)

1. Pick 2–3 keywords from the candidate finding's claim / problem / location.
2. Grep `dependency-gaps/**/*.md` for each keyword.
3. For every hit, open the gap file and read its `## Detection signals` section.
4. A match on any detection signal means the gap owns the finding — set `held-by: dependency-gaps/Fnnn` on the finding and record the match.

## Audit history

A row per closed audit; the row names the audit folder (now deleted or kept) and the dependency gaps it created or confirmed. The authoritative log; the audit folder's `INDEX.md` is deleted or kept per the close procedure.

| Audit | Closed | Findings | Created gaps | Notes |
|---|---|---|---|---|

_(fill in on first audit close.)_
