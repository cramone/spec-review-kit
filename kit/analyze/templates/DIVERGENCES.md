# Divergences — `{{ANALYSIS_DATE}}`

Existing files that do not fit any kit slot. Each row names the file, the signals the classifier used, and a recommendation.

**Project:** `{{PROJECT_NAME}}` · **Profile:** `{{PROFILE}}`

A divergence is **not** a defect. These files may belong in the repo but outside the kit's spec structure.

## Kept-in-place by design

Files the classifier recognised as kit-irrelevant. These stay where they are; migrate does not touch them.

| Source | Signal | Reason |
|---|---|---|
| `README.md` | repo-root readme | Project introduction; not kit content |
| `CONTRIBUTING.md` | contribution guide | Developer onboarding; not kit content |
| `CHANGELOG.md` | release notes | Not kit content |
| _(fill in: more)_ | _(signal)_ | _(reason)_ |

## Operator / runbook content

Content addressed to someone operating the system now, not describing the designed behaviour. Belongs out-of-repo (deploy-runbook, oncall playbook) or in a dedicated `runbooks/` folder — never in `{{SPEC_PATH}}/`.

| Source | Signal | Recommendation |
|---|---|---|
| _(fill in)_ | _(e.g. "contains current access credentials", "names on-call rotation")_ | _(move to `runbooks/` or an out-of-repo location)_ |

## Meeting / review notes

Dated notes that read like meeting minutes or review scratch — not design. Belongs in `{{REVIEW_PATH}}/` (which docs-guard excludes) or deleted.

| Source | Signal | Recommendation |
|---|---|---|
| _(fill in)_ | _(e.g. "date in heading", "attendee list")_ | _(archive to `{{REVIEW_PATH}}/notes/` or delete)_ |

## Code-heavy files

Files that are predominantly code examples with little specification prose. May belong under a `cookbook/` or `examples/` folder, or be inlined into the module's `api.md`.

| Source | Signal | Recommendation |
|---|---|---|
| _(fill in)_ | _(e.g. "fenced blocks exceed 60% of lines")_ | _(move to `examples/` or embed into unit `api.md`)_ |

## Ambiguous — needs manual review

Files that produced conflicting signals. The classifier could not pick a slot with any confidence.

| Source | Candidate interpretations | Why ambiguous |
|---|---|---|
| _(fill in)_ | _(e.g. "architecture + runbook + ADR")_ | _(e.g. "mixes design, deployment state, and historical context in one file")_ |

---

## How to use this report

- Each row is a judgment call. The classifier does not auto-delete or auto-move divergences.
- During migrate, every divergence is skipped by default (action `keep`). If you want a divergence moved or deleted, edit `MIGRATION-PLAN.md` and change its action.
- A divergence left in place for several analyze runs is a candidate for a `runbooks/` or `notes/` folder — a dedicated home outside the spec tree keeps the kit's structure clean.
