<!-- spec-review-kit:start -->
## Spec review — guardrails

This section is managed by [spec-review-kit](https://github.com/cramone/spec-review-kit). It restates the rules the kit's scripts (`docs_guard.py`, `compliance_coverage.py`) and slash commands (`/spec-audit-next`, `/spec-quality-audit`) enforce. Edit between the start/end markers only by re-running `/init-spec-review` — manual edits are overwritten.

### Source of truth

| What | Path |
|------|------|
| Spec (all contexts) | `{{SPEC_PATH}}/` |
| ADRs | `{{ADRS_PATH}}/` |
| Spec audits (one open per phase) | `{{REVIEW_PATH}}/spec-audit-<date>/INDEX.md` |
| Dependency gaps (SDK + code + infra) | `{{DEPGAPS_PATH}}/INDEX.md` |
| Compliance mapping | `{{COMPLIANCE_PATH}}/INDEX.md` |

Read the relevant spec files before implementing or reviewing any change that touches domain behavior, API contracts, or cross-context boundaries. Spec/ADR changes land in the same PR as the code change they describe.

<!-- strip-if-no-platform-check:start -->
### Spec-first phase — the only code consulted is `{{PLATFORM_REPO}}`

The application code (`src/`, `tests/`, infra) is not aligned to the spec, and the spec is being completed before the code is aligned to it. Until that changes:

- **Never read application code to decide, confirm or refute** a spec statement, an audit finding or a stored value. Where a statement depends on what the application does, the spec decides it.
- **`{{PLATFORM_REPO}}` is the one codebase that may be read.** Read its `CLAUDE.md` first. A capability it lacks is a platform gap for § Known deferred/partial work, never a weaker spec statement.
- A finding, note or worklist row that says "needs code check" against this repo is not a prerequisite. Decide it from the spec.
- Code alignment is its own later phase; § Known deferred/partial work is its starting list.
- **Before raising a new review finding, consult `{{DEPGAPS_PATH}}/INDEX.md`.** A proposal duplicating a known gap is recorded as `held-by: dependency-gaps/F0nn` in the finding file, not a new finding.
<!-- strip-if-no-platform-check:end -->

### When the spec and the code disagree, the spec wins

**The divergence is a defect in the code**, raised and scheduled like any other. `{{SPEC_PATH}}/` is a specification, not a description: where it states behaviour, that behaviour is what the system is required to do, whether or not it does it yet.

**A missing platform capability is the same kind of gap as a missing handler.** Write the spec as if the infrastructure exists and can be implemented properly later. The missing capability goes in `{{DEPGAPS_PATH}}/`, {{TRACKER_PHRASE}}, and § Known deferred/partial work — **never** into `{{SPEC_PATH}}/` as a weaker statement.

**Do not resolve a disagreement by editing either side quietly.** Correcting the spec to match code you happened to read is the same mistake as changing code to match a spec statement without the change being visible.

**Meta-rule: never "correct" the spec back to the deployed behaviour.** Every § Known deferred/partial work bullet describes a gap between spec and code; in every case the spec is correct and the code must catch up. Do not propose rewriting the spec to match what the code does today.

**The exception is a published integration event.** An integration event's `type` string is the filter key in every subscriber's policy, and its payload members are what subscribers parse. For these the spec states the **published** contract and the migration that would change it. **Every other stored value is stated as specified**: partition and sort keys, index names and shapes, aggregate-type strings, enum ordinals (pinned explicitly), snapshot and read-model members. Moving data already stored under another shape onto the specified one is a code-phase migration, recorded in § Known deferred/partial work and never in `{{SPEC_PATH}}/`.

### Spec files state the specified system — nothing else

`{{SPEC_PATH}}/` describes **what the system is specified to be**. Present tense, no history, no progress.

**Never write into a spec file:**

- **Change history** — "Corrected…", "this previously said…", strikethrough supersession, dates in heading text or anchors.
- **Citations to anything outside `docs/`** — review, finding, plan, workstream or backlog ids. An id is legitimate only if the thing it names is **defined inside `docs/`**. Point at the topic document and heading anchor instead.
- **Build or implementation status** — whether code exists, is wired, deployed, registered or provisioned.
- **Rationale, tradeoffs and rejected options** — belongs in `{{ADRS_PATH}}/`.
- **Recommendations, open questions and tracking** — "needs a decision from…", "⏳", "✓" columns, "raised as…", "tracked as…".
- **Notes addressed to a reader or an AI agent** — "treat this as authoritative", "don't propose anything shaped like this". A design caveat is not such a note — see test below.
- **Attribution** — who decided, and when.

### The caveat test

A caveat belongs in a spec file when it states a consequence of the **specified design** that holds for anyone implementing it correctly. It does not when it states the current state of the code, a known gap, or a recommendation.

| Belongs in the spec | Does not |
|---|---|
| A consequence of the design that every correct implementation must honour | Whether code exists, is wired or is deployed |
| A defaulted payload member must have its absent-meaning written down | "Treat the rest of this block as unverified" |
| An invariant stated once and referenced from its callers | What someone should do next |

**When a spec is wrong, fix the statement and delete the wrong one.** The diff is the history. A removed feature is simply absent from the spec.

**`.github/scripts/docs_guard.py` enforces these rules** over `docs/` (excluding `{{REVIEW_PATH}}/` and `{{COMPLIANCE_PATH}}/`), and CI runs it on every change to `docs/`. Run `python .github/scripts/docs_guard.py` before committing any spec or ADR change — every check is hard zero.

### Non-spec content has a home

| Content | Home |
|---|---|
| Why a decision was made; rejected options | `{{ADRS_PATH}}/` |
| Whether code exists, is wired or deployed | {{TRACKER_PHRASE}} · § Known deferred/partial work in this file |
| Review findings, drift, evidence | out-of-repo working notes |
| Spec audits — in-flight design findings | `{{REVIEW_PATH}}/spec-audit-<date>/INDEX.md`; docs-guard skips `{{REVIEW_PATH}}/`; a spec file never cites a finding |
| Dependency gaps | `{{DEPGAPS_PATH}}/INDEX.md` |
| Standards compliance mapping | `{{COMPLIANCE_PATH}}/INDEX.md`; docs-guard skips this folder |
| Open questions, remediation tracking | out-of-repo plans; a spec audit tracks its own in its `INDEX.md` + finding files |
| Deploy and ops checklists | out-of-repo runbooks |

**A fix that changes a rule this file restates updates the restatement in the same change.** Spec wins; this file follows it in the same commit.

**This file is not a spec file.** `CLAUDE.md` is agent instruction — build status, "do not rebuild this" guardrails and the reasoning behind them belong here, not in the spec.

### Review commands

- `/spec-quality-audit` — runs the sixteen-quality standing audit over `{{SPEC_PATH}}/` + `{{ADRS_PATH}}/`. Reports findings, decides mode (inline fix / open audit folder). Protocol at `{{REVIEW_PATH}}/spec-quality-audit.md`.
- `/spec-audit-next <date>` — works one unit of a spec-audit folder. One iteration per invocation. Mandatory dependency-gaps pre-flight; mandatory propagation sweep.

<!-- spec-review-kit:end -->
