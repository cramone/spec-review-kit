# Multi-tenancy and auth

How tenants are identified, how the actor is identified, and how permissions gate commands.

## Tenant source

The `TenantId` carried by every command, event, and read-model row is sourced from the JWT `tenant_id` claim on an HTTP request, or from `MessageMetadata.TenantId` on an SQS/bus message (rebuilt by the dispatch pipeline when the message was emitted inside this system).

A scheduled scanner acts on rows the scanner reads — the tenant is the row's `TenantId` attribute, bound into a per-dispatch execution context carrying a `System` actor.

**Never from a request body or query parameter. Never from a header outside the JWT.** A missing `tenant_id` claim refuses the request `401 TenantUnknown`.

## Actor types

| `actor_type` claim | Meaning | Issued to |
|---|---|---|
| `User` | A human caller or a tenant-provisioned M2M client | Standard tenant-scoped tokens |
| `System` | A platform-owned integration client | Platform integration clients only (never tenant-provisioned) |

Any other value is refused `401 TenantUnknown`.

## Permission model

Commands are permission-based. A permission is a dotted string (`<unit>.<verb>`). The permission service resolves the caller's role grants into the set of permissions they hold.

| Permission form | Example | Scope |
|---|---|---|
| `<unit>.<verb>` | `{{Unit}}.create` | Caller may perform `<verb>` on their own `<unit>`s |
| `<unit>.<verb>.all` | `{{Unit}}.read.all` | Caller may perform `<verb>` on any `<unit>` in the tenant (admin / cross-cutting role) |

The resource predicate for each route (owner, editor, assignee, custody chain) is stated in the route's `*.api.md`. The `.all` form widens the predicate; outside is `403 NotResourceOwner`.

## Token validation

Token validation is stateless — signature, standard claims, `exp`, audience. No replay detection, no revocation check, no per-request token state.

**`jti` is not a replay guard.** The `jti` claim is fixed at issuance; every request with the same token presents the same `jti`. Replay checks belong to credentials that are genuinely single-use (client assertions, refresh-token rotation, DPoP proofs) and live at the identity provider.

A leaked token is valid until `exp`; mitigation is the token TTL plus refresh-token revocation at the identity provider.

## Context accessor

The command pipeline binds an `IExecutionContext` for each dispatch, carrying `TenantId`, `Actor` (id, name, roles, type), and `MessageMetadata`. Handlers read the caller from the context, not from the command body — a command that carries an actor member is a defect.

_(fill in: platform-specific details — the context accessor implementation, how the pipeline rebuilds context from a bus message, how a scanner constructs context for a scheduled dispatch.)_
