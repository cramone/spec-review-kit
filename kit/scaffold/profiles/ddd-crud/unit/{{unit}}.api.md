# {{Unit}} — API

HTTP routes acting on `{{Unit}}`.

## Routes

| Method | Path | Command | Permission | 2xx | Errors |
|---|---|---|---|---|---|
| POST | `/v1/{{unit}}s` | `Create{{Unit}}` | `{{unit}}.create` | 201 | 400, 409, 422 |
| GET | `/v1/{{unit}}s/{id}` | — | `{{unit}}.read` | 200 | 404 |
| PATCH | `/v1/{{unit}}s/{id}` | `Update{{Unit}}` | `{{unit}}.edit` | 200 | 404, 409, 412, 422 |
| DELETE | `/v1/{{unit}}s/{id}` | `Delete{{Unit}}` | `{{unit}}.delete` | 204 | 404, 409, 422 |

_(fill in: every route the aggregate exposes.)_

## Authorization

Permission at the edge, then existence, then state. Resource predicate: _(fill in)_.

## Errors

See [`../../../../shared/error-catalog.md`](../../../../shared/error-catalog.md).

| Code | Status | Returned by |
|---|---|---|
| `{{Unit}}NotFound` | 404 | GET, PATCH, DELETE |
| _(fill in)_ | _(status)_ | _(routes)_ |
