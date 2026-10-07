---
description: Work the next spec-audit item. One unit per invocation. Audit-generic — operates on whichever `{{REVIEW_PATH}}/spec-audit-<date>/` folder is current. Re-reads state each turn so cascading edits stay consistent. Mandatory dependency-gaps pre-flight before any new finding is scored or acted on.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(python .github/scripts/docs_guard.py:*), Bash(python3 .github/scripts/docs_guard.py:*), Bash(ls:*)
---

# /spec-audit-next

You are executing **one** iteration of a spec-audit remediation loop. Do not batch. Do not skip ahead. Do not re-order a worklist.

## Dispatch — which audit

Read `$ARGUMENTS`:

| Argument | Meaning |
|---|---|
| `<date>` (e.g. `2026-11-15`) | Open the folder `{{REVIEW_PATH}}/spec-audit-<date>/`, pick the next unit per that audit's `INDEX.md` § Work order |
| `<date> F0nn` or just `F0nn` | A specific finding under the current (or named) audit |
| empty | Discover: `ls {{REVIEW_PATH}}/` — if exactly one `spec-audit-*` folder exists, use it. If none, print `NO AUDIT OPEN — consult {{DEPGAPS_PATH}}/INDEX.md for the surviving workstream` and stop. If several, list them and stop. |

### Audit discovery

Run `ls {{REVIEW_PATH}}/` to find candidate `spec-audit-<date>/` folders. The command works whichever one is current.

## Bindings

- **Audit root:** `{{REVIEW_PATH}}/spec-audit-<date>/`
- **Finding files:** `{{REVIEW_PATH}}/spec-audit-<date>/F0nn-<slug>.md` or `<agent>/F0nn-<slug>.md`
- **Audit index:** `{{REVIEW_PATH}}/spec-audit-<date>/INDEX.md` (or `WORKLIST.md` for older layouts)
- **Spec root (edits target here):** `{{SPEC_PATH}}/**`, `{{ADRS_PATH}}/**`
- **Dependency-gaps register:** `{{DEPGAPS_PATH}}/INDEX.md` — **mandatory pre-flight; see § 0**
- **Guardrail:** `CLAUDE.md` § "Spec files state the specified system"
<!-- strip-if-no-platform-check:start -->
- **Code that may be read:** `{{PLATFORM_REPO}}` only (`{{PLATFORM_REL_PATH}}`; read its `CLAUDE.md` first). Never read this repo's application code.
<!-- strip-if-no-platform-check:end -->
<!-- keep-if-no-platform-check:start -->
- **Code reads:** none during the spec-first phase. The spec decides.
<!-- keep-if-no-platform-check:end -->
- **Argument:** `$ARGUMENTS` — optional date and / or finding id.

## § 0. Mandatory dependency-gaps pre-flight (every iteration)

**Before loading the finding** at step 2:

1. Read `{{DEPGAPS_PATH}}/INDEX.md` — scan the gap-file register and the pre-flight procedure.
2. For the candidate finding, run both passes:
   - **Tag grep.** Pick 2–3 keywords from the finding's `claim` / `problem` / `location`. Grep `{{DEPGAPS_PATH}}/**/*.md` for each. Record hits.
   - **Detection-signal match.** Open every hit and read its `## Detection signals` section. The gap owns the finding if any signal matches, even when wording differs.
3. **If matched:**
   - Set `status: held` on the finding file, add `held-by: dependency-gaps/F0nn`, and record `resolution: already tracked as dependency-gaps/F0nn`.
   - Update the audit's `INDEX.md` row.
   - Report `MATCHED dependency-gaps/F0nn` and stop this iteration.
4. **If not matched:** proceed to step 1 below. The pre-flight result (gap files consulted, outcome) is recorded in the iteration report (§ 6).

The audit's `INDEX.md` § 0 (if present) lists dependency-gaps consulted at audit open — the per-iteration pre-flight re-runs the check in case gaps were added since.

## Protocol

### 1. Load state
- Read the audit's `INDEX.md` (or `WORKLIST.md`).
- If `$ARGUMENTS` names a finding, process that one — including a `held` or `blocked` one if the user's message gives the decision.
- Otherwise find the first `open` finding in § Work order whose dependencies are met.
- If none remain, print `AUDIT <date> COMPLETE`, list `held` / `blocked` / `platform-gap` findings, and stop.

