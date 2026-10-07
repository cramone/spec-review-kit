# Contracts

Library-wide invariants {{PROJECT_NAME}} maintains and consumers may rely on.

## Public surface

The public surface is the set of types, functions, and extension points exported from each module's `*.api.md`. A member not listed in a `*.api.md` is **not** part of the public surface — consumers that reach for it are relying on an unstated contract.

## Stability

| Stability tier | Meaning | Change policy |
|---|---|---|
| Stable | Breaking changes require a major-version bump | A rename is a new member plus deprecation of the old |
| Experimental | Prefixed with `Experimental` or documented as such | Breaking changes allowed between minor versions |
| Internal | Not exported; see access modifiers | May change in any release |

## Semver

The library follows semantic versioning. A patch release contains no public-surface changes. A minor release adds public members but does not change existing signatures or behaviour. A major release is permitted to break stable members.

## Nullability

A `*.api.md` names a member's nullability. A reference-type return is non-null unless marked otherwise. A nullable return names the "null means" condition — error, absent, or sentinel.

## Thread safety

Each module names its thread-safety contract in `*.contracts.md`:

- `thread-safe` — any method may be called concurrently
- `read-safe` — concurrent reads are safe; writes require external synchronisation
- `single-threaded` — all calls must come from one thread

A member whose thread-safety is not stated is implicitly `single-threaded`.

## Error contract

A function may throw only the exceptions listed in its `*.api.md` row. A function that catches and swallows an exception from a dependency names the swallowed condition in the row — a consumer reading the surface must know what the function does not propagate.

_(fill in: additional contracts specific to this library — resource ownership, disposal, lifetime, allocation guarantees.)_
