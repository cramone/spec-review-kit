# Fnnn — _(fill in: short title)_

```yaml
id: Fnnn
title: <same as heading>
theme: <theme folder name>
status: open               # open | in-progress | resolved | wont-fix
severity: <critical | major | minor>
raised: <YYYY-MM-DD>
owner: <name or role>
```

## Context

_(fill in: one paragraph. What is specified, what the system does today, and why the gap exists — missing SDK capability, infrastructure not provisioned, code written before the spec caught up.)_

## Detection signals

**Signals a spec-audit uses to recognise this gap.** Each signal is a phrase, pattern, or concept from the spec that touches the gap's territory. The audit's pre-flight greps the signals; a match means the gap owns the finding.

- _(fill in: signal 1)_
- _(fill in: signal 2)_

## Specified behaviour

_(fill in: what the spec says. Quote the relevant spec section with a link to it.)_

## Observed divergence

_(fill in: how the system diverges from the spec. State without softening — the spec is correct; this section describes the defect.)_

## Delivery plan

_(fill in: the workstream carrying resolution. Branch name, dependent gaps, acceptance criteria.)_

## Related findings

_(fill in: spec audit findings held by this gap. Each row links the audit folder + finding id. On resolution the findings close with `resolution: delivered by dependency-gaps/Fnnn`.)_

| Audit | Finding | Status |
|---|---|---|
