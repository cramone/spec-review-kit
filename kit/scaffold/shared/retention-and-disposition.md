# Retention and disposition

How long records are kept, when they move to disposition, and how disposition is executed.

## Retention schedule

A retention schedule names a class of records and the trigger / duration pair that determines when records in the class are eligible for disposition.

| Member | Meaning |
|---|---|
| `Class` | A domain classification — e.g. `Operational.General`, `Statutory.Personal` |
| `Trigger` | What starts the retention clock — `OnCreate`, `OnTerminalEvent`, `OnReview`, `OnExternalEvent` |
| `Duration` | How long after the trigger the record is eligible for disposition |
| `Action` | What disposition does — `Destroy`, `Transfer`, `Review` |
| `Authority` | The authority that mandates this schedule — statute, policy, standard clause |

A record is assigned a schedule at classification. A record under hold (legal, FOI, audit) is not disposed until the hold releases regardless of schedule.

## Disposition events

| Event | Meaning |
|---|---|
| `RetentionStarted` | The clock began — `Trigger` fired |
| `RetentionTransitioned` | The schedule assigned to a record changed (reclassification) |
| `DispositionScheduled` | The record passed its due date and is eligible for `Action` |
| `DispositionExecuted` | `Action` ran |
| `DispositionReversed` | A disposition was undone within an allowed window |

## Holds

A hold suspends disposition. A record under hold is not disposed when its schedule matures; the schedule continues to run; disposition occurs once every hold on the record is released.

| Hold kind | Who may apply | Who may release |
|---|---|---|
| Legal | legal-hold permission | legal-release permission |
| Audit | audit permission | audit permission |
| _(fill in)_ | _(permission)_ | _(permission)_ |

## Compliance

The retention schedule and disposition path are cited from each applicable standard under [`../../compliance/`](../../compliance/).

_(fill in: the specific schedule classes relevant to this system's domain, and the authority each class cites. Keep each row to one line.)_
