# Changelog

## 0.1.0 — initial extraction

Extracted from `mgq-magiq-media` after a multi-month spec-audit cycle. First portable release.

- `docs_guard.py` — ten checks, config-driven via `.spec-review.toml`
- `compliance_coverage.py` — three checks, config-driven, no-op when disabled
- `/spec-audit-next` + `/spec-quality-audit` slash commands, placeholder-driven
- `docs/review/` scaffold with `_template/` + 16-quality protocol
- `docs-guard.yml` CI workflow, conditional compliance step
- `CLAUDE.md § Spec review` guardrail section, idempotent marker-fenced
- `init-spec-review` skill — install / update / reconfigure / uninstall
