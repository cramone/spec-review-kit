# Audit trail

The immutable record of actions taken in {{PROJECT_NAME}} — who did what, when, to which resource, with what outcome.

## Source

The event stream is the authoritative audit trail. Every event carries `OccurredAt`, `OriginatingActorId`, and the state change that resulted. An auxiliary audit-event stream is **not** written — the domain stream is the record.

A query shape for audit (actor history, resource history, time-window scan) is a projection of the stream; it is query-optimised, not source-of-truth.

## Members on every event

| Member | Meaning |
|---|---|
| `OccurredAt` | Clock time when the event was appended |
| `OriginatingActorId` | The caller's `sub` claim at the time of the triggering command |
| `CorrelationId` | Groups events that belong to the same user-visible operation |
| `CausationId` | The `MessageId` of the message that produced this event |
| _(fill in: `Authority` or similar — a citation for an event raised in response to a legal / regulatory decision)_ | _(when it is set and what it names)_ |

## Query shapes

| Query | Projection | Partition |
|---|---|---|
| By actor over a time window | audit-by-actor | `TENANT#{TenantId}#ACTOR#{ActorId}` |
| By resource | audit-by-resource | the resource's detail-row key |
| By time window | audit-by-day | `TENANT#{TenantId}#DAY#{Date}` |

_(fill in: name the stores and the index shapes used.)_

## Retention

Audit retention follows the records-retention schedule for the resource — the stream is not purged on a shorter cycle than the resource it describes. See [`retention-and-disposition.md`](./retention-and-disposition.md) once that file exists.

## Compliance

Audit coverage is cited from the compliance mapping under [`../../compliance/`](../../compliance/) — each standard's clause anchors into this file and into the per-aggregate `*.scenarios.md` that demonstrates it.
