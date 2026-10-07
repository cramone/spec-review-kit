# API conventions

HTTP-level conventions every route in {{PROJECT_NAME}} follows.

## Media type

`application/json` for request and response bodies. Problem responses use `application/problem+json` per RFC 9457.

## Idempotency

Mutating requests carry an `Idempotency-Key` header per `draft-ietf-httpapi-idempotency-key-header-07`. The first request with a given key is processed; subsequent requests with the same key within the TTL return the cached response. See [`error-catalog.md`](./error-catalog.md) for the `IdempotencyKeyMismatch` code.

Caller-supplied aggregate ids provide a second idempotency leg: a `POST` to create an aggregate carries its id in the body, and a duplicate id returns `409 <Aggregate>AlreadyExists` from the conditional write.

## Concurrency

Routes that update a specific version require `If-Match` with the current `AggregateVersion` in quotes. A mismatch returns `412 VersionMismatch` per RFC 9110 § 13.1.1. A route whose contract does not include an `If-Match` requirement refuses an unexpected `If-Match` with `400 InvalidIfMatch`.

## Refusal precedence — state before the resource predicate

Every route checks guards in a fixed order; the first failure is what the caller sees.

1. **Permission at the edge** — role / claim gate. On miss: `403 NotPermitted`.
2. **Existence** — does the resource exist in the caller's tenant? On miss: `404 <Aggregate>NotFound`.
3. **State** — is the aggregate in a status that permits this command? On miss: `409 <Aggregate>StateInvalid` or `422 <Aggregate>Precondition<X>Failed`.
4. **Resource predicate** — owner/membership/custody match. On miss: `403 NotResourceOwner` (or more specific).

The predicate runs **after** state, which means a caller unauthorised by predicate sees a state-based refusal when the aggregate is in a disallowed state. The design accepts the existence-and-state disclosure that implies: a caller with permission-at-edge but no predicate match can learn an aggregate's status. The alternative — hiding state behind the predicate — produces fragile client behaviour and worse errors in the common case.

## Error shape

Every error response follows RFC 9457. The problem body carries at least:

| Member | Meaning |
|---|---|
| `type` | URI identifying the error class — a stable permalink into [`error-catalog.md`](./error-catalog.md) |
| `title` | Short human-readable summary |
| `status` | HTTP status code |
| `detail` | Human-readable description of this specific occurrence |
| `errorCode` | The catalogue code (e.g. `{{Unit}}NotFound`) — root-level, not nested |
| _(extension members)_ | Per-code; see each row in the catalogue |

Clients branch on `errorCode`, not on `detail`.

## Pagination

Collection routes return a `nextPageToken` when more results exist. Treat the token as opaque; it carries index state and should be considered internal key material (do not log).

_(fill in: additional conventions — API versioning, deprecation policy, caching, cors, rate limiting.)_