### 2. Load finding
- Read the finding file. Extract: `severity`, `dimension`, `location`, `claim`, `problem`, `evidence`, `proposal`, `bucket`, and any `fix-with:`, `held-by:`, `prior:`, `migration:`, `decision-needed:`.
- If `held-by:` names an unknown or retired audit, treat as stale — re-run § 0 against `{{DEPGAPS_PATH}}/`; if still unmatched, remove the stale `held-by:` and treat as `open`.

### 3. Re-read cited spec state
- For every `{{SPEC_PATH}}/**` or `{{ADRS_PATH}}/**` file cited in `location` or `evidence`, Read it fresh — earlier iterations may have shifted line numbers or removed text.
- Grep for the exact `claim` string. If it is no longer present, treat as candidate for supersede (§ 6b).
<!-- strip-if-no-platform-check:start -->
- If the finding needs a code check: a check against the platform SDK is done in `{{PLATFORM_REPO}}`; a check against this repo's application code is not done, and the spec decides.
<!-- strip-if-no-platform-check:end -->

### 4. Apply the caveat test (CLAUDE.md rule)
Before proposing an edit, confirm the proposal does **not** introduce any banned pattern into `{{SPEC_PATH}}/**`:

- No change history, no dates in headings, no strikethrough supersession
- No external tracker ids (`MM-\d+`, `X-\d+`, `DEC-\d+`, `ADR-0\d+`, `F0nn`) in spec files — link the topic doc + anchor instead
- No build / deployment status ("deployed as", "not built", "not yet wired", "migration is", "no such class")
- No rationale, no rejected options, no "raised as", no "treat as authoritative"
- No `⚠` caveats that state current code state rather than a consequence of the design

If the finding's own `proposal` violates any of these, downgrade the fix: apply only the design-normative part, and route the rest to `CLAUDE.md § Known deferred/partial work` or the finding's proposed alternate home.

### 5. Stored-value rule
- **Published integration events keep the exception.** If the finding changes an integration event's `type` string or payload members, the spec states the published contract and the migration that changes it (a new event version or a dual-publish window). With no migration stated, mark the finding `blocked` with reason `published integration event; needs migration decision`.
- **Every other stored value is stated as specified**: partition and sort keys, GSI names and shapes, aggregate-type strings, enum ordinals (pinned explicitly), snapshot and read-model members. Remove any "deployed" shape or migration text from `{{SPEC_PATH}}/`. Add the deployed-to-specified migration under `CLAUDE.md` § Known deferred/partial work in the same iteration.

### 6. Act by bucket

**6a. `spec-edit` — apply fix**
- Edit the cited spec / ADR files. Prefer surgical Edits over rewrites. Keep prose terse per spec convention.
- Set `status: fixed`, append `resolution: <one line>` and `changed: <files>`.

**6b. Supersede**
- If the claim is no longer supported by current file state (earlier iteration already fixed it), set `status: fixed` with `resolution: already stated — <where>`.

**6c. `decision`**
- If the user's message does not give the decision, set out the `decision-needed:` question, the options with their consequences, the files each option touches, and the other `fix-with:` members affected. Then **stop and wait**. Once decided, record the rationale in the ADR the `{{SPEC_PATH}}/README.md` question index names, then edit the spec.

<!-- strip-if-no-platform-check:start -->
**6d. `platform-check`**
- Read only what the `platform-check:` line names, in `{{PLATFORM_REPO}}`. Never read this repo's application code. Then either state the design in the spec if the platform delivers it, or state the design anyway and **add the capability to `{{DEPGAPS_PATH}}/`** (new `F0nn-<slug>.md` file + INDEX row + CLAUDE.md § Known deferred/partial work pointer). Status becomes `fixed` or `platform-gap`.
<!-- strip-if-no-platform-check:end -->

**6e. `held` by platform-gap**
- Set `status: held`, `held-by: dependency-gaps/F0nn`. Do not edit the spec. Report and stop.

**6f. Blocked**
- If the proposal needs owner input not yet given, set `status: blocked` with `blocked-on: <owner> — <question>` and stop.

### 7. Propagate re-check flags
- Grep other `open` findings whose `location:` or `evidence:` cites a file you edited. Add or refresh a `recheck: yes` line on each.
- Clear `recheck:` on the finding you just closed.

### 7a. Propagate the fix across the spec (mandatory)

**A fix often changes a value, rule, or statement that is restated across the spec. If this propagation step is skipped, the same drift returns next audit cycle.**

For every change applied in § 6a:

