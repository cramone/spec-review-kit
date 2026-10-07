# Taxonomy — mapping existing content to kit slots

Reference used by `/init-spec-review analyze` to classify each file in a target repo against the kit's expected structure. The classifier reads this file, scans each source, assigns a target slot + confidence.

A "slot" is a path shape in the installed kit tree. A source file may map to one slot, split across multiple slots, merge with other sources into one slot, remain in place (kit-irrelevant), or be deleted (obsolete).

## Target slots (common to all profiles)

| Slot | Path shape | Shape expected |
|---|---|---|
| spec root README | `{spec}/README.md` | Overview of the spec tree; cites children |
| glossary | `{spec}/glossary.md` | Domain terms table; one-sentence definitions |
| architecture — system | `{spec}/architecture/system-architecture.md` | Hosts, data stores, messaging, external systems |
| architecture — domain model | `{spec}/architecture/domain-model.md` | Aggregates/resources, relationships, lifecycles |
| architecture — bounded contexts | `{spec}/architecture/bounded-contexts.md` | Context map, integration events, external contexts |
| shared — api-conventions | `{spec}/shared/api-conventions.md` | HTTP conventions, media types, refusal precedence, error shape |
| shared — error-catalog | `{spec}/shared/error-catalog.md` | Every error code + status + extension members |
| shared — event-store-and-messaging | `{spec}/shared/event-store-and-messaging.md` | Event store, outbox, bus, snapshots |
| shared — multi-tenancy-and-auth | `{spec}/shared/multi-tenancy-and-auth.md` | Tenant source, actor types, permission model |
| shared — saga-patterns | `{spec}/shared/saga-patterns.md` | When a saga, shape, orchestration substrate |
| shared — audit-trail | `{spec}/shared/audit-trail.md` | Source, members, query shapes, retention |
| shared — cascade-rules | `{spec}/shared/cascade-rules.md` | Trigger → dependant propagation; reversal |
| shared — retention-and-disposition | `{spec}/shared/retention-and-disposition.md` | Schedules, holds, disposition events |
| shared — privacy-and-pii | `{spec}/shared/privacy-and-pii.md` | PII categories, minimisation, access, logging |
| shared — erasure | `{spec}/shared/erasure.md` | Scope, trigger, exclusions, mechanics |
| shared — preservation | `{spec}/shared/preservation.md` | Fixity, format migration, AIP |
| shared — operations | `{spec}/shared/operations.md` | Concurrency, fairness, scaling, back-off |
| shared — cross-aggregate-rules | `{spec}/shared/cross-aggregate-rules.md` | Rules spanning aggregates, enforcement patterns |
| shared — contracts (library) | `{spec}/shared/contracts.md` | Library-wide invariants, stability, semver, nullability |
| shared — extension-points (library) | `{spec}/shared/extension-points.md` | Interfaces, delegates, registration, policy hooks |
| unit — api | per profile; see Per-profile slots | HTTP routes / public methods |
| unit — write-model (ddd-event-sourced) | `{spec}/contexts/<Context>/aggregates/<Unit>/<unit>.write-model.md` | State, commands, invariants, events, status |
| unit — read-model (ddd-event-sourced) | `{spec}/contexts/<Context>/aggregates/<Unit>/<unit>.read-model.md` | Tables, indexes, projection rules, snapshot |
| unit — model (ddd-crud) | `{spec}/contexts/<Context>/aggregates/<Unit>/<unit>.model.md` | State + commands + invariants (unified) |
| unit — scenarios | `{spec}/.../<unit>.scenarios.md` | Given/When/Then coverage |
| unit — contracts (library) | `{spec}/modules/<Unit>/<unit>.contracts.md` | Invariants, extension points, policy hooks, threading |
| ADR README | `{adrs}/README.md` | Index of ADRs by number + topic |
| ADR | `{adrs}/<NNNN>-<slug>.md` | Context / Decision / Alternatives / Consequences |
| dep-gaps INDEX | `{depgaps}/INDEX.md` | Themes, pre-flight procedure, audit history |
| dep-gaps theme INDEX | `{depgaps}/<theme>/INDEX.md` | One theme's gap register |
| dep-gaps finding | `{depgaps}/<theme>/F<nnn>-<slug>.md` | Context, detection signals, specified vs observed |
| compliance INDEX | `{compliance}/INDEX.md` | List of standards + validation note |
| compliance standard | `{compliance}/<slug>.md` | Clause → spec/ADR anchor table |
| review (external) | `{review}/` | Managed by audit protocol; analyze does not reshape |

## Classification signals

### By filename

