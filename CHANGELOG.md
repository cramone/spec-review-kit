# Changelog

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
