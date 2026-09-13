# DDD in the Artifact-Driven Phases

This page maps each step of domain-driven design to one of the five phases of the
artifact-driven documentation model. Read [Domain-Driven Design](README.md) for the method and
[Artifact-Driven Documentation](../../documentation/artifact-driven/README.md) for the phases.

The domain model in `docs/domain/` is shared by all features. A feature reads it, and the phase
that owns a domain artifact updates it. A change updates the domain artifacts in place, in the
phase that owns them. A change to the context map is a decision.

## The phases

| Phase | Owner | DDD step | Output |
| --- | --- | --- | --- |
| 1 Requirements | Requirement expert | Strategic design. Name the subdomain and its type. Find or make the bounded context. List the actors, the business events, and the terms. | `docs/domain/README.md`, `glossary.md`, `context-<name>/README.md` without the messages and the component. The section `## Domain` in `changes/change-<name>/requirements/README.md`. |
| 2 Specifications | Solution expert | Tactical design. Fill the messages and the component of each context. Write one aggregate canvas for each aggregate with its invariants, commands, events, and policies. Write the contracts between the contexts. Select the implementation pattern. | `context-<name>/agg-<name>.md`, `context-map.md`, `changes/change-<name>/decisions/adr-<name>.md`. |
| 3 Plan | Solution expert | One task touches one bounded context. Upstream before downstream. | `changes/change-<name>/tasks/` with `**Context:**` on each task. |
| 4 Implementation | Implementation experts | Code the model in `services/<name>/`. Keep the domain rules in the domain code, the use cases in the application code, and the adapters in the infrastructure code. | The code and the tests. |
| 5 Version | Solution expert | No DDD step. The version copies the feature artifacts only. | `versions/<version>/` |

## How a feature artifact points to a domain artifact

Add a bold key line under the title of the feature artifact, in the same style as `**Master:**`
and `**Covers:**`. The value of `**Context:**` is the name of a folder in `docs/domain/`. The
value of `**Aggregate:**` is the name of a file in that folder without `.md`.

| Artifact | Key line | Value |
| --- | --- | --- |
| `requirements/README.md` | Section `## Domain` | A table with Subdomain, Type, Context, Actors, Events. |
| `req-<name>.md` | `**Context:**` | `context-<name>`, or a comma-separated list. |
| `spec-<name>.md` | `**Context:**` | `context-<name>`. |
| `spec-<name>.md` | `**Aggregate:**` | `agg-<name>`, or a comma-separated list. Present only if the specification changes an aggregate. |
| `task-<name>.md` | `**Context:**` | `context-<name>`. One context per task. |
| `adr-<name>.md` | `**Context:**` | `context-<name>`, or `domain` for a decision that changes the context map. |

Example:

```markdown
# spec-place-order: Place an order

**Master:** [Specifications](README.md)
**Covers:** req-order-placement
**Context:** context-ordering
**Aggregate:** agg-order
```
