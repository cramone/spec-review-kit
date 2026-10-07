# Spec quality audit — re-runnable

A standing audit over `{{SPEC_PATH}}/` and `{{ADRS_PATH}}/` that checks the sixteen qualities a specification is required to have. Not phase-bound. Run on cadence or before merging a batch that touches more than one spec file.

Qualities and their rationale restate CLAUDE.md § **Spec files state the specified system — nothing else** and § **When the spec and the code disagree, the spec wins**. This file is the executable form.

## When to run

- Before merging a spec change touching more than one file in `{{SPEC_PATH}}/` or `{{ADRS_PATH}}/`
- Weekly cadence as a drift check
- On demand when a reader reports confusion or an audit finds something a prior pass missed

## Scope

- `{{SPEC_PATH}}/**/*.md` — all qualities apply
- `{{ADRS_PATH}}/**/*.md` — qualities 1 (present tense), 3 (authoritative), 4 (complete), 5 (unambiguous), 7 (infrastructure-agnostic), 9 (statusless) and 15 (consistency) apply; the rest are relaxed because an ADR legitimately carries rationale, rejected options, attribution, dates and the state the decision replaced

Out of scope — `{{REVIEW_PATH}}/`, `{{COMPLIANCE_PATH}}/`, `{{DEPGAPS_PATH}}/`, `docs/reports/`.

## 0. Mechanical pre-flight

Hard zero required before any semantic walk begins. A hit here is a defect the semantic pass does not need to re-raise.

```bash
python .github/scripts/docs_guard.py
<!-- compliance-step-start -->
python .github/scripts/compliance_coverage.py
<!-- compliance-step-end -->
```

Ten `docs_guard` checks. Scopes as declared in the script header.

| Check | Catches |
|---|---|
| `citations` | External id cited but not defined inside `docs/` |
| `build-status` | Deploy state in spec prose |
| `dates` | A date in spec prose, full or year-month |
| `editorial` | Change history, tracking, open questions, notes to a reader, attribution |
| `future-work` | "Will be built", "going to", "plans to", "future phase" |
| `backcompat` | "For now", "in the interim", "legacy behaviour", "transitional shape" |
| `links` | Broken relative links and heading anchors |
| `references` | Bare `<name>.md` resolving to no file |
| `truncation` | A `](` with no closing paren on the line |
| `structure` | Unclosed code fence, ragged table |

If the pre-flight fails, fix the hits and re-run. The semantic walk below starts only on a clean pre-flight.

## 1. Present-tense

A spec sentence states what the system **is**, in the present. Future tense (`will do`, `is going to`, `plans to`) and past tense (`used to`, `once did`) have no place in a spec file.

Mechanical `future-work` catches the delivery sense (`will be built`, `going to deploy`); the semantic pass catches contract sentences written in future tense (`the handler will refuse`, `the item will transition`).

**Walk.**

```bash
grep -rn -E "\b(will|shall) (?!refuse|answer|carry|hold|contain|include|match|resolve|map|pin|point|read|write|publish|project|succeed|fail|return|produce|yield|raise|emit|see|find)" {{SPEC_PATH}}/ {{ADRS_PATH}}/
```

The negative-lookahead list carries the current-contract verbs this platform writes in future-tense legitimately as part of RFC-style wording. A hit outside that list is a finding candidate.

**Finding shape.** Quote the sentence; name a present-tense replacement; cite file:line.

## 2. Prescriptive, not descriptive

A spec file states what the system is required to do. A sentence that merely describes what today's code does ("the handler currently reads the first row and returns it") is description, not specification. If the described behaviour is the required behaviour, write it as a requirement; if it is not, do not write it in the spec at all.

**Walk.** Open five randomly selected spec files; for each, pick five randomly selected `##`/`###` sections; read each section asking: *could an implementer meet the stated behaviour by reading only this file?* Where the answer is "only if they also read the code", the section is description — raise a finding naming the ambiguity.

**Finding shape.** Quote the description-shaped sentence; state the required behaviour it leaves ambiguous.

## 3. Authoritative — spec wins

