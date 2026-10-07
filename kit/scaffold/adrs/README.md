# Architecture Decision Records

Decisions that shape {{PROJECT_NAME}}'s architecture, grouped by topic. Each ADR records the context, the decision, the alternatives considered, and the consequences.

ADRs are **not** spec files — they legitimately carry rationale, rejected options, attribution, dates, and the state the decision replaced. Spec files cite the ADR by topic + heading anchor; they do not restate rationale.

## Index

| ADR | Topic | Status |
|---|---|---|
| [`0001-architecture-and-stack.md`](./0001-architecture-and-stack.md) | Overall architecture and technology stack | Draft |

## How to add an ADR

1. Copy `0001-architecture-and-stack.md` to the next free number.
2. Fill in Context, Decision, Alternatives considered, Consequences.
3. Add the row to the Index above.
4. Point affected spec files at the ADR's heading anchors.

## Numbering

Four-digit, zero-padded, monotonic. A superseded ADR keeps its number; the superseding ADR links back to it and the superseded one's Status changes to `Superseded by NNNN`.

## Status vocabulary

| Status | Meaning |
|---|---|
| `Draft` | Under review; not yet in effect |
| `Accepted` | In effect |
| `Superseded by NNNN` | Replaced by a later ADR |
| `Rejected` | Not adopted; retained for the record of the rejection |
