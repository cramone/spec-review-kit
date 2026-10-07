# System architecture

The shape of {{PROJECT_NAME}} at the component level — hosts, data stores, message buses, external systems.

## Hosts

Each host deploys independently.

| Host | Role |
|---|---|
| _(fill in: write-side host — commands, event append)_ | _(fill in)_ |
| _(fill in: read-side host — queries)_ | _(fill in)_ |
| _(fill in: projector host(s) — SQS/stream triggered)_ | _(fill in)_ |
| _(fill in: worker hosts — processing, scheduled tasks)_ | _(fill in)_ |

## Data stores

| Store | Role |
|---|---|
| Event store | Append-only; one stream per aggregate; conditional write for optimistic concurrency |
| Read models | Query-shaped projections; rebuilt from events |
| _(fill in: search / object store / cache as applicable)_ | _(fill in)_ |

## Messaging

Domain events publish to an internal bus; projectors subscribe. Integration events publish on a separate topic for cross-context fan-out.

_(fill in: name the bus technology — SNS, Kafka, EventBridge — and reference the retry / DLQ contract in [`../shared/event-store-and-messaging.md`](../shared/event-store-and-messaging.md).)_

## External systems

| System | Direction | What crosses the boundary |
|---|---|---|
| _(fill in: identity provider)_ | inbound | JWT bearing tenant and actor claims |
| _(fill in: downstream subscriber)_ | outbound | Integration events on the published topic |

See [`bounded-contexts.md`](./bounded-contexts.md) for the context map and [`domain-model.md`](./domain-model.md) for the aggregate relationships.
