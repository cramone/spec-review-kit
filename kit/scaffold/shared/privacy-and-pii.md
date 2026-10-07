# Privacy and PII

How personally identifying information is identified, handled, and bounded in {{PROJECT_NAME}}.

## What counts as PII

| Category | Examples | Treatment |
|---|---|---|
| Direct identifiers | name, email, phone, government id | Stored only where the aggregate's business purpose requires |
| Indirect identifiers | user id, device id, IP address | Logged under rules that match the retention of the record |
| Sensitive | health, biometrics, financial, political | Stored under additional access controls stated per-aggregate |

A field containing PII is tagged in the aggregate's write-model so the audit, retention, and erasure paths treat it correctly.

## Minimisation

A command does not persist PII beyond what the aggregate's invariants require. A field required for input but not for stored state is not stored (free-text comments, derived display names).

## Access

PII access is permission-gated, and the permission's grant is audited. A permission like `<unit>.readPii` is distinct from `<unit>.read` — a role that reads redacted records does not read PII.

## Erasure

See [`erasure.md`](./erasure.md) for how the right to erasure is executed. The erasure path is the only one that removes stored PII before its retention schedule matures.

## Logging

Logs do not carry PII. A log line that would otherwise include PII either redacts the field or includes a reference (resource id) rather than the value. Structured logs under `MessageMetadata` carry actor and correlation ids, not names or emails.

_(fill in: name the data-protection framework the system is subject to — GDPR, Australian Privacy Principles, HIPAA, etc. — and reference the compliance mapping that cites specific clauses.)_
