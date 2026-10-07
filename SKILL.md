---
name: init-spec-review
description: Scaffold / install / analyze / migrate the spec-review kit. Use when the user says "setup spec review", "install spec review kit", "scaffold spec", "analyze existing spec", "migrate to spec review kit", or runs /init-spec-review. Interactive — asks for project config and (optionally) scaffold profile. Supports analyze mode (classify existing content against kit slots; writes read-only reports) and migrate mode (walk the analysis plan interactively, backup first, apply approved moves).
allowed-tools: Read, Grep, Glob, Edit, Write, AskUserQuestion, Bash(git status:*), Bash(git rev-parse:*), Bash(git mv:*), Bash(git rm:*), Bash(ls:*), Bash(mkdir:*), Bash(cp:*), Bash(cat:*), Bash(date:*), Bash(python .github/scripts/docs_guard.py:*), Bash(python3 .github/scripts/docs_guard.py:*)
---

# init-spec-review

Scaffold the portable spec review kit into the current repo. This skill is executed from `~/.claude/skills/init-spec-review/` (a clone of `https://github.com/cramone/spec-review-kit`). The `kit/` folder next to this `SKILL.md` is the source material.

## Argument dispatch

Read `$ARGUMENTS`:

| Argument | Meaning |
|---|---|
| empty | **Install.** Pre-flight, gather config, scaffold if docs/spec empty, copy kit files, append CLAUDE section. |
| `scaffold` | **Scaffold only.** Create the spec tree per profile; stop before review-kit config. |
| `analyze` | **Analyze.** Read-only. Scan existing content, classify against kit slots, write four reports under `.spec-review-analysis-<date>/`. No file moves. See § 12. |
| `migrate` | **Migrate.** Read the latest analysis plan; back up current content to `.spec-review-backup-<date>/`; walk each row interactively (propose-only); log decisions. See § 13. |
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

## 12. Analyze

When `$ARGUMENTS = analyze`:

Classify every file in scope against the kit's slot taxonomy; emit four reports. **Zero file moves.** **Zero spec edits.** The analysis is a proposal the user reviews before migrate runs.

### 12a. Pre-flight

