---
name: init-spec-review
description: Scaffold the spec-review kit into the current repo. Use when the user says "setup spec review", "install spec review kit", "init spec review kit", "scaffold spec", or runs /init-spec-review. Interactive — asks for project name, owner, platform-check repo, team names, custom tokens, tracker, scaffold profile. Writes .spec-review.toml, scaffolds docs/spec tree, copies scripts/workflow/commands/templates, appends a managed CLAUDE.md guardrail section.
allowed-tools: Read, Grep, Glob, Edit, Write, AskUserQuestion, Bash(git status:*), Bash(git rev-parse:*), Bash(ls:*), Bash(mkdir:*), Bash(cp:*), Bash(cat:*)
---

# init-spec-review

Scaffold the portable spec review kit into the current repo. This skill is executed from `~/.claude/skills/init-spec-review/` (a clone of `https://github.com/cramone/spec-review-kit`). The `kit/` folder next to this `SKILL.md` is the source material.

## Argument dispatch

Read `$ARGUMENTS`:

| Argument | Meaning |
|---|---|
| empty | **Install.** Pre-flight, gather config, scaffold if docs/spec empty, copy kit files, append CLAUDE section. |
| `scaffold` | **Scaffold only.** Create the spec tree per profile; stop before review-kit config. |
| `reconfigure` | Re-gather config and re-copy. Preserves existing `.spec-review.toml` values as defaults. Updates `{{TRACKER_PHRASE}}` substitutions. Does not re-scaffold. |
| `update` | Re-copy files only. `.spec-review.toml` untouched; CLAUDE section refreshed between markers. |
| `uninstall` | Remove installed files + CLAUDE section (between markers). Prompt before each delete. Does not touch scaffolded `docs/spec/` content. |

## 1. Pre-flight

1. Confirm cwd is a git repo: `git rev-parse --show-toplevel`. If not, print `init-spec-review: not a git repo — stop` and exit.
2. Check for existing install: look for `.spec-review.toml` at repo root. If present and `$ARGUMENTS` is empty, offer:
   - `update` — re-copy, keep config
   - `reconfigure` — new config, re-copy
   - `abort`
3. Check for existing scaffold: list `docs/spec/`. If present with content, scaffold step is skipped unless `$ARGUMENTS = scaffold` (which refuses to overwrite — asks to delete first).
4. Locate kit source: skill folder is `Path(__file__)` equivalent — grep for `SKILL.md` in `~/.claude/skills/init-spec-review/`. Kit root is that folder; files are under `kit/`.

## 2. Config gathering

Use **one** AskUserQuestion with these fields (defaults populated from any existing `.spec-review.toml` on `reconfigure`):

```
project.name            — short slug (e.g. my-service)
project.owner           — audit INDEX default owner
paths.spec              — default: docs/spec
paths.adrs              — default: docs/adrs
paths.review            — default: docs/review
paths.dependency_gaps   — default: docs/dependency-gaps (blank to disable)
paths.compliance        — default: docs/compliance (blank to disable)
platform_check.enabled  — y / n
  if y:
    platform_check.repo          — repo name
    platform_check.relative_path — path from repo root
guard.attribution.names — comma-separated names flagged in audit protocol attribution grep
guard.attribution.teams — comma-separated team names
guard.allow_tokens.custom — comma-separated extra ALLOW_TOKEN entries
guard.references.allow    — comma-separated out-of-repo filenames named in spec prose
compliance.enabled      — y / n
tracker.enabled         — y / n
  if y:
    tracker.name             — free-form display name
    tracker.reference_phrase — how CLAUDE.md refers to it (e.g. "the Media ADO board")
scaffold.needed         — detected: y if docs/spec/ absent or empty
  if y:
    scaffold.profile — one of: ddd-event-sourced, ddd-crud, api-service, library
    scaffold.units   — comma-separated top-level unit names (contexts / resources / modules)
    scaffold.sub_units_per_unit — map of unit → comma-separated sub-units (for profiles with sub_unit_container)
    scaffold.shared_opt_in — comma-separated optional shared concerns to include (menu from profile manifest)
```

Build a `.spec-review.toml` dict from answers (merge with existing on `reconfigure`).

## 3. Scaffold step (install flow only, if docs/spec/ empty)

### 3a. Load profile manifest

Read `kit/scaffold/profiles/{profile}/manifest.toml`. Extract:
- `unit_term`, `unit_container`, `sub_unit_container`
- `root_files`, `architecture_files`, `unit_files`
- `shared.required`, `shared.optional`

### 3b. Confirm shared menu

Show the user:
- Required (auto-included): `shared.required`
- Optional (menu): `shared.optional` — user picks any subset

The final shared set is `required ∪ picked_optional`.

### 3c. Write the tree

For profile `{profile}`:

