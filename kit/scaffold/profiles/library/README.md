# {{PROJECT_NAME}} — specification

Specification for the {{PROJECT_NAME}} library. The public API surface, invariants, extension points, and policy hooks consumers rely on.

## Layout

| Path | Content |
|---|---|
| [`glossary.md`](./glossary.md) | Terms |
| [`architecture/`](./architecture/) | Package shape and consumer model |
| [`shared/`](./shared/) | Cross-cutting contracts and extension points |
| [`modules/`](./modules/) | One folder (or one file pair) per public module |

Each module carries `*.api.md` (public types and functions) and `*.contracts.md` (invariants, extension points, policy hooks).
