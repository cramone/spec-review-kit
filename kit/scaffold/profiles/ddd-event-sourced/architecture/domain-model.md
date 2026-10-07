# Domain model

The aggregates of {{PROJECT_NAME}}, their relationships, and the invariants that span more than one.

## Aggregates

| Aggregate | Context | Purpose | Key invariant |
|---|---|---|---|
| _(fill in: aggregate name)_ | _(context)_ | _(what it owns)_ | _(one-line invariant)_ |

Each aggregate's full specification lives under `../contexts/<Context>/aggregates/<Aggregate>/`.

## Relationships

_(fill in: how aggregates reference each other. By id only — no aggregate reaches into another's state. Cross-aggregate invariants are enforced by a saga or by eventual consistency, not by a shared transaction.)_

## Cross-aggregate rules

Rules that hold across more than one aggregate live in [`../shared/cross-aggregate-rules.md`](../shared/cross-aggregate-rules.md) once that file exists. Keep per-aggregate files local to one aggregate's invariants.

## Lifecycles

_(fill in: for each aggregate, state the terminal states and the transitions between non-terminal states. A state transition is a verb — `Draft` → `Published` on `Publish`.)_
