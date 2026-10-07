# F<nnn> — `<one-line finding title>`

```yaml
id: F<nnn>
title: <same as heading>
severity: <critical | major | minor | nit>
dimension: <A-J, comma-separated if multi>
bucket: <spec-edit | decision | platform-check>
status: open
origin: spec-audit-<YYYY-MM-DD>
owner: <name or role>
```

**Optional yaml members** (add when they apply):

```yaml
fix-with: [F<nnn>, F<nnn>]            # lands in the same commit as these
held-by: spec-audit-<date>/<row id>   # waits on this blocker closing
                                      # or: dependency-gaps/F<nnn>
prior: <path>                         # revisits an older finding
migration: yes                        # fix adds a CLAUDE.md § Known deferred/partial work entry
platform-check: <path>                # read only this file in the platform-check repo
decision-needed: <one-line question>  # bucket: decision — question to answer
decision-owner: <records-domain | architecture | platform-team | ...>
recheck: yes                          # another iteration edited a file this one cites
```

---

## Claim

**(What the spec says today, or what is missing.)** Quote the exact lines. Cite paths with line numbers.

```
<quoted text>
```

- Cited at: `{{SPEC_PATH}}/.../<file>.md:<line>`

## Problem

**(Why the current state is wrong.)** One paragraph. Lead with the consequence a reader or implementer hits.

## Evidence

**(What was checked.)** Grep patterns, file paths, line numbers. Enough that a future auditor can verify without redoing the search.

- `grep -n '<pattern>' {{SPEC_PATH}}/.../<file>.md` → N hits, each listed by file:line
- `{{SPEC_PATH}}/.../<other-file>.md:<line>` — says X
- `{{SPEC_PATH}}/.../<third-file>.md:<line>` — says Y

## Proposal

**(What the spec should say instead.)** Written so it can be pasted into a spec file: present tense, no finding id, no rationale, no external tracker ids inside spec files.

> `<proposed replacement text>`

Rationale that cannot sit in the spec goes to the matching topic ADR under [`{{ADRS_PATH}}/README.md`](../../../{{ADRS_PATH}}/README.md).

## Verdict (fill at close)

```yaml
status: fixed | platform-gap | held | wont-fix | superseded
resolution: <one line — what the spec now says, or why not>
changed: [<path1>, <path2>, ...]
propagation:
  grepped: <old pattern>
  hits: <count>
  fixed in this commit: [<files>]
  left (different context): [<files or "none">]
  raised as new finding: [<F<nnn> or "none">]
```

---

## Phase-specific finding shapes

**Delete the subsection(s) that do not apply. Keep only the one matching the audit's phase.**

### A — spec-internal consistency

Shape: `rule X stated in file A, file B says Y`.

Example filled fields:
- **Claim** quotes both files side-by-side
- **Problem** explains how the two statements differ
- **Evidence** lists every file in `{{SPEC_PATH}}/**` that restates the rule
- **Proposal** picks a canonical statement and names the files to update

### B — scenarios coverage

Shape: `invariant / error code / state transition on <unit> has no scenario demonstrating it`.

Example filled fields:
- **Claim** quotes the invariant / code / transition from the write-model
- **Problem** says the unit's `scenarios.md` has no scenario for this rule
- **Evidence** confirms by grep across `*.scenarios.md`
- **Proposal** sketches the scenario that should be added, in the unit's scenario-file shape

### C — dark corners

Shape: `declaration X is in the spec but reached by nothing`.

Example filled fields:
- **Claim** quotes the declaration (error code row, event type, permission string, state value)
- **Problem** confirms by grep that no consumer / route / handler / command reaches it
- **Evidence** lists every file where the declaration appears, each is a declaration not a use
- **Proposal** either (a) delete the dead declaration, or (b) point at the usage the audit missed

### D — external standards

Shape: `spec claim X does not match RFC/vendor source Y`.

Example filled fields:
- **Claim** quotes the spec claim
- **Problem** cites the external source and notes the specific divergence
- **Evidence** links to the source (URL + section anchor + retrieved-on date)
- **Proposal** aligns the spec to the source, or records why the deviation is deliberate (which goes in the ADR, not the spec)
