# {{Unit}} — API

HTTP routes that act on the `{{Unit}}` aggregate. Permission requirements, request / response shapes, and error contracts.

## Routes

| Method | Path | Command | Permission | 2xx | Errors |
|---|---|---|---|---|---|
| POST | `/v1/{{unit}}s` | `Create{{Unit}}` | `{{unit}}.create` | 201 `{{Unit}}Created` | 400, 409, 422 |
| GET | `/v1/{{unit}}s/{id}` | — (query) | `{{unit}}.read` | 200 `{{Unit}}` | 404 |
| PATCH | `/v1/{{unit}}s/{id}` | `Update{{Unit}}` | `{{unit}}.edit` | 200 `{{Unit}}Updated` | 404, 409, 412, 422 |
| DELETE | `/v1/{{unit}}s/{id}` | `Delete{{Unit}}` | `{{unit}}.delete` | 204 | 404, 409, 422 |

_(fill in: add every route the aggregate exposes. Keep the Command column honest — one command per non-query route.)_

## Authorization

Every route checks permission at the edge (`403` on miss), then existence (`404`), then state (`409`/`422`), then any resource predicate (`403` on miss). The refusal precedence is stated once in [`../../../../shared/api-conventions.md`](../../../../shared/api-conventions.md) § Refusal precedence; this file does not restate it.

The resource predicate for `{{Unit}}` is: _(fill in: owner-id match, membership check, custody chain, etc.)_

## Request / response shapes

### `Create{{Unit}}`

Request body:

| Field | Type | Required | Absent means |
|---|---|---|---|
| `id` | UUID v7 | yes | — (caller-supplied; natural idempotency key) |
| _(fill in)_ | _(type)_ | _(req?)_ | _(absent means ...)_ |

Response: `201 Created` with the aggregate's canonical read-model shape. See [`{{unit}}.read-model.md`](./{{unit}}.read-model.md) § Detail row.

_(fill in: shape every other command's request and response. Reuse the aggregate's canonical read-model shape for GET responses; do not define a parallel API DTO.)_

## Errors

Every error returned by this route is listed in [`../../../../shared/error-catalog.md`](../../../../shared/error-catalog.md) with its status code and remediation. This file names the error codes a route returns; the catalogue defines them.

| Code | Status | Returned by |
|---|---|---|
| `{{Unit}}NotFound` | 404 | GET, PATCH, DELETE |
| `{{Unit}}AlreadyExists` | 409 | POST (duplicate id) |
| _(fill in)_ | _(status)_ | _(routes)_ |