1. **Identify the pattern that changed.** A stored value (key shape, enum member, event name, error code, aggregate-type string), a rule statement (invariant, guard order, refusal precedence), a cross-reference text, a terminology choice (field name, policy name), or a filename.
2. **Grep the entire spec tree.** Run Grep across `{{SPEC_PATH}}/**` and `{{ADRS_PATH}}/**` for the **old** pattern. Not just the file edited.
3. **For each hit, classify:**
   - **Same drift** → fix in the same commit as part of this finding.
   - **Different context (same word, different meaning)** → leave; note in the finding's `resolution` which hits were examined and left.
   - **Follow-up drift** (related but not covered by this finding's proposal) → raise a new finding before closing this one. Add it as an `open` row in the audit's `INDEX.md` and link from this finding's `related:`.
4. **Record the sweep.** Append to the finding file:
   ```
   propagation:
   - grepped: <old pattern>
   - hits: <count>
   - fixed in this commit: <files>
   - left (different context): <files or "none">
   - raised as new finding: <F0nn or "none">
   ```

**The sweep is not optional.** A finding that changes a widely-stated contract without a propagation block has not landed. If no sweep is applicable (meta-decision, docs-only edit), say so explicitly: `propagation: n/a — <reason>`.

### 8. Close
- Run `python .github/scripts/docs_guard.py`. Fix any hit before closing.
- Update the finding's status row in the audit's `INDEX.md` § All findings.
- If the fix changes a rule `CLAUDE.md` restates, update the restatement in the same change.

### 9. Report and stop

Emit exactly this shape (terse):

```
ITER <audit-date> <finding-id>
preflight: <matched dependency-gaps/F0nn | no match — <gap files consulted>>
action: <fixed|held|platform-gap|superseded|decision-needed|blocked>
edits: <path1>, <path2>, ...
propagation: <hits grepped — fixed in commit | n/a — reason>
audit: <n fixed> / <total> · <n open> · <n held> · <n platform-gap> · <n blocked>
next: <next finding id> or AUDIT COMPLETE
recheck flags added: <count>
new platform-gap: <F0nn if a 6d call created one, else none>
new findings raised by propagation: <F0nn or "none">
```

Stop. Do not proceed to the next finding in the same invocation.

## Guardrails

- **Do not** edit `{{SPEC_PATH}}/**` or `{{ADRS_PATH}}/**` outside § 6a / 6d.
<!-- strip-if-no-platform-check:start -->
- **Do not** read this repo's application code. Only `{{PLATFORM_REPO}}` may be read.
<!-- strip-if-no-platform-check:end -->
- **Do not** create new spec files unless the finding names one.
- **Do not** open Plan mode; this is straight execution.
- **Do not** commit unless the user explicitly asks — accumulate edits until `/commit` or manual instruction.
- **Do not** touch findings outside the current one + re-check propagation.
- **Do not** skip § 0 pre-flight. It runs every iteration.
- Bash is restricted to read-only `git status | diff | log`, `ls`, and `docs_guard.py`. No push, no reset, no branch ops.

## Opening a new audit — INDEX.md must carry § 0

A new `{{REVIEW_PATH}}/spec-audit-<date>/INDEX.md` must open with:

```markdown
## 0. Known dependency-gaps consulted

Pre-flight at audit open (date): read `{{DEPGAPS_PATH}}/INDEX.md`. Candidate findings matched to existing gaps are recorded here, not raised as new findings.

| Candidate subject | Matched gap | Decision |
|---|---|---|
| <subject> | dependency-gaps/F0nn | held-by |
| ... | ... | ... |

Pre-flight re-runs on every `/spec-audit-next` iteration — gaps added after audit open are caught at per-iteration time.
```

Without § 0, the audit is treated as pre-flight-incomplete and `/spec-audit-next` refuses to run.

## Failure modes to watch for

- **Cascading edits in a single file**: if two findings edit the same file back-to-back, the second's line numbers will not match its evidence. Always re-Read after any prior iteration.
- **Ghost claims**: the finding cites a heading that was renamed. Grep for the surrounding sentence, not just the anchor.
- **Stale `held-by:`**: a finding held on a retired audit — re-run § 0 against `{{DEPGAPS_PATH}}/` and either rebind or clear.
- **Pre-flight skipped**: iteration proceeds without consulting `{{DEPGAPS_PATH}}/` — new finding raised that duplicates existing gap. Hard rule: § 0 runs first, always.
- **Stored values**: the spec states the specified key, name or ordinal; the move from deployed data goes into `CLAUDE.md` § Known deferred/partial work. Only a published integration event's `type` or payload keeps its published value in the spec, with a stated migration.
