# Event store and messaging

The persistence model for domain events, the publication path to subscribers, and the storage boundaries every aggregate honours.

## Event store

One append-only store. Every aggregate's event stream is keyed by `TENANT#{TenantId}#AGG#{AggregateType}#ID#{AggregateId}`; events are ordered by `AggregateVersion` within a stream.

Optimistic concurrency: the write is a conditional put that refuses when the next version already exists. The command pipeline retries up to 3× with backoff; on exhaustion the caller sees `409 ConcurrencyConflict`.

## Envelope

Every event carries:

| Member | Meaning |
|---|---|
| `TenantId` | Isolation key; equals the stream's tenant |
| `AggregateId` | The stream's aggregate id |
| `AggregateVersion` | Monotonic within the stream |
| `OccurredAt` | Clock time at append |
| `MessageMetadata` | Carries `OriginatingActorId`, `CorrelationId`, `CausationId`, idempotency key |
| `Type` | Discriminator — `{AggregateType}.{EventName}@{EventVersion}` |
| `Data` | The event payload |

_(fill in: name the serialiser, the compaction scheme, and the storage technology. If the store supports streaming (DynamoDB Streams, Kafka, EventStoreDB), state so.)_

## Snapshots

A snapshot captures aggregate state at a specific `AggregateVersion`. Load path: fetch the latest snapshot; replay events since; fall back to full replay on snapshot read failure.

A snapshot shape change is a code-phase migration: the new snapshot version is written on next save; on load, an older version falls back to replay.

## Transactional outbox

Events publish through a transactional outbox written in the same transaction as the event-store append. The outbox relay reads committed entries and publishes to the message bus; on failure the entry is retried bounded; on exhaustion the entry is parked with `OutboxEntryParked`.

Without the outbox, a crash between append and publish loses a committed event — subscribers never see it.

## Message bus

Domain events republish to an internal topic; projectors subscribe. Integration events republish to a separate topic for cross-context fan-out; each subscriber context filters by `type`.

| Topic | Purpose | Subscribers |
|---|---|---|
| _(fill in: domain events topic)_ | Intra-context fan-out | Projectors in this context |
| _(fill in: integration events topic)_ | Cross-context fan-out | Other contexts and external systems |

## Integration events

An integration event is a domain event republished across contexts under a stable `type` string and payload. The `type` is the filter key in every subscriber's policy; the payload members are what subscribers parse.

**The published contract is pinned.** A member rename or type change is a new event version or a dual-publish window — see `CLAUDE.md` § Known deferred/partial work for how a migration is recorded.

| Event | Payload members (summary) | Subscribers |
|---|---|---|
| _(fill in: integration event name)_ | _(members)_ | _(subscriber contexts)_ |

## Storage boundaries

The event store, the read models, and the outbox each have different retention, read, and backup needs. The spec pins which attributes live where.

_(fill in: the key shapes of every stored table. Keep them specified; the deployed-to-specified migration goes in `CLAUDE.md`, not here.)_
