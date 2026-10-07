# Operations

Runtime concerns that span the system — concurrency, fairness, scaling, back-pressure, back-off.

## Concurrency

Hosts run under reserved concurrency limits per deployment environment. The limits are chosen so a single tenant's traffic does not exhaust the shared pool.

| Host | Reserved concurrency | Reason |
|---|---|---|
| Write API | _(fill in)_ | Protects event-store write path |
| Read API | _(fill in)_ | Isolates query latency |
| Projector | _(fill in)_ | Bounds projection lag |
| _(fill in: other hosts)_ | _(fill in)_ | _(fill in)_ |

## Fairness

Shared queues apply per-tenant fairness so one tenant's bulk operation does not starve another's regular traffic. The fairness mechanism is a per-tenant budget on dispatch per unit time; a tenant that exceeds its budget is scheduled behind other tenants.

## Scaling

Autoscaling rules per host are stated in the deploy spec, not here. This file names the invariants the autoscaler must honour.

- Projector concurrency does not exceed the event-store's read capacity under projection replay
- The write API's conditional-write retry is bounded; a retry storm does not amplify a conflict burst
- The outbox relay runs continuously; a scaled-down relay is a backlog, not a loss

## Back-off

Retried operations use exponential back-off with jitter. The ceiling and attempt count are per operation:

| Operation | Max attempts | Backoff ceiling |
|---|---|---|
| Event-store conditional write (concurrency conflict) | 3 | 100 ms |
| SNS publish from outbox relay | 10 | 30 s |
| Projection replay (per batch) | 5 | 10 s |
| _(fill in)_ | _(count)_ | _(ceiling)_ |

## Observability

| Metric | Dimension | Reason |
|---|---|---|
| Projection lag per table | per tenant | Alerts when a read is stale |
| Outbox parked entries | per aggregate type | Signals a publication defect |
| Conditional-write retry rate | per aggregate type | Flags hotspots |
| _(fill in)_ | _(dimension)_ | _(reason)_ |

_(fill in: name the monitoring stack and the dashboards operators consult. Specific dashboard URLs live out-of-repo, not in this file.)_
