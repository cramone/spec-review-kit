# Glossary

Domain terms used across the specification. Each term is defined once here; spec files cite the term, not restate the definition.

| Term | Definition |
|---|---|
| Aggregate | A consistency boundary — a cluster of entities and value objects that change together under one invariant set. _(fill in: name the aggregates this system has, link each to its folder)_ |
| Bounded context | A region of the domain with its own ubiquitous language. Separated from other contexts by explicit integration events. _(fill in: list contexts)_ |
| Command | A request to change state. Validated against invariants; refused or accepted; on accept, appends events. |
| Domain event | A fact about something that happened in the past. Immutable; carries the state change needed to replay the aggregate. |
| Event stream | The ordered sequence of events for one aggregate instance. Keyed by aggregate id. |
| Integration event | A domain event republished across bounded contexts. Shape is a published contract; the stream is subscribed to by other contexts. |
| Projection | A read-model row derived from an event stream. Rebuilt by replay. |
| Read model | A query-optimised shape; projected from events. Eventually consistent with the stream. |
| Snapshot | A compacted aggregate state at a specific version. Loaded instead of replaying from zero. |
| Tenant | The isolation key. Every stored row, every event, every command carries the tenant. |

_(fill in: add domain-specific terms as the spec grows — e.g. a resource lifecycle, a workflow stage name, a classification scheme name. Keep each entry to one sentence.)_