When a spec statement and the deployed code disagree, the spec is correct and the code is a defect. CLAUDE.md § **When the spec and the code disagree, the spec wins** is the governing rule. The audit does **not** compare spec against code — it checks the spec never weakens a statement to match something a prior session observed in application code.

**Walk.** Scan every spec change in the recent review window for a phrasing of the form "the current implementation …", "today the service …", "the handler as deployed …". A spec statement in that voice records what code does, not what the system is specified to do.

**Finding shape.** Quote the implementation-voiced sentence; name the specified behaviour it should state; propose rewording.

## 4. Complete — every stored value pinned

A specification is complete when every value with cross-service, cross-release or cross-tenant significance is pinned in the spec. For an event-sourced, multi-tenant system that set typically includes:

- Every persistent partition / sort key shape
- Every secondary index name and its PK/SK shape
- Every aggregate-type / stream-type string
- Every enum ordinal relied on by replay or by read-model projection
- Every snapshot member and every read-model row member
- Every published integration event's `type` string and payload member set
- Every error code and the status it maps to
- Every HTTP route, the aggregate it targets and the permission it checks

CLAUDE.md § **Spec files state the specified system** names the exception for a published integration event (spec states the published contract, migration lives in § Known deferred/partial work); every other stored value is spec-pinned.

**Walk.** For a sample of five aggregates (or equivalent top-level units):
- Grep the aggregate's read-model file for key / index declarations → every key shape appears
- Grep for the aggregate-type / stream-type string → one declaration
- Open the write-model file § Events → every event has a payload table

**Finding shape.** Name the unit and the stored value that is not pinned (member missing, ordinal unstated, key shape not specified).

## 5. Unambiguous — absent-meanings written down

A payload member that is nullable has a specified meaning when absent. A field that has a default has the default written down. An enum has every value listed with its ordinal (whether or not the storage format carries ordinals today — the spec pins what a future migration would see). No sentence leaves two reasonable readings.

**Walk.** For a sample of five events:
- Every nullable member in the payload table has an "absent means …" row or a stated default
- Every enum member has its ordinal (`0`, `1`, …) in the enum definition

**Finding shape.** Name the member or enum; quote the ambiguous passage; propose the absent-meaning or ordinal row.

## 6. Self-contained — no citations outside `docs/`

Mechanical check `citations` covers this hard-zero. The semantic pass adds one check: an ADR sentence that cites an external work-item id (ADO, Linear, Jira, GitHub issue) or branch name is a finding — ADR citations are allowed only to things defined under `docs/`.

**Walk.**

```bash
grep -rn -E "\b(MM|AO|PBI|ADO|LI|GH|JIRA)-?[0-9]+\b" {{ADRS_PATH}}/
grep -rn -E "(ClickUp|Linear|Jira|GitHub issue|branch name|repository_dispatch)" {{ADRS_PATH}}/
```

**Finding shape.** Quote the cite; name the `docs/`-local anchor it should replace.

## 7. Infrastructure-agnostic — missing capability is a gap, never a weaker spec

A missing platform capability goes to `{{DEPGAPS_PATH}}/INDEX.md` and to CLAUDE.md § **Known deferred/partial work**. It never softens a spec statement. A sentence of the form "because the SDK does not support X, the spec specifies Y instead of the correct Z" is a finding — the spec specifies Z and the gap records that the SDK must grow X.

**Walk.** Open each spec section whose topic appears in a platform-gap file. Check whether the spec statement is written to the correct target or to the deployed-capability-constrained target.

```bash
# If a dependency-gaps register exists, list its gap topics:
grep -A1 '^## \[F' {{DEPGAPS_PATH}}/INDEX.md | grep '^|' | head -40
```

For each gap topic, find the spec section it covers and verify the statement is at full strength.

**Finding shape.** Quote the weakened statement; name the correct target; name the platform-gap id that holds the delivery gap.

## 8. Historyless

Mechanical `editorial` and `dates` catch most of this on `{{SPEC_PATH}}/`. Semantic pass extends to `{{ADRS_PATH}}/`:

