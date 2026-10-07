# {{Unit}} — scenarios

Given/When/Then coverage for the invariants, errors, and state transitions declared in [`{{unit}}.write-model.md`](./{{unit}}.write-model.md). Each invariant has at least one scenario; each error code has at least one scenario; each state transition is walked.

## Create

Example literals used below: aggregate id `aggregate-one`, tenant id `tenant-primary`.

### C-1 — creates a new `{{Unit}}` from an authorised caller

**Given** no `{{Unit}}` with id `aggregate-one` exists in tenant `tenant-primary`
**When** `Create{{Unit}}` is issued with id `aggregate-one`, tenant `tenant-primary`, caller holding permission `{{unit}}.create`
**Then** the event store carries one new stream `TENANT#tenant-primary#AGG#{{project-prefix}}.{{unit}}#ID#aggregate-one` with event `{{Unit}}Created@1` at version 1
**And** the response is `201 Created` with the detail row shape

### C-2 — refuses a duplicate id

**Given** `{{Unit}}` `aggregate-one` exists in tenant `tenant-primary`
**When** `Create{{Unit}}` is re-issued with id `aggregate-one`, tenant `tenant-primary`
**Then** the response is `409 {{Unit}}AlreadyExists`
**And** no event is appended

_(fill in: further C-N scenarios covering every create precondition and the invariants that must hold after create)_

## Update

### U-1 — _(fill in: scenario demonstrating an invariant from § Invariants)_

**Given** _(precondition state)_
**When** `Update{{Unit}}` is issued with _(input)_
**Then** _(expected event and read-model result)_

### U-2 — refuses an `If-Match` on stale version

**Given** `{{Unit}}` `aggregate-one` is at `AggregateVersion` three
**When** `Update{{Unit}}` is issued with `If-Match: "2"`
**Then** the response is `412 VersionMismatch`
**And** no event is appended

_(fill in: further U-N scenarios covering every invariant and every error code from § Errors)_

## Delete

_(fill in: delete scenarios demonstrating the terminal transition and refusals of a delete against a state that does not permit it)_

## Projection

### P-1 — projector applies an event once

**Given** `{{Unit}}Updated@1` at version four arrives twice from the event bus
**When** the projector processes both deliveries
**Then** the detail row's `ProjectedVersion` is four
**And** the state members reflect the version-four payload exactly once

### P-2 — projector preserves monotonic version

**Given** the detail row has `ProjectedVersion` five
**When** `{{Unit}}Updated@1` at version four arrives (out-of-order delivery)
**Then** the projector drops the event
**And** `ProjectedVersion` remains five

_(fill in: further P-N scenarios per read-model table and index)_