1. **Root files.** For each in `root_files`, copy `kit/scaffold/profiles/{profile}/<name>` → `{paths.spec}/<name>` with placeholder substitution.
2. **Architecture.** For each in `architecture_files`, copy `kit/scaffold/profiles/{profile}/architecture/<name>` → `{paths.spec}/architecture/<name>`.
3. **Shared.** For each name in the final shared set, copy `kit/scaffold/shared/<name>.md` → `{paths.spec}/shared/<name>.md`.
4. **Units.** For each unit `U` in `scaffold.units`:
   - If `sub_unit_container` is empty: for each file in `unit_files`, write to `{paths.spec}/{unit_container}/<unit>.{suffix}.md` (where `<unit>` is `U` lower-cased).
   - If `sub_unit_container` is non-empty: for each sub-unit `S` under `U`, for each file in `unit_files`, write to `{paths.spec}/{unit_container}/<U>/{sub_unit_container}/<S>/<s>.{suffix}.md`.
5. **ADRs.** Copy `kit/scaffold/adrs/README.md` → `{paths.adrs}/README.md` and `kit/scaffold/adrs/0001-architecture-and-stack.md` → `{paths.adrs}/0001-architecture-and-stack.md`.
6. **Dependency gaps** (if `paths.dependency_gaps` non-empty): copy `kit/scaffold/dependency-gaps/INDEX.md` + `_template/*` under `{paths.dependency_gaps}/`.
7. **Compliance** (if `compliance.enabled = true` AND `paths.compliance` non-empty): copy `kit/scaffold/compliance/INDEX.md` + `_template/*` under `{paths.compliance}/`.

### 3d. Scaffold placeholder substitutions

Beyond the global set (§ 4), scaffold adds per-unit substitutions when writing unit files:

| Placeholder | Source |
|---|---|
| `{{Unit}}` | Pascal-case form of the unit name (e.g. `MediaItem`) |
| `{{unit}}` | lower-case form (e.g. `mediaitem`) |
| `{{UNIT_UPPER}}` | upper-case form (e.g. `MEDIAITEM`) |
| `{{Context}}` | Pascal-case parent (empty if flat) |
| `{{context}}` | lower-case parent (empty if flat) |
| `{{UnitTerm}}` | from manifest `unit_term`, title-cased (e.g. `Aggregate`) |
| `{{unitTerm}}` | from manifest `unit_term` lower-cased |
| `{{project-prefix}}` | `project.name` lower-cased, hyphens preserved |

The template filename `{{unit}}.<suffix>.md` is also substituted at write time — e.g. `{{unit}}.api.md` becomes `mediaitem.api.md`.

### 3e. Record scaffold state

Write back to `.spec-review.toml`:

```toml
[scaffold]
profile = "<chosen>"
units   = ["Unit1", "Unit2", ...]
```

## 4. Install plan (file set)

Compute the file set:

| Source (under kit/) | Target (in repo) | Transform |
|---|---|---|
| `_config/spec-review.example.toml` | `.spec-review.toml` | Replace values from config dict; preserve comments |
| `scripts/docs_guard.py` | `.github/scripts/docs_guard.py` | Copy verbatim |
| `scripts/compliance_coverage.py` | `.github/scripts/compliance_coverage.py` | Copy verbatim — **skip if `compliance.enabled = false`** |
| `workflows/docs-guard.yml` | `.github/workflows/docs-guard.yml` | Strip `compliance_coverage` step if disabled |
| `commands/spec-audit-next.md` | `.claude/commands/spec-audit-next.md` | Placeholder substitution; strip conditional blocks |
| `commands/spec-quality-audit.md` | `.claude/commands/spec-quality-audit.md` | Placeholder substitution; strip conditional blocks |
| `review/README.md` | `{paths.review}/README.md` | Placeholder substitution; **prompt before overwrite** |
| `review/spec-quality-audit.md` | `{paths.review}/spec-quality-audit.md` | Placeholder substitution; prompt before overwrite |
| `review/_template/README.md` | `{paths.review}/_template/README.md` | Placeholder substitution |
| `review/_template/INDEX.md` | `{paths.review}/_template/INDEX.md` | Placeholder substitution |
| `review/_template/FINDING-template.md` | `{paths.review}/_template/FINDING-template.md` | Placeholder substitution |
| `guardrails/CLAUDE-section.md` | append to `CLAUDE.md` between markers | Placeholder substitution; strip conditional blocks |

Print the plan. Ask the user to confirm before writing anything.

## 5. Placeholder substitution (global)

Replace in-place in every text file being written:

| Placeholder | Source | Fallback when source empty |
|---|---|---|
| `{{PROJECT_NAME}}` | `project.name` | required — stop if empty |
| `{{PROJECT_OWNER}}` | `project.owner` | required |
| `{{SPEC_PATH}}` | `paths.spec` | `docs/spec` |
| `{{ADRS_PATH}}` | `paths.adrs` | `docs/adrs` |
| `{{REVIEW_PATH}}` | `paths.review` | `docs/review` |
| `{{DEPGAPS_PATH}}` | `paths.dependency_gaps` | empty (callers handle) |
| `{{COMPLIANCE_PATH}}` | `paths.compliance` | empty |
| `{{PLATFORM_REPO}}` | `platform_check.repo` | empty |
| `{{PLATFORM_REL_PATH}}` | `platform_check.relative_path` | empty |
| `{{TRACKER_PHRASE}}` | `tracker.reference_phrase` if `tracker.enabled` else empty | `the project tracker` |

