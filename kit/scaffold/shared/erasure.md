# Erasure

How a right-to-erasure request is executed in {{PROJECT_NAME}} — what is erased, what remains, and the audit trail of the erasure itself.

## Scope

Erasure removes PII attributes from a record. It does not delete the record — the audit trail remains, with the PII fields nulled or hashed.

| Attribute | Treatment on erasure |
|---|---|
| Direct identifier | Replaced with a stable hash (`sha256(value + per-tenant salt)`) |
| Free-text that may carry PII | Replaced with the string `_erased_` |
| Reference to another resource | Preserved (not PII in itself) |
| Audit metadata (actor id, correlation id) | Preserved |

The erasure itself is an auditable event: `PiiErased` carrying the resource id, the actor who authorised the erasure, and the authority cited.

## Trigger

| Trigger | Who may initiate |
|---|---|
| Data subject request | Caller with `erasure.initiate` permission after verifying the subject's identity |
| Retention schedule maturity with `Action = Destroy` | Automatic — the retention pass dispatches `EraseByRetention` |
| Legal mandate | Caller with `erasure.initiate.legal` with the authority cited in the command |

## Exclusions

Erasure does not apply when the record is under hold (see [`retention-and-disposition.md`](./retention-and-disposition.md) § Holds). A pending erasure for a held record is queued; the queue is drained when the hold releases.

Records subject to records-management obligations (statutory retention, archival mandate) are **not** erased by data-subject request — the obligation to retain overrides the right to erasure, and the subject is notified with the authority.

## Mechanics

The erasure path is projection-safe: the read-model projector reads the erased event and updates every projection carrying the attribute. A projection rebuild from the pre-erasure stream re-applies the erasure as the stream is replayed, so a rebuild does not restore the PII.

_(fill in: name the key-store or crypto-erasure mechanism if applicable — some systems delete the per-record encryption key rather than overwriting the ciphertext. State the design, not the deployment.)_
