# {{Unit}} — read model

Query-optimised projections of the `{{Unit}}` aggregate. Projected from the event stream by a projector; eventually consistent with the write side.

## Tables

### `{{project-prefix}}-{{unit}}` — detail row

One row per `{{Unit}}` instance.

| Attribute | Shape |
|---|---|
| PK | `TENANT#{TenantId}#{{UNIT_UPPER}}#{{{Unit}}Id}` |
| SK | `DETAIL` |
| `TenantId` | `TenantId` |
| `{{Unit}}Id` | `{{Unit}}Id` |
| `Status` | `{{Unit}}Status` (stored as member name under a property-scoped `JsonStringEnumConverter`) |
| `ProjectedVersion` | `long` — the `AggregateVersion` the projector last applied |
| _(fill in: every projected member)_ | _(type)_ |

### `{{project-prefix}}-{{unit}}s` — list row

One row per `{{Unit}}` instance; shaped for list queries.

| Attribute | Shape |
|---|---|
| PK | `TENANT#{TenantId}#{{UNIT_UPPER}}S` |
| SK | `{{{Unit}}Id}` |
| _(fill in: projected summary members)_ | _(type)_ |

## Indexes

| Index | PK | SK | Query |
|---|---|---|---|
| _(fill in: index name — e.g. `GSI1` for a DynamoDB global secondary)_ | _(shape)_ | _(shape)_ | _(what it supports)_ |

## Projection rules

The projector reads events from the aggregate's stream and applies them in order, guarded by `ProjectedVersion`. A duplicate delivery (SQS at-least-once) is a no-op because the projector skips any event whose `AggregateVersion <= ProjectedVersion`.

| Event | Action on detail row | Action on list row |
|---|---|---|
| `{{Unit}}Created@1` | insert | insert |
| `{{Unit}}Updated@1` | merge members | merge members |
| `{{Unit}}Deleted@1` | mark terminal (keep for audit) or delete per retention rules | delete |
| _(fill in)_ | _(action)_ | _(action)_ |

## Snapshot

A snapshot of `{{Unit}}` state at a given version, stored for fast load.

| Member | Type | Meaning |
|---|---|---|
| `Version` | `long` | `AggregateVersion` the snapshot captures |
| `State` | `{{Unit}}State` | Full state at `Version` |
| _(fill in)_ | _(type)_ | _(meaning)_ |

A snapshot is a stored shape; adding a member is a code-phase migration (new snapshot version + fallback to replay on load miss). See [`../../../../shared/event-store-and-messaging.md`](../../../../shared/event-store-and-messaging.md) § Snapshots.
