# {{PROJECT_NAME}} — specification

Specification for the {{PROJECT_NAME}} system. DDD with CRUD read/write — aggregates have one state class, no event stream.

## Layout

| Path | Content |
|---|---|
| [`glossary.md`](./glossary.md) | Domain terms |
| [`architecture/`](./architecture/) | System shape and bounded contexts |
| [`shared/`](./shared/) | Cross-cutting concerns |
| [`contexts/`](./contexts/) | Bounded contexts; aggregates under `contexts/<Name>/aggregates/<Aggregate>/` |

Each aggregate carries three files: `*.api.md` (routes), `*.model.md` (state + commands + invariants), `*.scenarios.md` (coverage).