## 6. Conditional-block processing

The kit files carry comment-fenced blocks for install-time stripping:

### Platform-check blocks

```
<!-- strip-if-no-platform-check:start -->
...content...
<!-- strip-if-no-platform-check:end -->
```

- If `platform_check.enabled = true`: keep content, remove the marker lines.
- If `platform_check.enabled = false`: delete the block (markers + content).

```
<!-- keep-if-no-platform-check:start -->
...content...
<!-- keep-if-no-platform-check:end -->
```

- Mirror: keep when disabled, delete when enabled.

### Compliance blocks

```
<!-- compliance-step-start -->
...content...
<!-- compliance-step-end -->
```

- If `compliance.enabled = true`: keep content, remove marker lines.
- If `compliance.enabled = false`: delete the block (markers + content).

Apply these transforms **after** placeholder substitution.

## 7. CLAUDE.md append (idempotent)

The managed section is bounded by:

```
<!-- spec-review-kit:start -->
...
<!-- spec-review-kit:end -->
```

- If no `CLAUDE.md` exists: create one with just the managed section.
- If `CLAUDE.md` exists and contains the start marker: replace everything between the markers (inclusive) with the new rendered section.
- If `CLAUDE.md` exists and does **not** contain the marker: append the section at end-of-file with a leading blank line.

## 8. Version marker

Write `.spec-review-kit-version` at repo root with:

```
<kit git sha>
installed: <ISO date>
platform_check: <true|false>
compliance: <true|false>
tracker: <true|false>
scaffold_profile: <profile name or "n/a">
```

Get the kit sha via `git -C ~/.claude/skills/init-spec-review rev-parse HEAD`.

## 9. Report

```
WROTE  .spec-review.toml .spec-review-kit-version
SCAFF  <paths.spec>/README.md, glossary.md, architecture/*, shared/*
       <paths.spec>/<unit-tree>
       <paths.adrs>/README.md, 0001-architecture-and-stack.md
       [<paths.dependency_gaps>/INDEX.md, _template/*]
       [<paths.compliance>/INDEX.md, _template/*]
COPIED .github/scripts/docs_guard.py
       [.github/scripts/compliance_coverage.py]
       .github/workflows/docs-guard.yml
       .claude/commands/spec-audit-next.md
       .claude/commands/spec-quality-audit.md
       <paths.review>/README.md, spec-quality-audit.md, _template/*
APPEND CLAUDE.md § Spec review (markered)

NEXT   1. edit .spec-review.toml allowlist for your repo's vocabulary
       2. run `python .github/scripts/docs_guard.py` — must pass before any spec change
       3. fill in `_(fill in: ...)_` placeholders in scaffolded files
       4. run `/spec-quality-audit preflight` to validate the install
```

## 10. Reconfigure

When `$ARGUMENTS = reconfigure`:

1. Load current `.spec-review.toml`.
2. Run § 2 config gathering with current values as defaults.
3. Re-render every text file through § 5 + § 6 (new tracker, new paths, new flags).
4. Append / replace the CLAUDE.md section between markers.
5. Do NOT re-scaffold; existing `docs/spec/` content is user-authored by now.
6. Report:

```
RECFG  .spec-review.toml
RERENDER .github/workflows/docs-guard.yml
       .claude/commands/{spec-audit-next,spec-quality-audit}.md
       <paths.review>/{README,spec-quality-audit}.md + _template/*
REFRESH CLAUDE.md § Spec review (markered)
```

## 11. Uninstall

When `$ARGUMENTS = uninstall`:

1. List every installed kit file.
2. Prompt the user: `remove installed kit files? (y/N)` — list each.
3. On confirmation:
   - Delete scripts, workflow, commands, review folder (prompt once per folder).
   - Edit `CLAUDE.md`: remove everything between `<!-- spec-review-kit:start -->` and `<!-- spec-review-kit:end -->` inclusive.
   - Delete `.spec-review.toml` and `.spec-review-kit-version`.
4. **Do not** delete scaffolded `docs/spec/`, `docs/adrs/`, `docs/dependency-gaps/`, `docs/compliance/` — those contain user-authored content by now.
5. Report deleted paths.

## Guardrails

- **Never** delete files outside the install plan.
- **Never** overwrite `{paths.review}/*` or `{paths.spec}/*` without prompting — these may contain in-flight audits or filled-in spec content.
- **Never** write a `.spec-review.toml` with `platform_check.enabled = true` but empty `repo` / `relative_path`.
- **Never** write a `.spec-review.toml` with `tracker.enabled = true` but empty `reference_phrase`.
- **Never** write a `.spec-review.toml` with `compliance.enabled = true` but no `paths.compliance`.
- **Do not** commit the install — the user commits after reviewing.
- **Do not** re-scaffold on `reconfigure` or `update`.
- `.spec-review-kit-version` is write-only by this skill; don't let the repo's own tooling edit it.
