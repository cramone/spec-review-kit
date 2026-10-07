# Compliance mapping

Clause-to-spec anchors for each standard {{PROJECT_NAME}} is subject to. One file per standard; each file cites spec sections and ADR anchors as evidence that the standard's clauses are addressed by the design.

## Standards

| Standard | File | Status |
|---|---|---|
| _(fill in: standard name and version)_ | _(fill in: `<slug>.md`)_ | Draft |

## How a mapping works

Each mapping file is a table. Each row names a clause id (per the standard's own numbering), the clause's requirement, and the spec / ADR anchor that carries the behaviour satisfying it.

A clause whose spec section does not exist yet carries `tbd` in the anchor column; the compliance-coverage script reports these as unmapped rows.

A clause the system intentionally does not meet carries a cross-reference to a `wont-fix` dependency gap under [`../dependency-gaps/`](../dependency-gaps/) and the authority that permits non-coverage.

## Validation

The `compliance_coverage.py` script walks every mapping file and verifies:

- Every link into `docs/spec/` or `docs/adrs/` resolves to a real file and a real heading
- Every dependency-gap citation resolves to an existing Fnnn file

The script runs as part of the pre-flight step in `/spec-quality-audit`.

## Vocabulary

Compliance files **may** carry standard clause ids as citations (that is the file's job). `docs_guard` excludes this folder for that reason. Spec files **do not** carry standard clause ids — the mapping is one-way, from compliance to spec, never the reverse.