| Pattern | Likely slot | Confidence |
|---|---|---|
| `README.md` at repo root | `README.md` (kept in place, not kit slot) | high |
| `glossary.md` / `terms.md` / `vocabulary.md` | glossary | high |
| `architecture.md` / `arch.md` | architecture — system (or split if also carries domain model) | medium |
| `domain-model.md` / `data-model.md` / `aggregates.md` | architecture — domain model | high |
| `bounded-contexts.md` / `contexts.md` / `services.md` | architecture — bounded contexts | high |
| `api.md` / `api-conventions.md` / `rest.md` / `http.md` | shared — api-conventions | medium |
| `errors.md` / `error-codes.md` / `error-catalog.md` / `problem-details.md` | shared — error-catalog | high |
| `events.md` / `event-store.md` / `event-sourcing.md` / `messaging.md` | shared — event-store-and-messaging | high |
| `auth.md` / `authentication.md` / `authorization.md` / `tenancy.md` / `multi-tenancy.md` | shared — multi-tenancy-and-auth | high |
| `sagas.md` / `workflows.md` / `orchestration.md` | shared — saga-patterns | medium |
| `audit.md` / `audit-trail.md` / `activity-log.md` | shared — audit-trail | high |
| `cascade.md` / `propagation.md` / `delete-rules.md` | shared — cascade-rules | medium |
| `retention.md` / `disposition.md` / `records-retention.md` | shared — retention-and-disposition | high |
| `privacy.md` / `pii.md` / `data-protection.md` | shared — privacy-and-pii | high |
| `erasure.md` / `right-to-erasure.md` / `gdpr-article-17.md` | shared — erasure | high |
| `preservation.md` / `archival.md` / `fixity.md` / `oais.md` | shared — preservation | high |
| `operations.md` / `ops.md` / `scaling.md` / `runbook.md` | shared — operations (if design) or kept out of spec (if runbook) | low |
| `cross-aggregate.md` / `invariants.md` | shared — cross-aggregate-rules | medium |
| `<AggregateName>.md` or `<aggregate>-model.md` | likely needs split: api + write/read-model + scenarios | low |
| `<AggregateName>/api.md` / `<AggregateName>/write-model.md` / etc. | unit slots per profile | high |
| `adr-NNN-*.md` / `NNNN-*.md` in `docs/adrs/` or `docs/decisions/` | ADR | high |
| `CHANGELOG.md` | kept in place; not kit content | high |
| `CONTRIBUTING.md` | kept in place; not kit content | high |

### By content

Classifier reads the file. Score against each slot's content signals:

| Slot | Content signals |
|---|---|
| architecture — system | Lists hosts, databases, queues; names topology |
| architecture — domain model | Enumerates aggregates / resources + relationships |
| shared — api-conventions | References RFC 9110 / 9457 / idempotency key / If-Match |
| shared — error-catalog | Table of error codes + HTTP status |
| shared — event-store-and-messaging | References append-only / stream / outbox / SNS / Kafka / event version |
| shared — multi-tenancy-and-auth | References JWT claims / tenant isolation / permission model |
| shared — saga-patterns | References long-running / orchestrator / Step Functions / Temporal / compensation |
| unit — write-model | Lists commands, invariants, events, status transitions |
| unit — read-model | Lists projection tables, indexes, snapshot members |
| unit — scenarios | Given/When/Then structure |
| ADR | Context / Decision / Consequences / Status |
| dep-gaps finding | Specified behaviour vs observed divergence |
| compliance standard | Clause id → spec/ADR anchor mapping |

### By path

| Path prefix | Likely treatment |
|---|---|
| `docs/spec/` | Already in kit shape; map to matching slot by content |
| `docs/adrs/` or `docs/decisions/` | ADR slot |
| `docs/compliance/` | Compliance slot |
| `docs/reports/` / `docs/notes/` | Kept in place; not kit slot |
| `docs/review/` | Kept in place; audit protocol owns it |
| `docs/architecture/` | Architecture slots |
| `docs/api/` | Shared — api-conventions, or per-route under unit slot |
| `docs/old/` / `docs/archive/` / `docs/deprecated/` | Candidates for delete; low confidence any map |
| `src/**/README.md` | Kept in place (per-module readme) unless clearly spec content |
| Top-level `*.md` (not README/CONTRIBUTING/CHANGELOG/LICENSE) | Low confidence; inspect content |

## Actions

Each source file in the migration plan carries one of these actions:

| Action | Meaning |
|---|---|
| `move` | Source maps verbatim to one slot. `git mv`; no content change. |
| `move+trim` | Maps to one slot but needs trimming (drop editorial prose, change history, dates, attribution). Content transform at write-time. |
| `split` | Content spans multiple slots. User names the N target slots; auditor splits headings. |
| `merge` | Belongs with another source into one target slot. Grouped with other `merge` rows for the same target. |
| `keep` | Doesn't fit kit; leave in place. Listed in DIVERGENCES.md. |
| `delete` | Obsolete / superseded / empty. User confirms. |
| `tbd` | Needs human judgment; parked for manual review. |

## Confidence levels

| Level | Meaning | Classifier behaviour |
|---|---|---|
| high | Filename + content + path all point to one slot | `move` or `move+trim`, no questions |
| medium | Filename or content strongly indicates; path neutral or ambiguous | Flag for user review in plan |
| low | Only weak signals; multiple plausible slots | `tbd` with alternatives listed |

## Signals that force `keep`

A file is kept in place regardless of other signals if:

- Path is under `.github/`, `.vscode/`, `.idea/`, `scripts/`, `tools/`, `infra/`
- Content is predominantly code (fenced blocks exceed 60% of lines)
- Filename matches `LICENSE*`, `NOTICE*`, `AUTHORS*`
- File is a runbook (prose addressed to an operator reading now, not design-of-system)
- File is meeting notes (dates in headings, attendee lists)

## Signals that force `delete` candidacy

A file is proposed for delete (user confirms) if:

- Path contains `old/`, `archive/`, `deprecated/`, `legacy/`, `wip/`, `draft/` AND content is clearly superseded
- Content is a stub (fewer than 10 non-blank lines, no tables)
- Content is a copy of another file (identical hash after whitespace normalisation)
- File is a review artefact leaked outside `{review}/` (findings, worklists, meeting notes)

## Scope — what analyze walks

| Scope | Default |
|---|---|
| `docs/**/*.md` | yes |
| `README.md` (repo root) | yes |
| `CONTRIBUTING.md` | yes |
| `CHANGELOG.md` | yes (classify as `keep`) |
| `src/**/README.md` | yes |
| Top-level `*.md` (other) | yes |
| `.github/**/*.md` | no |
| `node_modules/**` | no |
| `cdk.out/**` | no |
| `bin/**` / `obj/**` | no |

Scope is overridable via `.spec-review.toml` `[analyze]` section (not yet rendered — add on first analyze run).
