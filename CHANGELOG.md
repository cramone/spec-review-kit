# Changelog

## 0.3.0 — analyze + migrate

Classify an existing repo's content against the kit's slots; migrate interactively with full backup and per-row y/N approval.

- `kit/analyze/taxonomy.md` — classification reference: slot catalogue, filename / content / path signals, action vocabulary, scope rules
- `kit/analyze/templates/MIGRATION-PLAN.md` — proposed source → slot mapping with action + confidence + split/merge groups
- `kit/analyze/templates/GAPS.md` — kit slots the profile expects but the repo has no content for
- `kit/analyze/templates/DIVERGENCES.md` — files kept in place by design (operator / runbook / meeting-notes / code-heavy)
- `kit/analyze/templates/GUARD-BASELINE.md` — pre-migration `docs_guard` state
- `/init-spec-review analyze` — scan `docs/**`, `README.md`, `CONTRIBUTING.md`, `src/**/README.md`, top-level `*.md`; emit four reports under `.spec-review-analysis-<date>/`. Zero file moves.
- `/init-spec-review migrate` — walk the plan interactively (propose-only, every move needs y/N); back up to `.spec-review-backup-<date>/`; log every decision to `MIGRATION-LOG.md`. Hand off to `/spec-quality-audit` for remaining `docs_guard` hits.

## 0.2.0 — spec scaffold

Scaffold a `docs/spec/` tree at install time. Four profiles cover common shapes; shared concerns menu picks the cross-cutting files that fit the system.

- `kit/scaffold/profiles/` — four profiles: `ddd-event-sourced` (deep), `ddd-crud`, `api-service`, `library` (shallow — manifest + minimal starters)
- `kit/scaffold/shared/` — 14 cross-cutting stubs (api-conventions, error-catalog, event-store, auth, saga patterns, audit, cascade, retention, privacy, erasure, preservation, operations, cross-aggregate rules, contracts, extension points)
- `kit/scaffold/adrs/` — ADR README + starter `0001-architecture-and-stack.md`
- `kit/scaffold/dependency-gaps/` — INDEX + `_template/` for themes and findings
- `kit/scaffold/compliance/` — INDEX + `_template/` for standards mapping
- `[scaffold]` + `[tracker]` sections added to `.spec-review.toml`; tracker reference phrase substitutes into CLAUDE.md
- Scaffold subcommand `/init-spec-review scaffold`; reconfigure updates tracker without re-scaffolding
- Every scaffolded file passes `docs_guard` on first install — placeholders use italic `_(fill in: ...)_` prose rather than TODO markers

## 0.1.0 — initial extraction

Extracted from `mgq-magiq-media` after a multi-month spec-audit cycle. First portable release.

- `docs_guard.py` — ten checks, config-driven via `.spec-review.toml`
- `compliance_coverage.py` — three checks, config-driven, no-op when disabled
- `/spec-audit-next` + `/spec-quality-audit` slash commands, placeholder-driven
- `docs/review/` scaffold with `_template/` + 16-quality protocol
- `docs-guard.yml` CI workflow, conditional compliance step
- `CLAUDE.md § Spec review` guardrail section, idempotent marker-fenced
- `init-spec-review` skill — install / update / reconfigure / uninstall
