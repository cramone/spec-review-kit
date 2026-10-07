# {{Unit}} — model

The `{{Unit}}` aggregate — state, commands, invariants.

## State

| Member | Type | Default | Meaning |
|---|---|---|---|
| `Id` | `{{Unit}}Id` | — | Caller-supplied UUID v7 |
| `TenantId` | `TenantId` | — | Isolation key |
| `Status` | `{{Unit}}Status` | `Draft` | Current lifecycle state |
| _(fill in)_ | _(type)_ | _(default)_ | _(meaning)_ |

### Status enum

| Member | Meaning |
|---|---|
| `Draft` | Initial state |
| _(fill in)_ | _(meaning)_ |

## Commands

| Command | Purpose | Preconditions |
|---|---|---|
| `Create{{Unit}}` | Mint | aggregate does not exist |
| `Update{{Unit}}` | Change | aggregate exists; version matches |
| `Delete{{Unit}}` | Terminal | aggregate exists; status permits |
| _(fill in)_ | _(purpose)_ | _(preconditions)_ |

## Invariants

- **I-1 — _(fill in)_** _(fill in: one-sentence rule)_

## Status transitions

| From | On | To |
|---|---|---|
| _(initial)_ | `Create{{Unit}}` | `Draft` |
| _(fill in)_ | _(fill in)_ | _(fill in)_ |

## Errors

| Code | Status | Raised by |
|---|---|---|
| `{{Unit}}NotFound` | 404 | Any command on missing id |
| `{{Unit}}StateInvalid` | 409 | Precondition fails on `Status` |
| `VersionMismatch` | 412 | `If-Match` does not match |
| _(fill in)_ | _(status)_ | _(context)_ |