1. `git rev-parse --show-toplevel` — confirm git repo.
2. Load `.spec-review.toml` if present. If missing, run § 2 config gathering (defaults loaded from the kit's example) so the taxonomy knows which profile and paths to classify against. Save the resulting toml at `.spec-review.toml` so re-runs are consistent (ask user to confirm).
3. Compute analysis-date: `date -u +%Y-%m-%d`.
4. Create `.spec-review-analysis-<date>/`. If it exists, offer: `overwrite` / `append-suffix` (`-01`, `-02`) / `abort`.
5. Read `kit/analyze/taxonomy.md`. Load the per-profile unit shape from `kit/scaffold/profiles/<profile>/manifest.toml`.

### 12b. Walk scope

Scope from `kit/analyze/taxonomy.md § Scope`:

```
docs/**/*.md
README.md
CONTRIBUTING.md
CHANGELOG.md
src/**/README.md
<top-level>/*.md (except LICENSE/NOTICE/AUTHORS)
```

For each file:
- Read the file (full content for small files; first 200 lines + heading structure for large).
- Compute signals per `kit/analyze/taxonomy.md § Classification signals`:
  - Filename pattern match
  - Content signal match (phrase / structure)
  - Path prefix match
- Score against every target slot; pick top candidate.
- Assign confidence: `high` (filename + content + path agree), `medium` (two of three agree), `low` (one agrees).
- Determine action: `move` / `move+trim` / `split` / `merge` / `keep` / `delete` / `tbd`.

For files > ~400 lines or where confidence is `low`, consider delegating classification to the `Explore` agent in a batch to protect main context.

### 12c. Detect splits and merges

- **Split candidates:** a source file whose heading structure maps to multiple top-level slots (e.g. one file carrying `## HTTP`, `## State`, `## Errors`, `## Scenarios` → unit's api + write-model + error-catalog + scenarios).
- **Merge candidates:** multiple source files whose top candidate slot is the same (e.g. three files that all score for `shared/error-catalog.md`).

Group merge candidates by target slot before emitting the plan.

### 12d. Run docs_guard baseline

```bash
python .github/scripts/docs_guard.py
```

If `docs_guard.py` is not yet installed, note "guard-not-installed" in `GUARD-BASELINE.md` and skip. (The user can run guard after `/init-spec-review` installs it; re-run analyze to refresh.)

Capture raw output + per-check hit counts + top offending files.

### 12e. Emit reports

Copy `kit/analyze/templates/*.md` to `.spec-review-analysis-<date>/` with placeholders substituted:

| Placeholder | Source |
|---|---|
| `{{ANALYSIS_DATE}}` | computed date |
| `{{PROJECT_NAME}}` | config |
| `{{PROFILE}}` | config |
| `{{ANALYZE_SCOPE}}` | summary string of scope |
| `{{GUARD_OUTPUT}}` | raw docs_guard output |
| `{{SPEC_PATH}}` | config |
| `{{REVIEW_PATH}}` | config |

Fill in each report's table rows from the classifier's output.

### 12f. Report

```
ANALYZED <n> files
WROTE   .spec-review-analysis-<date>/MIGRATION-PLAN.md    (<n> rows)
        .spec-review-analysis-<date>/GAPS.md               (<n> missing slots)
        .spec-review-analysis-<date>/DIVERGENCES.md        (<n> kept-in-place)
        .spec-review-analysis-<date>/GUARD-BASELINE.md     (<total> hits)
BY ACTION   move:<n>  move+trim:<n>  split:<n>  merge:<n>  keep:<n>  delete:<n>  tbd:<n>
BY CONFIDENCE  high:<n>  medium:<n>  low:<n>

NEXT    1. Review MIGRATION-PLAN.md — edit any row the classifier got wrong
        2. Confirm GAPS.md recommendations
        3. Confirm DIVERGENCES.md kept-in-place list
        4. Run `/init-spec-review migrate` to apply decisions interactively
```

### 12g. Analyze guardrails

- Read-only. No `git mv`, `Write` to source files, or `Edit` to anything outside `.spec-review-analysis-<date>/`.
- No reports commit automatically. User reviews, optionally commits.
- Add `.spec-review-analysis-*/` to `.gitignore` if the user prefers reports stay local.
- The classifier's output is a proposal, not a verdict. Every row says "proposed" implicitly; the user corrects before migrate runs.

## 13. Migrate

When `$ARGUMENTS = migrate`:

Walk the latest `MIGRATION-PLAN.md` row by row. Every move / split / merge / delete requires **y/N** from the user. Back up the full target before any change.

### 13a. Pre-flight

1. `git rev-parse --show-toplevel`.
2. Confirm `.spec-review.toml` exists. If not, stop: `migrate requires an installed kit — run /init-spec-review first`.
3. Find the latest `.spec-review-analysis-*/MIGRATION-PLAN.md`. If none exists, stop: `migrate requires an analysis — run /init-spec-review analyze first`.
4. Confirm `git status` is clean (no uncommitted changes). If dirty, offer: `commit first` / `stash` / `abort`.
5. Compute migrate-date: `date -u +%Y-%m-%d`.

### 13b. Back up

Create `.spec-review-backup-<date>/`. Copy every source file named in `MIGRATION-PLAN.md` into the backup, preserving its original path:

```
.spec-review-backup-<date>/
  docs/
    old/
      auth.md
  README.md
```

Verify the backup file count matches the plan's row count. Write `.spec-review-backup-<date>/MANIFEST.md` listing every backed-up path.

### 13c. Walk the plan

Parse `MIGRATION-PLAN.md`. For each row (skip `keep` rows — they are no-ops):

Show the user:
```
[<i>/<n>] <source>
  action: <action>
  target: <target slot>
  confidence: <high|medium|low>
  notes: <notes>
```

Prompt options:
| Key | Meaning |
|---|---|
| `y` | Apply as proposed |
| `n` | Skip this row (leave source in place) |
| `e` | Open source in Read view; let user re-decide after reading |
| `t` | Change target slot (user types new path) |
| `a` | Change action (user picks from valid alternatives) |
| `q` | Quit the walk; progress persists in `MIGRATION-LOG.md` |

On `y`:
- `move`: `git mv <source> <target>`. If git move fails (not tracked), use `Write` to target + delete source.
- `move+trim`: Read source; apply trim transforms (strip change-history prose, dates in headings, attribution). `Write` to target with trimmed content. `git rm` source.
- `split`: for each named target slot, ask user which headings/sections go to that slot. Write each slice to its target. `git rm` source.
- `merge`: append source content under a `## From <source-path>` heading in the target (or into an existing matching heading if one exists). Second and subsequent merge-ins ask user for the merge strategy (append / replace / dedupe).
- `delete`: `git rm <source>` after confirming (second prompt: `delete <source>? (y/N)` — this is the irreversible one).

Log every decision + action to `MIGRATION-LOG.md`:
```
| Timestamp | Source | Decision | Target | Notes |
|---|---|---|---|---|
| 2026-10-07T14:22:00Z | docs/old/auth.md | applied move+trim | docs/spec/shared/multi-tenancy-and-auth.md | trimmed § History |
```

### 13d. Post-walk

1. Run `docs_guard`. Capture new hit count.
2. Append to `MIGRATION-LOG.md`:
```
## Baseline
- Pre-migration docs_guard hits: <baseline count>
- Post-migration docs_guard hits: <new count>
- Delta: <reduction>
```
3. Append to `CLAUDE.md § Known deferred/partial work` any `tbd` rows that were deferred (if the user chose `n` or `q`).

### 13e. Report

```
MIGRATED <n> rows applied of <total>
BACKED UP .spec-review-backup-<date>/ (<n> files)
LOG     .spec-review-backup-<date>/MIGRATION-LOG.md
GUARD   <baseline> → <new> hits (<delta> reduction)

DEFERRED <n> rows (skipped or quit mid-walk)
         Resume: `/init-spec-review migrate` picks up at the first unapplied row

NEXT    1. Review MIGRATION-LOG.md for every applied move
        2. Run `/spec-quality-audit` for the full standing audit — addresses remaining docs_guard hits + 16-quality semantic walk
        3. Fill in `_(fill in: ...)_` placeholders in any newly-created slots
        4. Commit the migration (one commit per logical group is recommended)
        5. Delete `.spec-review-backup-<date>/` once satisfied the migration is correct
```

### 13f. Migrate guardrails

- **Never** `git rm` a source without a y/N for that specific file.
- **Never** touch files not named in `MIGRATION-PLAN.md`.
- **Never** modify `.spec-review-backup-<date>/` after it is written.
- **Never** commit the migration — the user commits after reviewing.
- If a target file already exists before `move`/`move+trim`, prompt: `target <path> exists — append / overwrite / rename-source / skip?`
- If the user quits mid-walk, record the stopping index in `MIGRATION-LOG.md` so the next invocation resumes.

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
- **Do not** commit the install, scaffold, analyze, or migrate — the user commits after reviewing.
- **Do not** re-scaffold on `reconfigure` or `update`.
- **Do not** modify `.spec-review-analysis-*/` after analyze emits reports.
- **Do not** modify `.spec-review-backup-*/` after migrate writes the backup.
- **Never** run `git mv` or `git rm` in migrate without a y/N for that specific file.
- `.spec-review-kit-version` is write-only by this skill; don't let the repo's own tooling edit it.
