# {{Unit}} — scenarios

Given/When/Then coverage for invariants, errors, and state transitions in [`{{unit}}.model.md`](./{{unit}}.model.md).

## Create

Example literals: aggregate id `aggregate-one`.

### C-1 — creates a new `{{Unit}}`

**Given** no `{{Unit}}` with id `aggregate-one` exists
**When** `Create{{Unit}}` is issued with id `aggregate-one`
**Then** the row is persisted with status `Draft`
**And** the response is `201 Created`

_(fill in: further C-N scenarios covering every precondition and invariant)_

## Update

_(fill in: U-N scenarios per invariant and error)_

## Delete

_(fill in: D-N scenarios)_
