# spec-review-kit

Portable spec-review tooling for event-sourced / DDD / CQRS projects (or any spec-first codebase). Carries two slash commands, two Python guards, a review-folder scaffold, and a CLAUDE.md guardrail section — all driven by a `.spec-review.toml` at the target repo root.

Extracted from a long-running audit cycle; proven on a .NET/DynamoDB codebase, generic enough for any stack.

## What it ships

| Component | What it does |
|---|---|
| **`docs_guard.py`** | Ten hard-zero checks over `docs/` — citations, build-status, dates, editorial, future-work, backcompat, links, references, truncation, structure |
| **`compliance_coverage.py`** | Validates every link from `docs/compliance/` into spec / ADR / dependency-gaps resolves |
| **`/spec-quality-audit`** | Sixteen-quality standing audit. Mechanical pre-flight then semantic walk. Opens an audit folder when findings cross threshold |
| **`/spec-audit-next <date>`** | Works one unit of an open audit folder per invocation. Mandatory dependency-gaps pre-flight + propagation sweep |
| **`docs/review/_template/`** | INDEX + FINDING templates for a new audit |
| **`docs-guard.yml`** | CI workflow that runs both guards on every spec change |
| **`CLAUDE.md § Spec review`** | Guardrail section pasted (markered, idempotent) into the target repo's `CLAUDE.md` |
| **Spec scaffold** | Opinionated `docs/spec/` tree per profile (`ddd-event-sourced`, `ddd-crud`, `api-service`, `library`) — glossary, architecture, shared concerns, per-unit shape, ADRs, dependency gaps, compliance mapping. Every scaffolded file passes `docs_guard` from install |

## Install

```bash
git clone https://github.com/cramone/spec-review-kit ~/.claude/skills/init-spec-review
```

Then in the target repo:

```
/init-spec-review
```

The skill:
1. Asks config values (project name, owner, paths, platform-check target, tracker, compliance).
2. If `docs/spec/` is empty, offers a scaffold step — pick a profile and name the top-level units.
3. Writes `.spec-review.toml`, copies scripts / commands / review templates, appends the CLAUDE.md guardrail section between managed markers.

Run `/init-spec-review scaffold` to run just the scaffold step without the full install. Run `/init-spec-review reconfigure` to update tracker / platform-check / paths without re-scaffolding.

## Update

```bash
git -C ~/.claude/skills/init-spec-review pull
```

Then in the target repo:

```
/init-spec-review update
```

Re-copies kit files; preserves `.spec-review.toml`; refreshes the CLAUDE.md section between markers.

## Reconfigure

```
/init-spec-review reconfigure
```

Re-gathers config values (existing answers prefill as defaults). Then re-copies.

## Uninstall

```
/init-spec-review uninstall
```

Prompts before removing each installed path. CLAUDE section is removed between markers.

## Config

See [`kit/_config/spec-review.example.toml`](./kit/_config/spec-review.example.toml) for the full shape. Minimal:

```toml
[project]
name  = "my-service"
owner = "Your Name"

[paths]
spec   = "docs/spec"
adrs   = "docs/adrs"
review = "docs/review"

[platform_check]
enabled = false

[guard]
allow_families = ["BCP","ISO","RFC","UTF","SHA","HTTP","SI","UUID"]

[guard.allow_tokens]
custom = []

[guard.attribution]
names = []
teams = []

[guard.references]
allow = []

[guard.checks]
enabled = ["citations","build-status","dates","editorial","future-work","backcompat","links","references","truncation","structure"]

[compliance]
enabled = false

[audit.dimensions]
A = "DDD / aggregate design"
# ...
```

## How the parts fit

```
.spec-review.toml  ──┬── docs_guard.py           (reads paths, allowlists, checks)
                     ├── compliance_coverage.py  (reads paths, compliance.enabled)
                     ├── spec-audit-next.md      (reads paths via install-time substitution)
                     └── spec-quality-audit.md   (reads paths via install-time substitution)
                     
docs/
  spec/                   ← the specification
  adrs/                   ← the decisions
  review/
    README.md             ← audit tracker
    spec-quality-audit.md ← the 16-quality protocol
    _template/            ← starting point for a new spec-audit-<date>/
    spec-audit-<date>/    ← an open audit (created ad hoc)
  dependency-gaps/        ← platform / SDK / infra gaps (optional)
  compliance/             ← standards mapping (optional)
```

## When to use

- You maintain a specification separate from the code (or want to).
- You've been through at least one "the spec said X but the code did Y" incident.
- You want a repeatable review cycle that catches drift mechanically.
- You accept the "spec wins" axiom — divergences are code bugs, not spec weaknesses.

## When not to use

- Your source of truth is the code; specs are generated or absent.
- You want permissive, descriptive documentation.
- You don't want hard-zero CI gates on prose.

## License

MIT.
