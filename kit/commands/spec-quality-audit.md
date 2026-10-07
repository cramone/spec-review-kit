---
description: Run the standing spec quality audit over {{SPEC_PATH}}/ + {{ADRS_PATH}}/. Mechanical pre-flight (docs_guard) then semantic walk of the sixteen qualities. Reports findings, decides mode (inline fix / open audit folder), appends a Pass log row.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash(python .github/scripts/docs_guard.py:*), Bash(python3 .github/scripts/docs_guard.py:*), Bash(python .github/scripts/compliance_coverage.py:*), Bash(python3 .github/scripts/compliance_coverage.py:*), Bash(git log:*), Bash(git diff:*), Bash(git status:*), Bash(ls:*), Bash(mkdir:*), Bash(date:*), Bash(cp:*)
---

# /spec-quality-audit

Executes `{{REVIEW_PATH}}/spec-quality-audit.md`. One pass per invocation. Audit protocol is the source of truth; this command is the executor.

## Dispatch — which mode

Read `$ARGUMENTS`:

| Argument | Meaning |
|---|---|
| empty | **Full pass.** Pre-flight + all sixteen qualities. |
| `preflight` | Mechanical only. docs_guard<!-- compliance-step-start --> + compliance_coverage<!-- compliance-step-end -->. Report and stop. |
| `Q<n>` or `Q<n>,Q<m>,…` (e.g. `Q1,Q9,Q16`) | Semantic walk restricted to the named qualities. Pre-flight still runs first. |
| `--since <ref>` | Scope grep walks to files changed since `<ref>` (git). Pre-flight unchanged. |

## Bindings

- **Audit protocol:** `{{REVIEW_PATH}}/spec-quality-audit.md`
- **Scope:** `{{SPEC_PATH}}/**/*.md` for all sixteen qualities; `{{ADRS_PATH}}/**/*.md` for Q1, Q3, Q4, Q5, Q7, Q9, Q15 per the protocol
- **Guardrail:** `CLAUDE.md` § "Spec files state the specified system"
- **Out of scope for the audit:** `{{REVIEW_PATH}}/`, `{{COMPLIANCE_PATH}}/`, `{{DEPGAPS_PATH}}/`, `docs/reports/`
<!-- strip-if-no-platform-check:start -->
- **Code reads:** none; `{{PLATFORM_REPO}}` only if a quality's semantic walk needs code evidence (CLAUDE.md § Spec-first phase)
<!-- strip-if-no-platform-check:end -->

## Protocol

### 0. Mechanical pre-flight — hard zero required

Run both scripts. If either exits non-zero, print the hits and **stop** — fix hits before the semantic walk.

```bash
python .github/scripts/docs_guard.py
<!-- compliance-step-start -->
python .github/scripts/compliance_coverage.py
<!-- compliance-step-end -->
```

Record totals for the Pass log row.

### 1. Semantic walk — per quality

Walk the quality set per `$ARGUMENTS` (default: all sixteen). Each quality's grep commands live under its § Walk heading in `{{REVIEW_PATH}}/spec-quality-audit.md`. For each quality:

1. Run the quality's grep(s). Capture hits.
2. For a reading-only quality (Q2, Q3, Q4, Q5, Q7, Q11, Q13, Q15), sample per the protocol:
   - Q2 — five random spec files, five random `##` sections each
   - Q4 — five aggregates (or equivalent top-level units), every stored-value table
   - Q5 — five events (or equivalent payload-bearing records), every nullable member and enum
   - Q11 — every spec file's first `## Overview` or opening paragraphs
   - Q13 — five invariants from one unit's `*.write-model.md` § Invariants, confirm scenario coverage
   - Q15 — every ADR changed in the last 14 commits touching `{{ADRS_PATH}}/`, confirm spec rows in the ADR-spec matrix agree
3. For each hit, apply the quality's test (named in the protocol's § Walk).
4. Record each finding as `(quality, file:line, quote, proposed rewrite)`.

A hit that is a false positive (grep caught a legitimate use) is recorded and ignored — do not file it as a finding.

### 2. Decide mode

Count findings. Apply the audit's Running the audit table:

| Count | Mode | Action |
|---|---|---|
| 0 | pass | Add row to § Pass log, exit |
| 1–5 and single-file | inline | Propose each fix as an Edit; apply only after user confirms the batch; add row |
| 6+ or any multi-file propagation | folder | Open `{{REVIEW_PATH}}/spec-audit-<today>-quality/`, copy from `_template/`, write one finding file per hit, add row with folder name |

**Any** finding whose fix spans multiple spec files opens a folder regardless of count — propagation needs the audit protocol (`/spec-audit-next` iterates it).

### 3. Act

- **inline:** emit the Edit diffs to the user. Do not auto-apply. Wait for confirmation.
- **folder:** scaffold the folder, write finding files per `FINDING-template.md` shape, populate the folder's `INDEX.md` with § Work order rows, add a row to `{{REVIEW_PATH}}/README.md` § Open audits.

### 4. Pass log

Edit `{{REVIEW_PATH}}/spec-quality-audit.md` § Pass log. Append one row:

```
| <today> | <cadence|pre-merge|on-demand> | <pass|N hits> | <N findings> | <inline|N> | <none|<folder>> |
```

Keep the rolling tail at twenty rows. Older rows drop off; git preserves the trail.

### 5. Re-run docs-guard

Final verification that any inline edits did not introduce new mechanical hits. If any check now fails, back out the inline edit and raise a finding instead.

```bash
python .github/scripts/docs_guard.py
```

### 6. Report

Print a terse summary:

```
PRE-FLIGHT  <pass|FAIL>
SEMANTIC    Q1:<n> Q2:<n> … Q16:<n>  (total <N>)
MODE        <pass|inline|folder>
ACTION      <none|<N edits proposed>|<folder opened: path>>
PASS LOG    appended
```

Stop. One pass per invocation. The user re-invokes to run another pass, or runs `/spec-audit-next <date>-quality` to work a folder opened by this pass.

## Notes

- **No batching.** One pass per invocation. If the user asks for multiple cadence runs, they re-invoke.
- **Mechanical first.** A failing pre-flight blocks the semantic walk; the hits are the defects the semantic pass does not need to re-raise.
- **Spec wins.** CLAUDE.md § "When the spec and the code disagree" governs every proposed rewrite. Where a semantic walk notices the spec is weaker than it should be because of a code constraint, the finding names the platform-gap that should carry the delivery lag — never softens the spec.
- **Grep-only quality limits.** Q1, Q6, Q8, Q9, Q10, Q12, Q14, Q16 are grep-first; Q2, Q3, Q4, Q5, Q7, Q11, Q13, Q15 are reading-first. The command runs grep for grep-first qualities and samples per the protocol for reading-first qualities.
