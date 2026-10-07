# {{PROJECT_NAME}} — specification

Specification for the {{PROJECT_NAME}} HTTP API. Resources are top-level; each has endpoints, request/response shapes, errors, and scenarios.

## Layout

| Path | Content |
|---|---|
| [`glossary.md`](./glossary.md) | Terms |
| [`architecture/`](./architecture/) | System shape |
| [`shared/`](./shared/) | Cross-cutting concerns — API conventions, error catalogue |
| [`resources/`](./resources/) | One folder per resource (or one file pair per resource at this root) |

Each resource carries `*.api.md` (endpoints) and `*.scenarios.md` (coverage).
