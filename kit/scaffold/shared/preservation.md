# Preservation

Long-term preservation of records in {{PROJECT_NAME}} — fixity, format migration, archival ingest and dissemination.

## Fixity

Every stored artefact carries a checksum captured at ingest. A fixity check compares the stored artefact's checksum against the recorded one on a schedule and on access.

| Member | Meaning |
|---|---|
| `Checksum` | SHA-256 of the artefact at ingest |
| `ChecksumVerifiedAt` | The last time a fixity pass confirmed the artefact matched |
| `ChecksumAlgorithm` | `sha-256` (one algorithm; a change is a migration recorded in `CLAUDE.md`) |

A fixity failure raises `FixityFailure` and marks the artefact for review. The original stream is not altered.

## Format migration

Where a record is retained longer than its native format is readable, a format migration is a derivative — a new artefact in a currently-readable format, linked to the original. The original is preserved; the derivative is marked as such and carries its own fixity.

| Migration event | Meaning |
|---|---|
| `FormatMigrationPerformed` | A new derivative was produced |
| `FormatMigrationFailed` | A migration pass refused — manual review |

## Archival information package (AIP)

The AIP groups a record's artefacts, metadata, and audit history into a package suitable for long-term custody. The AIP shape follows the OAIS reference model.

_(fill in: name the SIP (ingest) and DIP (dissemination) package shapes used, and the standard the AIP targets — ISO 14721 OAIS, PREMIS, METS.)_

## Compliance

Preservation obligations are cited from the applicable archival standards under [`../../compliance/`](../../compliance/).