- An ADR's § Context may describe the state the decision replaced; it must not read like a changelog of the ADR itself. "The ADR previously said X but now says Y" is a finding; "the system previously used counter-based uniqueness; this decision replaces it with name-reservation" is legitimate.

**Walk.**

```bash
grep -rn -E "(previously (said|read|stated)|this (ADR|section|document) (used to|once|formerly))" {{ADRS_PATH}}/
```

**Finding shape.** Quote the self-referential ADR history; propose rewording that keeps the Context statement about the system, not about the document.

## 9. Statusless

Mechanical `build-status` and `future-work` are spec-only. The semantic pass extends to `{{ADRS_PATH}}/`:

- An ADR states a decision in the present tense. "X is the coordination substrate" is correct. "X will be the coordination substrate once deployed" is a finding — the deployment state is CLAUDE.md's § Known deferred/partial work, not the ADR's.

**Walk.**

```bash
grep -rn -E "(not (yet )?(deployed|shipped|built|wired|provisioned)|unbuilt|Not built)" {{ADRS_PATH}}/
```

**Finding shape.** Quote the ADR line; name the CLAUDE.md § Known deferred/partial work entry that should carry the deploy state; propose the present-tense ADR rewording.

## 10. Rationale-free (spec), rationale-full (ADR)

A spec file states behaviour. The rationale, trade-offs and rejected options go in the ADR named for the topic. The semantic pass checks both directions:

- A spec section with a "why" paragraph is a finding — move the paragraph to the ADR, replace with a `See [<adr>.md](...)` pointer.
- An ADR section with no § Alternatives, § Rejected options or equivalent is a weak ADR — the decision has rationale missing. Raise as a finding and name the missing rejected-options content.

**Walk.** For each spec file, scan paragraph starters: `Because`, `The reason`, `This is why`, `We chose`, `The alternative was`, `We considered` all indicate rationale.

```bash
grep -rn -E "^(Because|The reason|This is why|We (chose|considered|rejected|opted|picked)|The alternative was)" {{SPEC_PATH}}/
```

For each ADR, confirm presence of a § Rejected / § Alternatives / § Options considered subsection.

**Finding shape.** Spec hit: name the spec line, name the ADR to move it to. ADR hit: name the ADR, name the decision without rationale.

## 11. Reader-neutral

A spec sentence is addressed to no one. "Treat this as authoritative", "do not propose anything shaped like X", "if you are an AI agent reading this" are findings. Mechanical `editorial` catches a tripwire set of these phrasings; the semantic pass reads the first two paragraphs of every spec file and flags any sentence written to a reader.

**Walk.** Open each `{{SPEC_PATH}}/**/*.md` and read the first `## Overview` or opening paragraphs. A direct-address sentence ("note to the reader", "when you read this", "AI agents should", "before proposing") is a finding.

**Finding shape.** Quote the sentence; propose a reader-neutral rewrite that states the design rule rather than instructing the reader.

## 12. Attribution-free (spec)

Mechanical `editorial` catches `decided by <Name>`, `at the request of <Name>`. Semantic pass extends:

- A spec file naming a team ("Platform Team decided", "<Name> requires") is a finding — remove the attribution; the design stands on its own.
- An ADR naming the deciders in § Context is fine (and in some ADR styles required) — do not flag `{{ADRS_PATH}}/`.

**Walk.** Reload the `.spec-review.toml` attribution lists and grep `{{SPEC_PATH}}/` for any `<Name> (decided|requires|wants|needs|asked|requested)` form.

**Finding shape.** Quote the attributed sentence; propose the rewording that states the design rule.

## 13. Testable — rule maps to observable behaviour

A specification rule is testable when a reader can write a scenario that passes exactly when the rule holds. A rule that reduces to "the system behaves well" is not testable; a rule that reduces to "a `CreateFolder` where the parent is `Archived` returns `409 FolderArchived`" is.

**Walk.** For a sample of five rules from one unit's `*.write-model.md` § Invariants:
- Does the unit's `*.scenarios.md` carry a scenario that triggers the rule's error code?
- Does the scenario walk the specific state transition the rule constrains?

