# Saga patterns

Long-running processes that coordinate across more than one aggregate or across the boundary to an external system. The spec names each saga, its correlation key, its state transitions, and its compensation path.

## When a saga

A saga exists when a workflow:

- Spans more than one aggregate's command sequence
- Waits on an external callback or a timer
- Needs explicit compensation on failure of a later step

A workflow that fits inside one aggregate's command handler is **not** a saga — it is an invariant on the aggregate.

## Shape

Each saga is specified in its own file under `../contexts/<Context>/sagas/<SagaName>.md` with:

- **Correlation key** — the identifier that joins events to the saga instance
- **State machine** — states, transitions, terminal states
- **Steps** — ordered commands the saga dispatches
- **Timeouts** — per step, with the compensation triggered
- **Compensation** — on any step failure, what rolls back
- **Idempotency** — how a replayed event is absorbed as a no-op

## Orchestration substrate

_(fill in: name the orchestration substrate — Step Functions, Temporal, Durable Functions, Camunda, in-house. The substrate carries the state machine and timers; the spec states the saga's logical shape, not the substrate's internals.)_

## Approval is not a saga

A review or approval that happens inside one aggregate is an invariant on that aggregate, not a saga. A review session with reviewers assigned, decisions pending, and a terminal `Approved` / `Rejected` state is state on the aggregate; approval commands check the caller's assignment inside the aggregate's command handler.

A saga is appropriate when approval orchestrates work across multiple aggregates (e.g. "once approved, publish the resource and notify the subscribers via two separate aggregates").

## Catalogue

| Saga | Correlation key | Triggered by | Terminal states |
|---|---|---|---|
| _(fill in: saga name)_ | _(key)_ | _(initiating event)_ | _(success / failure states)_ |
