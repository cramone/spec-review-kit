---
name: init-spec-review
description: Scaffold the spec-review kit into the current repo. Use when the user says "setup spec review", "install spec review kit", "init spec review kit", or runs /init-spec-review. Interactive — asks for project name, owner, platform-check repo, team names, custom tokens. Writes .spec-review.toml, copies scripts/workflow/commands/templates, appends a managed CLAUDE.md guardrail section.
allowed-tools: Read, Grep, Glob, Edit, Write, AskUserQuestion, Bash(git status:*), Bash(git rev-parse:*), Bash(ls:*), Bash(mkdir:*), Bash(cp:*), Bash(cat:*)
---

# init-spec-review

Scaffold the portable spec review kit into the current repo. This skill is executed from `~/.claude/skills/init-spec-review/` (a clone of `https://github.com/cramone/spec-review-kit`). The `kit/` folder next to this `SKILL.md` is the source material.

## Argument dispatch

Read `$ARGUMENTS`:

| Argument | Meaning |
|---|---|
| empty | **Install.** Pre-flight, gather config, copy kit files, append CLAUDE section. |
| `reconfigure` | Re-gather config and re-copy. Preserves existing `.spec-review.toml` values as defaults. |
| `update` | Re-copy files only. `.spec-review.toml` untouched; CLAUDE section refreshed between markers. |
| `uninstall` | Remove installed files + CLAUDE section (between markers). Prompt before each delete. |

## 1. Pre-flight

1. Confirm cwd is a git repo: `git rev-parse --show-toplevel`. If not, print `init-spec-review: not a git repo — stop` and exit.
2. Check for existing install: look for `.spec-review.toml` at repo root. If present and `$ARGUMENTS` is empty, offer:
   - `update` — re-copy, keep config
   - `reconfigure` — new config, re-copy
   - `abort`
3. Check for `docs/spec/` or `docs/adrs/`. If neither exists, warn: `kit assumes a spec-first repo; found no docs/spec/ or docs/adrs/ — continue?`
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
    platform_check.repo          — repo name (e.g. my-platform-sdk)
    platform_check.relative_path — path from repo root (e.g. ../my-platform-sdk)
guard.attribution.names — comma-separated people flagged in attribution grep
guard.attribution.teams — comma-separated team names
guard.allow_tokens.custom — comma-separated extra ALLOW_TOKEN entries (project-specific vocabulary)
guard.references.allow    — comma-separated out-of-repo filenames named in spec prose
compliance.enabled      — y / n
```

Build a `.spec-review.toml` dict from answers (merge with existing on `reconfigure`).

## 3. Install plan

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

## 4. Placeholder substitution

Replace in-place in every text file being written:

| Placeholder | Source |
|---|---|
| `{{PROJECT_NAME}}` | `project.name` |
| `{{PROJECT_OWNER}}` | `project.owner` |
| `{{SPEC_PATH}}` | `paths.spec` |
| `{{ADRS_PATH}}` | `paths.adrs` |
| `{{REVIEW_PATH}}` | `paths.review` |
| `{{DEPGAPS_PATH}}` | `paths.dependency_gaps` or empty |
| `{{COMPLIANCE_PATH}}` | `paths.compliance` or empty |
| `{{PLATFORM_REPO}}` | `platform_check.repo` or empty |
| `{{PLATFORM_REL_PATH}}` | `platform_check.relative_path` or empty |

## 5. Conditional-block processing

The kit files carry two kinds of comment-fenced blocks for install-time stripping:

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

## 6. CLAUDE.md append (idempotent)

The managed section is bounded by:

```
<!-- spec-review-kit:start -->
...
<!-- spec-review-kit:end -->
```

- If no `CLAUDE.md` exists: create one with just the managed section + a one-line heading above (`# {project.name}` if the user wants it, else bare section).
- If `CLAUDE.md` exists and contains the start marker: replace everything between the markers (inclusive) with the new rendered section.
- If `CLAUDE.md` exists and does **not** contain the marker: append the section at end-of-file with a leading blank line.

## 7. Version marker

Write `.spec-review-kit-version` at repo root with:

```
<kit git sha>
installed: <ISO date>
platform_check: <true|false>
compliance: <true|false>
```

Get the kit sha via `git -C ~/.claude/skills/init-spec-review rev-parse HEAD` (or equivalent — the skill folder's git state).

## 8. Report

```
WROTE  .spec-review.toml .spec-review-kit-version
COPIED .github/scripts/docs_guard.py
       [.github/scripts/compliance_coverage.py]   # if compliance enabled
       .github/workflows/docs-guard.yml
       .claude/commands/spec-audit-next.md
       .claude/commands/spec-quality-audit.md
       <review>/README.md
       <review>/spec-quality-audit.md
       <review>/_template/{README,INDEX,FINDING-template}.md
APPEND CLAUDE.md § Spec review (markered)

NEXT   1. edit .spec-review.toml allowlist for your repo's vocabulary
       2. run `python .github/scripts/docs_guard.py` — must pass before any spec change
       3. run `/spec-quality-audit preflight` to validate the install
```

## 9. Uninstall

When `$ARGUMENTS = uninstall`:

1. List every installed file (per the Install plan table).
2. Prompt the user: `remove installed kit files? (y/N)` — list each.
3. On confirmation:
   - Delete scripts, workflow, commands, review folder (prompt once per folder).
   - Edit `CLAUDE.md`: remove everything between `<!-- spec-review-kit:start -->` and `<!-- spec-review-kit:end -->` inclusive.
   - Delete `.spec-review.toml` and `.spec-review-kit-version`.
4. Report deleted paths.

## Guardrails

- **Never** delete files outside the install plan.
- **Never** overwrite `{paths.review}/*` without prompting — these may contain in-flight audits.
- **Never** write a `.spec-review.toml` with `platform_check.enabled = true` but empty `repo` / `relative_path`.
- **Do not** commit the install — the user commits after reviewing.
- `.spec-review-kit-version` is write-only by this skill; don't let the repo's own tooling edit it.
