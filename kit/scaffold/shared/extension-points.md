# Extension points

Places where a consumer customises {{PROJECT_NAME}}'s behaviour by implementing an interface or passing a delegate.

## Shape

An extension point is a public interface or a public delegate type the library defines and the consumer provides an implementation for. The library invokes the consumer's implementation at specified call sites with specified inputs and expects specified outputs.

## Catalogue

| Extension point | Signature | Called when | Consumer contract |
|---|---|---|---|
| _(fill in: interface name)_ | _(signature)_ | _(call site)_ | _(what the implementation must honour)_ |

## Registration

| Mechanism | How a consumer registers | Scope |
|---|---|---|
| DI container | Register the interface with the container; the library resolves it | Per container instance |
| Explicit option | Pass the implementation as a parameter at bootstrap | Per bootstrap call |
| Static hook | Set the implementation on a static property | Process-wide |

_(fill in: name the mechanisms this library offers. Prefer DI container registration where available; name the static-hook option when a DI-less consumer path is supported.)_

## Policy hooks

A policy hook is an extension point whose default is sufficient for most consumers; replacing it customises behaviour that would otherwise be opinionated.

| Hook | Default behaviour | Replace to |
|---|---|---|
| _(fill in: hook name)_ | _(default)_ | _(reason a consumer overrides)_ |

## Lifetime

An extension point implementation is held by the library for its own lifetime. If the implementation holds resources (file handles, connections), the consumer provides a disposer that the library calls at shutdown.
