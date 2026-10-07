# Gaps — `{{ANALYSIS_DATE}}`

Kit slots the installed profile expects to exist, but the current repo has no content for. Each gap is a stub the scaffold step would have written for a fresh repo; because the repo already has some content, the stub is not written automatically.

**Project:** `{{PROJECT_NAME}}` · **Profile:** `{{PROFILE}}`

## Shared concerns not covered

| Slot | Required by profile | Scaffold would write | Recommendation |
|---|---|---|---|
| _(e.g. `docs/spec/shared/error-catalog.md`)_ | required | yes | Run the scaffold step (restricted to this slot) via `/init-spec-review scaffold --slot=shared/error-catalog` after migration, then fill in |

## Architecture files not present

| Slot | Scaffold would write | Recommendation |
|---|---|---|
| _(e.g. `docs/spec/architecture/bounded-contexts.md`)_ | yes | Run the scaffold step for this slot post-migration |

## Per-unit files not present

Sub-set of each top-level unit (context / resource / module) that is missing a file the profile expects.

| Unit | Missing file(s) | Recommendation |
|---|---|---|
| _(fill in: unit name)_ | _(e.g. `<unit>.scenarios.md`)_ | _(scaffold the missing file; fill in post-migration)_ |

## ADR coverage

| Topic | Spec cites it | ADR exists | Recommendation |
|---|---|---|---|
| _(topic)_ | _(yes / no)_ | _(yes / no — ADR path)_ | _(write ADR / cite existing / drop citation)_ |

## Dependency-gaps register

| Theme | Expected by migration | Exists | Recommendation |
|---|---|---|---|
| _(fill in: theme name — e.g. `security`, `platform-capabilities`)_ | _(yes if migration surfaced known gaps)_ | _(yes / no)_ | _(create folder from `_template/`)_ |

## Compliance mapping

| Standard | Cited in spec | Mapping file exists | Recommendation |
|---|---|---|---|
| _(fill in: standard — e.g. ISO 15489)_ | _(yes / no)_ | _(yes / no)_ | _(create from `_template/standard-template.md`)_ |

---

## How to use this report

- Each gap is an invitation, not a mandate. Many gaps are expected if the system does not have the concern (e.g. a non-event-sourced system has no `event-store-and-messaging.md`).
- A gap under "required by profile" is the kit's opinion on what the profile needs. If the profile is wrong for this system, change the profile in `.spec-review.toml` and re-run analyze.
- Gaps are addressed after migration: run migrate first, then revisit this list and either scaffold the missing slot or document in `CLAUDE.md § Known deferred/partial work` why it is deliberately absent.
