# Cross-aggregate rules

Rules that hold across more than one aggregate in {{PROJECT_NAME}}. A rule stated here is the single source of truth; per-aggregate files cite the rule, not restate it.

## When a rule is cross-aggregate

A rule is cross-aggregate when its correctness depends on state in more than one aggregate — a reference between them, an ordering constraint, a shared classification, a lifecycle dependency.

A rule that depends only on one aggregate's state is **not** cross-aggregate; it is an invariant on that aggregate and lives in the aggregate's `*.model.md` or `*.write-model.md`.

## Catalogue

Each rule carries an id (`CAR-N`, numbered sequentially), a one-sentence statement, the aggregates it touches, and the enforcement site — which aggregate's handler, which saga, which projector verifies it.

| Id | Statement | Aggregates | Enforcement |
|---|---|---|---|
| _(fill in: id in form `CAR-N`)_ | _(one-sentence rule)_ | _(aggregates it spans)_ | _(where enforced)_ |

## Enforcement patterns

A cross-aggregate rule is enforced by one of:

- **Idempotent reaction** — a projector or saga reads an event from aggregate A, verifies the rule, dispatches a correcting command to aggregate B if needed. The reaction is idempotent so duplicate delivery is harmless.
- **Explicit saga** — a long-running coordination with explicit state. Appropriate when the rule has steps that must happen in order with compensation on failure.
- **Read-side read-your-writes** — the handler on aggregate A reads a read-model row for aggregate B before dispatching. Appropriate when B's state is stable and the staleness window is acceptable.

A rule enforced by **shared transaction** across aggregate boundaries is not supported — aggregates own their own consistency. A sentence of the form "update A and B atomically" is a design error; redesign so the rule is enforced by one of the three patterns above.

## Reference integrity

A member on aggregate A that references aggregate B carries the id, not the state. A projection reads B's read model to join at query time. A delete of B does not cascade to A automatically; the cross-aggregate rule names what happens on B's terminal event — ignore, mark A as orphaned, cascade via a projector.
