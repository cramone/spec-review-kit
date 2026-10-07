# {{Unit}} — write model

The `{{Unit}}` aggregate — state, commands, invariants, events, status transitions. The write side of the CQRS pair; the read side lives in [`{{unit}}.read-model.md`](./{{unit}}.read-model.md).

```
[AggregateType("{{project-prefix}}.{{unit}}")]
```

_(fill in: pin the aggregate-type string once. Code emits this string in every event envelope; a change is a migration recorded in `CLAUDE.md` § Known deferred/partial work.)_

## State

| Member | Type | Default | Meaning |
|---|---|---|---|
| `Id` | `{{Unit}}Id` | — | Caller-supplied UUID v7 |
| `TenantId` | `TenantId` | — | Isolation key; immutable after create |
| `Status` | `{{Unit}}Status` | `Draft` (ordinal 0) | Current lifecycle state |
| _(fill in: every member)_ | _(type)_ | _(default)_ | _(meaning + absent-meaning if nullable)_ |

### Status enum

| Member | Ordinal | Meaning |
|---|---|---|
| `Draft` | 0 | Initial state after create |
| _(fill in)_ | _(ordinal)_ | _(meaning)_ |

The ordinal is the stored shape; a reorder is a migration. Spec pins what a future migration would see.

## Commands

| Command | Purpose | Preconditions | Events on success |
|---|---|---|---|
| `Create{{Unit}}` | Mint a new instance | aggregate does not exist (conditional write refuses `409 {{Unit}}AlreadyExists`) | `{{Unit}}Created` |
| `Update{{Unit}}` | Change mutable state | aggregate exists; `Status != Terminal`; `If-Match` matches `AggregateVersion` | `{{Unit}}Updated` |
| `Delete{{Unit}}` | Terminal transition | aggregate exists; `Status in {allowed states}` | `{{Unit}}Deleted` |
| _(fill in)_ | _(purpose)_ | _(preconditions)_ | _(events)_ |

## Invariants

Rules that must hold after any successful command. The scenarios file demonstrates each one with a Given/When/Then.

- **I-1 — _(fill in: name the invariant)_** _(fill in: one-sentence rule)_
- **I-2 — _(fill in)_** _(fill in)_

Cross-aggregate invariants live in [`../../../../shared/cross-aggregate-rules.md`](../../../../shared/cross-aggregate-rules.md); this file carries only the ones local to `{{Unit}}`.

## Events

Each event's payload table is complete — every member, every type, every absent-meaning for nullable members.

### `{{Unit}}Created@1`

| Member | Type | Absent means |
|---|---|---|
| `TenantId` | `TenantId` | — |
| `{{Unit}}Id` | `{{Unit}}Id` | — |
| _(fill in)_ | _(type)_ | _(absent means ...)_ |

### `{{Unit}}Updated@1`

_(fill in: payload table per invariant that triggered)_

### `{{Unit}}Deleted@1`

_(fill in: payload table)_

## Status transitions

| From | On | To |
|---|---|---|
| _(initial)_ | `Create{{Unit}}` | `Draft` |
| `Draft` | _(command)_ | _(state)_ |
| _(fill in)_ | _(fill in)_ | _(fill in)_ |

A command whose preconditions name a `Status` disallowed transition refuses `409 {{Unit}}StateInvalid` with the current status named in the extension member `currentStatus`.

## Errors

Catalogue entries used by this aggregate. The full definition lives in [`../../../../shared/error-catalog.md`](../../../../shared/error-catalog.md).

| Code | Status | Raised by |
|---|---|---|
| `{{Unit}}NotFound` | 404 | Any command on a missing id |
| `{{Unit}}AlreadyExists` | 409 | `Create{{Unit}}` on duplicate id |
| `{{Unit}}StateInvalid` | 409 | Any command whose precondition fails on `Status` |
| `VersionMismatch` | 412 | Any command with an `If-Match` that does not match `AggregateVersion` |
| _(fill in)_ | _(status)_ | _(context)_ |
