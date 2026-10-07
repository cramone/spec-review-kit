# {{Unit}} — scenarios

Given/When/Then coverage for the endpoints in [`{{unit}}.api.md`](./{{unit}}.api.md).

## Read

Example literal: resource id `resource-one`.

### R-1 — returns a `{{Unit}}` by id

**Given** `{{Unit}}` with id `resource-one` exists
**When** the caller requests `GET /v1/{{unit}}s/resource-one` with permission `{{unit}}.read`
**Then** the response is `200 OK` with the canonical representation

### R-2 — refuses an unknown id

**Given** no `{{Unit}}` with id `resource-one` exists
**When** the caller requests `GET /v1/{{unit}}s/resource-one`
**Then** the response is `404 {{Unit}}NotFound`

_(fill in: further R-N scenarios for list filters, pagination, authorization edge cases)_

## Write

_(fill in: W-N scenarios per POST / PATCH / DELETE)_
