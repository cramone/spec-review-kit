# Spec-audit template

Starting point for a new `{{REVIEW_PATH}}/spec-audit-<YYYY-MM-DD>/`. Copy, fill in, then run.

## Files in this template

- [`INDEX.md`](./INDEX.md) — audit index: scope, dependency-gaps pre-flight, work order, all-findings table
- [`FINDING-template.md`](./FINDING-template.md) — one-per-finding file shape

## To open a new audit

```bash
# 1. Make the audit folder with today's date
mkdir {{REVIEW_PATH}}/spec-audit-$(date +%Y-%m-%d)

# 2. Copy the INDEX
cp {{REVIEW_PATH}}/_template/INDEX.md {{REVIEW_PATH}}/spec-audit-$(date +%Y-%m-%d)/INDEX.md

# 3. Fill in INDEX.md's § Scope, § 0 pre-flight (list dependency-gaps checked),
#    and § Work order (unit list after the agent sweep populates findings)

# 4. Pre-populate findings — run cluster agents, verify a sample by hand,
#    write one FINDING-template.md-shaped file per finding
#    (e.g. {{REVIEW_PATH}}/spec-audit-<date>/F001-<slug>.md)

# 5. Add a row to {{REVIEW_PATH}}/README.md § Open audits

# 6. Begin work
/spec-audit-next <date>
```

## Agent sweep caveat

Agents consistently produce false-negative `missing`/`partial` findings on narrow greps. A random verification of 10-20% of the sweep's output is mandatory before trusting non-aligned verdicts.

## Phase templates (choose per audit)

Different audit phases need different finding shapes. Each phase has its own template section inside `FINDING-template.md` — pick the one that matches:

- **A — spec-internal consistency** — "rule X stated in file A, file B says Y" shape
- **B — scenarios coverage** — "invariant X on write-model has no scenario demonstrating it" shape
- **C — dark corners** — "error code X in catalogue returned by no route" shape
- **D — external standards** — "spec claim X contradicts RFC/vendor source Y" shape
