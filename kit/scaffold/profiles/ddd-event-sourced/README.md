# {{PROJECT_NAME}} — specification

Specification for the {{PROJECT_NAME}} system. Present tense; one source of truth per rule. See [`CLAUDE.md § Spec review`](../../CLAUDE.md) for the guardrails every spec file in this tree follows.

## Layout

| Path | Content |
|---|---|
| [`glossary.md`](./glossary.md) | Domain terms with one-line definitions |
| [`architecture/`](./architecture/) | System diagrams, domain model, bounded-context map |
| [`shared/`](./shared/) | Cross-cutting concerns — API conventions, error catalogue, event store, auth |
| [`contexts/`](./contexts/) | Bounded contexts; one folder per context; aggregates under `contexts/<Name>/aggregates/<Aggregate>/` |

## How to read

Start at `architecture/system-architecture.md` for the shape. `architecture/bounded-contexts.md` names each context and what it owns. Each context's aggregates carry four files: `*.api.md` (routes), `*.write-model.md` (commands, invariants, events), `*.read-model.md` (projections, keys, indexes), `*.scenarios.md` (given/when/then coverage).

Shared files state once what every aggregate inherits — refusal precedence, tenant source, event envelope shape, retry contract. A per-aggregate file does not restate a shared rule; it points at the shared file.

## How to change

A spec change lands in the same commit as the code change it describes. A rule change that touches more than one file opens a spec-quality audit via `/spec-quality-audit`; the audit folder lives at [`../review/`](../review/) and iterates one unit per `/spec-audit-next` run.

Rationale and rejected options live in [`../adrs/`](../adrs/), never in a spec file. Deployment state and known gaps live in `CLAUDE.md § Known deferred/partial work`, never in a spec file.
