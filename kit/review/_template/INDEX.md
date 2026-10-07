# Spec audit — `<YYYY-MM-DD>`

**Phase:** `<A | B | C | D>` · **Scope:** `<one-line scope statement>` · **Mode:** `<spec-internal consistency | scenarios coverage | dark corners | external standards>`

**Owner:** `<name>`

## Where this fits

See [`{{REVIEW_PATH}}/README.md`](../README.md) § Phase roadmap for how this phase fits the broader audit chain. See the audit folder's finding files for per-finding state. `/spec-audit-next <YYYY-MM-DD>` iterates one unit per invocation.

---

## 0. Known dependency-gaps consulted

**Mandatory pre-flight.** Before any finding was raised, the sweep consulted [`{{DEPGAPS_PATH}}/INDEX.md`](../../../{{DEPGAPS_PATH}}/INDEX.md) and matched candidate findings against every Fnnn gap file across every theme. The table below records the mapping.

| Candidate subject | Matched dependency-gap | Decision |
|---|---|---|
| _(fill in — one row per candidate matched or examined)_ | | |

Pre-flight re-runs on every `/spec-audit-next` iteration. Any new dependency-gap added since this audit opened is caught then.

---

## Scope

**In scope.** `<what this audit covers>`

**Out of scope.** `<what this audit explicitly does not cover>`

**Spec files consulted.** `<list the subset of {{SPEC_PATH}}/** this audit reads from>`

---

## Totals

Updated as findings close.

| Verdict | Count |
|---|---:|
| `open` | tbd |
| `in-progress` | tbd |
| `fixed` | tbd |
| `platform-gap` | tbd |
| `held` | tbd |
| `wont-fix` | tbd |
| `superseded` | tbd |
| **Total** | tbd |

---

## Work order

`/spec-audit-next <YYYY-MM-DD>` picks the first `open` unit in this list. A finding named after `+` lands in the same commit as its unit lead (its `fix-with:` field). Skip `held` findings — they release when their blocker closes.

| Order | Unit | Finding(s) | Status |
|---|---|---|---|
| 1 | `<description>` | [`F001`](./F001-<slug>.md) + `F002` | open |
| 2 | ... | ... | ... |

---

## All findings

| Id | Sev | Dim | Bucket | Status | Title |
|---|---|---|---|---|---|
| [`F001`](./F001-<slug>.md) | `<critical \| major \| minor \| nit>` | `<A-J>` | `<spec-edit \| decision \| platform-check>` | `open` | `<one-line title>` |
| ... | | | | | |

Dimension codes (edit per `.spec-review.toml` `[audit.dimensions]`):

- **A** DDD / aggregate design · **B** event sourcing · **C** CQRS / read models · **D** concurrency, idempotency, ordering · **E** multi-tenancy & auth · **F** sagas & process managers · **G** cascade & lifecycle · **H** API contract & errors · **I** bottlenecks / capacity · **J** spec hygiene

---

## Phase-specific focus areas

**(Delete the subsections that do not apply to this phase. Keep only the one that matches the phase stated above.)**

### Phase A — spec-internal consistency

Hotspots:
- Cross-unit shared rules vs per-unit restatements
- Integration event catalogue vs per-unit domain events
- Index inventory vs per-unit `*.read-model.md`
- Error catalogue vs per-route Errors lines
- Aggregate-type / stream-type strings
- Enum ordinals stated in multiple places
- `AggregateType` → file-name convention

### Phase B — scenarios coverage

For each unit's `*.write-model.md`:
- Does `*.scenarios.md` carry a scenario for every invariant in § Invariants?
- Does `*.scenarios.md` trigger every error code listed in § Errors?
- Does `*.scenarios.md` walk every state transition in § Status transitions?

### Phase C — dark corners

- Error codes declared but never returned (grep `*.api.md` for each code)
- Events declared in write-models not consumed by any projector / handler / integration event
- Permissions in vocabulary not granted by any role / not required by any route
- State transitions reachable in the state machine but produced by no command

### Phase D — external standards

Spec claims that need external verification. Fill with the standards and RFCs the spec cites.

---

## Iteration protocol summary

Every `/spec-audit-next <YYYY-MM-DD>` run:

0. Platform-gaps pre-flight (mandatory)
1. Load state from this INDEX
2. Load finding
3. Re-read cited spec state
4. Apply the caveat test (CLAUDE.md § Spec files state the specified system)
5. Stored-value rule
6. Act by bucket — fix / supersede / decision / platform-check / held / blocked
7. Propagate re-check flags
7a. **Propagate the fix across the spec** — grep for the old pattern tree-wide, fix same drift, raise follow-up findings
8. Close — run docs-guard
9. Report and stop

Full protocol in [`.claude/commands/spec-audit-next.md`](../../../.claude/commands/spec-audit-next.md).
