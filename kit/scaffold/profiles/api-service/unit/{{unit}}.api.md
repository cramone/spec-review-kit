# {{Unit}} — API

HTTP endpoints for the `{{unit}}` resource.

## Endpoints

| Method | Path | Permission | 2xx | Errors |
|---|---|---|---|---|
| GET | `/v1/{{unit}}s` | `{{unit}}.read` | 200 (list) | 400 |
| GET | `/v1/{{unit}}s/{id}` | `{{unit}}.read` | 200 (`{{Unit}}`) | 404 |
| POST | `/v1/{{unit}}s` | `{{unit}}.create` | 201 (`{{Unit}}`) | 400, 409, 422 |
| PATCH | `/v1/{{unit}}s/{id}` | `{{unit}}.edit` | 200 (`{{Unit}}`) | 404, 409, 412, 422 |
| DELETE | `/v1/{{unit}}s/{id}` | `{{unit}}.delete` | 204 | 404, 409, 422 |

_(fill in: route per endpoint. If this resource is immutable, drop PATCH/DELETE and say so.)_

## Representation

Canonical `{{Unit}}` shape returned by GET and used as the response body of POST / PATCH.

| Field | Type | Required | Absent means |
|---|---|---|---|
| `id` | string | yes | — |
| `createdAt` | ISO 8601 string | yes | — |
| _(fill in)_ | _(type)_ | _(req?)_ | _(absent means ...)_ |

## Authorization

Permission at the edge, then existence, then state. See [`../../shared/api-conventions.md`](../../shared/api-conventions.md).

## Errors

See [`../../shared/error-catalog.md`](../../shared/error-catalog.md).

| Code | Status | Returned by |
|---|---|---|
| `{{Unit}}NotFound` | 404 | GET, PATCH, DELETE |
| _(fill in)_ | _(status)_ | _(routes)_ |
