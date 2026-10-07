# Bounded contexts

The regions of the domain, each with its own ubiquitous language and invariants, and the integration events that cross between them.

## Context map

| Context | Owns | Depends on (as consumer of integration events) |
|---|---|---|
| _(fill in: context name)_ | _(aggregates / topics)_ | _(upstream contexts)_ |

## Integration events

Integration events are the only coupling across contexts. Each event's `type` string, payload members, and the subscriber contexts are specified. The published contract is pinned; moving to a new contract is a dual-publish or new-version migration, not a quiet change.

See [`../shared/event-store-and-messaging.md`](../shared/event-store-and-messaging.md) § Integration Events for the full catalogue once it exists.

## External contexts

| Context | Role | Boundary |
|---|---|---|
| _(fill in: upstream identity provider / downstream analytics / third-party integration)_ | _(role)_ | _(what crosses — JWT, event, webhook)_ |

An external context is not inside {{PROJECT_NAME}}; its contract is a dependency, not a specified behaviour of this system.
