# Cascade rules

How a change to one resource propagates to its dependants — archive, delete, retention transition, custody change.

## Principles

A cascade is explicit. A spec statement that says "when X is archived, every Y that references X is also archived" names the saga or the projection that executes the cascade; it does not leave the propagation implicit in a database foreign key.

A cascade crosses the aggregate boundary; a change inside one aggregate's state is not a cascade.

## Catalogue

| Trigger | Dependant kind | Propagation path | Terminal behaviour |
|---|---|---|---|
| _(fill in: event or command)_ | _(the kind that cascades)_ | _(saga / projector / event handler)_ | _(what dependants end up in)_ |

## Idempotency

A cascade's dependant-level work is idempotent by `(TriggerId, DependantId)` — a replay of the trigger event does not re-apply the change. The projector or saga step records the pair before dispatching.

## Reversal

Where a cascade is reversible (archive-and-unarchive, hold-and-release), the reverse operates on the same set the forward applied to. The dependant set is captured at the moment the forward cascade executes, not re-queried at reverse time; otherwise a dependant added between forward and reverse would be reversed without having been applied.

## Scale

Cascades over large dependant sets run bounded. A long-running cascade is a saga; a bounded fan-out runs under an orchestration substrate (Step Functions Distributed Map, Durable Entities, etc.).

_(fill in: name the substrate used for cascades at scale, and the per-tenant fairness controls that prevent one tenant's cascade from starving another's.)_
