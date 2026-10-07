# Error catalogue

Every error code the system can return, its HTTP status, and the extension members its RFC 9457 problem response carries.

## Shape

See [`api-conventions.md`](./api-conventions.md) § Error shape for the base response members. Each row below names its extension members and the caller-facing remediation guidance.

## Catalogue

| Code | Status | Extension members | Caller action |
|---|---|---|---|
| `NotPermitted` | 403 | `permission` | Re-check role grants; the caller lacks the stated permission |
| `NotResourceOwner` | 403 | `resourceId`, `resourceType` | The caller is not the owner / editor / assigned reviewer for this resource |
| `NotFound` | 404 | `resourceId`, `resourceType` | The resource does not exist in the caller's tenant |
| `AlreadyExists` | 409 | `resourceId` | A resource with this id already exists (idempotency hint: this is a duplicate create) |
| `StateInvalid` | 409 | `currentState`, `allowedStates` | The resource is in a state that does not permit this command |
| `VersionMismatch` | 412 | `expectedVersion`, `currentVersion` | Reload and retry; the resource was modified between read and write |
| `InvalidIfMatch` | 400 | — | The route does not accept `If-Match`; remove the header |
| `IdempotencyKeyMismatch` | 422 | `storedKey` | A different `Idempotency-Key` was previously used for this request shape |
| `TenantUnknown` | 401 | — | The JWT carries no `tenant_id` claim, or the tenant is not known |
| `TenantDisabled` | 403 | — | The tenant is in a disabled state; no requests are served |
| `ValidationFailed` | 400 | `errors` (array of `{field, message}`) | Fix the input per the listed field errors |
| _(fill in: aggregate-specific codes)_ | _(status)_ | _(extensions)_ | _(action)_ |

## Conventions for new codes

- One code, one meaning. A code that fires for two unrelated conditions is split.
- Status reflects the condition's RFC meaning: `409` for a conflict with current state, `412` for a precondition on a specific version, `422` for a semantically-valid request the business rules refuse.
- Every extension member is listed in this file. A member seen on the wire but not catalogued is a defect in the catalogue, not a feature of the client.
- Caller action is written for a human reading the problem response — it says what to do, not what the server did.
