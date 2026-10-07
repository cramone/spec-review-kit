# Spec review — audit tracker

Top-level index of every spec audit and review artifact. This folder is **outside docs-guard scope** — it carries citations, dates and review state that spec files cannot.

## Open audits

An audit is open until its `INDEX.md` shows zero `open` and zero `blocked` findings. Work the next unit via `/spec-audit-next <date>`; state persists in the audit folder across sessions.

| Audit | Phase | Scope | Status | Owner | Opened | Next action |
|---|---|---|---|---|---|---|
| _(none open)_ | | | | | | |

## Closed audits

Audits whose findings are all resolved (fixed, held, platform-gap, superseded, or wont-fix). Full folder contents are recoverable via `git log --all -- {{REVIEW_PATH}}/<folder>/`.

## Phase roadmap

Spec correctness is pursued across four audit phases, each its own `spec-audit-<date>/` folder:

| Phase | Scope | Why |
|---|---|---|
| **A** — spec-internal consistency | Cross-file restatements: shared rules vs per-unit statements; event / error / permission catalogues vs per-unit declarations; index inventories vs per-unit indexes; type / id strings; enum ordinals | Catches silent drift between spec files that neither docs-guard nor an ADR-spec matrix catches |
| **B** — scenarios coverage | Does `*.scenarios.md` demonstrate every invariant, error code and state transition in `*.write-model.md`? | Scenarios are the test oracle. Missing coverage = untestable rule |
| **C** — dark corners | Error codes declared but never returned; events declared but never consumed; permissions in vocabulary not granted / not required; state transitions reachable but never produced | Finds dead spec |
| **D** — external standards | RFCs, vendor service limits, domain standards cited by the spec | Confirms spec claims about external contracts match sources |

Each phase opens its own dated audit folder. Phases A → D in order; later phases may surface new findings for earlier phases to carry.

## Standing audits

Re-runnable audits that are not phase-bound. State lives in each audit's own file; a run opens a dated folder only when its finding count or propagation reach meets the audit's threshold.

| Audit | Scope | When to run |
|---|---|---|
| [`spec-quality-audit.md`](./spec-quality-audit.md) | `{{SPEC_PATH}}/` + `{{ADRS_PATH}}/` — the sixteen qualities a specification must have | Before merging a batch touching more than one spec/ADR file; weekly cadence; on-demand |

## How to resume work across sessions

Audits are durable across Claude sessions because the state lives in the audit folder, not in memory. To resume:

```
1. ls {{REVIEW_PATH}}/             # list open audit folders
2. cat {{REVIEW_PATH}}/README.md   # see which phase is active + its state
3. /spec-audit-next <date>         # work next unit; state resumes
```

Every `/spec-audit-next` iteration runs the mandatory dependency-gaps pre-flight (`{{DEPGAPS_PATH}}/INDEX.md` if present) and the mandatory in-commit propagation sweep. Both prevent regressions from one session's fix to another's.

## How to open a new audit

1. **Pick a date and phase.** Create `{{REVIEW_PATH}}/spec-audit-<YYYY-MM-DD>/`.
2. **Copy from `_template/`** — INDEX.md and finding template. See [`_template/README.md`](./_template/README.md).
3. **Run an agent sweep** to pre-populate findings. One agent per spec cluster is a good default.
4. **Verify a representative sample** of the agent's findings by direct spec read before trusting them. Agents produce false negatives on narrow greps.
5. **Add a row to § Open audits above.**
6. **Begin work via `/spec-audit-next <date>`.**

## How to close an audit

1. Confirm `INDEX.md` shows zero `open`, zero `blocked`. All findings must be `fixed`, `held`, `platform-gap`, `superseded` or `wont-fix`.
2. Confirm `python .github/scripts/docs_guard.py` passes.
3. If any findings held platform work, confirm they were extracted to `{{DEPGAPS_PATH}}/` with crosslinks from affected ADRs.
4. Move the audit's row from § Open audits to § Closed audits above, with closed date and a one-line residue note.
5. Decide whether to keep the folder in-repo (useful if findings are referenced later) or delete it (reduces repo size — history preserved by git).