**Finding shape.** Quote the invariant; confirm no scenario demonstrates it; propose the scenario shape.

## 14. Diff-is-history

A removed feature is simply absent from the spec. A changed shape is written in its final form. Git log carries the trail; the spec carries no trace of its own evolution.

Mechanical `editorial`/`dates`/`backcompat` catch the obvious patterns (`previously said`, `renamed from`, `transitional shape`). Semantic pass checks for subtler forms:

- A member on a snapshot or event marked "retained for backward compatibility"
- A route marked "accepted alongside the newer `POST …` form"
- A property noted as "the legacy name of X"

**Walk.**

```bash
grep -rn -E "(retained for|alongside the newer|legacy name of|dual-named|accepted for existing callers)" {{SPEC_PATH}}/
```

**Finding shape.** Quote the dual-form sentence; propose spec in final shape; name the CLAUDE.md § Known deferred/partial work migration row to add.

## 15. Consistent across spec and ADR

A rule stated in a shared spec file and restated in a per-unit `*.write-model.md` is one rule; the two files agree on it. A rule stated in a spec file and in the ADR that governs the topic agree on it. This quality checks whether a recent change to one side was propagated to the other.

**Walk.** For each ADR changed in the past 14 commits touching `{{ADRS_PATH}}/`:
- `git log --oneline -- {{ADRS_PATH}}/<file>.md`
- For each spec section the ADR covers, confirm the rule statement matches.

**Finding shape.** Name the rule; quote the ADR statement and the spec statement; name the drift.

## 16. Caveat test

CLAUDE.md § **The caveat test** sets the rule: a caveat belongs in a spec file when it states a consequence of the specified design that holds for anyone implementing it correctly, and does not when it states the current state of the code, a known gap or a recommendation.

**Walk.** For each caveat (noticed by its phrasing: "note that", "important:", "⚠", "beware", "readers should"):
- Apply the test. State in one sentence why it passes or fails.
- A failing caveat is a finding — propose either rewording to state the design consequence or deletion.

```bash
grep -rn -E "(^> \*\*(Note|Important|Caveat|Warning)\*\*|⚠|^\*\*Note:|^\*\*Caveat:)" {{SPEC_PATH}}/
```

**Finding shape.** Quote the caveat; apply the test; propose the rewrite or deletion.

---

## Running the audit

A pass has four modes depending on what it finds:

| Finding count | Action |
|---|---|
| 0 | Record pass in the row below. No audit folder opens. |
| 1–5 | Fix in-place. Record pass with "resolved inline" note. No audit folder opens. |
| 6+ | Open a dated audit folder `{{REVIEW_PATH}}/spec-audit-<YYYY-MM-DD>-quality/` from the `_template`. Write one finding file per hit. Work through via `/spec-audit-next <date>`. |

Any finding whose fix spans multiple spec files **always** opens a folder regardless of count — propagation needs the audit protocol.

## Pass log

| Date | Mode | Pre-flight | Semantic | Resolved | Opened folder |
|---|---|---|---|---|---|
| _(empty — first pass fills this in)_ | | | | | |

Rolling tail; keep the last twenty rows. Older rows are visible in git.

## Protocol summary — every run

0. **Mechanical pre-flight** — `python .github/scripts/docs_guard.py` to zero.<!-- compliance-step-start --> Also `compliance_coverage.py` to zero.<!-- compliance-step-end -->
1. **Semantic walk** — qualities 1–16 in order; stop at the first that fails only if the failure blocks later qualities (rare).
2. **Decide mode** — count findings; apply the Running the audit table.
3. **Act** — fix inline, or open the audit folder and write finding files.
4. **Record** — add a row to Pass log.
5. **Close** — re-run docs-guard; confirm zero.

<!-- strip-if-no-platform-check:start -->
The audit does not read this repo's application code. Where a semantic walk would benefit from code evidence, read `{{PLATFORM_REPO}}` instead (CLAUDE.md § **Spec-first phase**).
<!-- strip-if-no-platform-check:end -->
