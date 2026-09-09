# Domain-Driven Design

Domain-driven design (DDD) is the design method of this project. It has two levels. The
strategic design finds the boundaries of the system. The tactical design models the parts inside
each boundary. Do the strategic design before the tactical design. A tactical pattern depends on
the type of the subdomain and on the boundary of the context that holds it.

The domain model of the project is in `docs/domain/`. Write the domain artifacts before the
code. Update the domain artifacts when the model changes.

## Strategic design

### Subdomains

A subdomain is a part of the business. Each subdomain has one type. The type tells you where to
invest.

| Type | Definition | How to find it | Where to invest |
| --- | --- | --- | --- |
| Core | The part that gives the business an advantage over the competition. The rules are complex and change often. | You cannot buy a product for it, and the rules are complex. | Deep model, custom code, the most experienced people. |
| Supporting | A part that the business needs, but that gives no advantage. The rules are simple. | You cannot buy a product for it, but the rules are simple. | Custom code that is good enough. |
| Generic | A part that the industry has solved. | You can buy or adopt a product without a loss of advantage. | An existing product. Write only the integration. |

Put each subdomain in the table of `docs/domain/README.md`. This table is the core domain chart
of the project.

### Bounded contexts

A bounded context is the boundary in which one model and one language apply. The same thing in
the real world can have a different model in each context. Example: a drone is a vehicle with a
maintenance history in the maintenance context, and an available resource with a location in the
scheduling context.

One bounded context has one canvas in `docs/domain/context-<name>/README.md`. The canvas gives
the purpose, the language, the business rules, the messages, and the aggregates of the context.

### Ubiquitous language

The ubiquitous language is the set of terms of one bounded context. The business, the documents,
and the code use the same terms. One term has one meaning in one context. Put each term in
`docs/domain/glossary.md`. If two contexts use the same word with two meanings, write two rows.

### Context map

The context map shows the relationships between the bounded contexts. Each relationship has one
contract. An upstream context sends messages or data to a downstream context. A change in the
upstream context affects the downstream context. A change in the downstream context does not
affect the upstream context.

| Contract | Direction | Use it when | Who adapts |
| --- | --- | --- | --- |
| Partnership | Symmetric | The two contexts succeed or fail together. | Both teams plan together. |
| Shared kernel | Symmetric | The two contexts share a small part of the model as code. | Both teams agree before a change to the shared code. |
| Customer-supplier | Upstream to downstream | The downstream context can ask the upstream context for changes. | The upstream team plans the requests of the downstream team. |
| Conformist | Upstream to downstream | The downstream context uses the upstream model as it is. | The downstream team. |
| Anticorruption layer | Upstream to downstream | The downstream context translates the upstream model to protect its own model. | The downstream team writes the translation. |
| Open host service | Upstream to downstream | The upstream context gives one protocol to many downstream contexts. | The upstream team keeps the protocol stable. |
| Published language | Upstream to downstream | The protocol has a documented, shared format. | The upstream team documents the format. |
| Separate ways | None | The cost of the integration is higher than its value. | Nobody. The contexts do not communicate. |

Only an upstream context can give an open host service or a published language. A downstream
context is a conformist or has an anticorruption layer. It is not both. Put each relationship in
`docs/domain/context-map.md`.

## Tactical design

The tactical design models one bounded context. Use these patterns.

**Aggregate.** An aggregate is a group of one or more entities and value objects with one root
entity. The aggregate is the boundary of consistency: one command changes one aggregate in one
transaction. The root enforces the invariants. Follow the four rules of Vernon:

1. Model true invariants in the consistency boundary. Put in the aggregate only the data that
   one business rule must keep consistent at the same time.
2. Design small aggregates. Most aggregates are one root entity with value objects.
3. Reference other aggregates by identity only. Keep the identifier, not the object.
4. Use eventual consistency outside the boundary. When one command must change two aggregates,
   the first aggregate emits a domain event, and a policy sends a command to the second.

**Entity.** An entity is an object with an identity that stays the same over time. The
attributes can change. The entity holds the rules that apply to its state.

**Value object.** A value object has no identity. Two value objects with the same attributes
are the same. A value object does not change; a change makes a new value object. Use a value
object by default. Make an entity only when you must track the identity.

**Domain event.** A domain event is a fact that happened in the business. Write it in the past
tense. Example: "Delivery cancelled". An aggregate emits the event after a change of state. Other
aggregates and other contexts react to the event.

**Command.** A command is a request to change the state. One aggregate or one domain service
handles one command. A command can fail. An event cannot fail.

**Policy.** A policy is a rule of the form "when this event, then this command". A policy
connects two aggregates or two contexts.

**Domain service.** A domain service holds a business rule that spans more than one aggregate
and belongs to none. It has no state.

**Application service.** An application service runs one use case. It loads the aggregate,
calls the domain logic, saves the aggregate, and publishes the events. It holds no business rule.

**Repository.** A repository loads and saves one type of aggregate by the identity of its root.
One repository exists for each aggregate.

Write one canvas for each aggregate in `docs/domain/context-<name>/agg-<name>.md`.

## Where a context lives

The repository architecture defines the components. The domain model maps to it with one rule.

- One bounded context is implemented by one directory in `services/`.
- An application in `apps/` is a user interface over one or more contexts. It holds no domain
  rule.
- A library in `libs/` holds only a shared kernel or a published language.
- A context does not read the data store of another context. It uses the messages of the
  context map.

Give the component in the `**Component:**` line of the bounded context canvas.

## Select the implementation pattern

Select one implementation pattern for each aggregate. The type of the subdomain and the
complexity of the rules give the pattern.

| Subdomain type | Business logic | Pattern |
| --- | --- | --- |
| Generic | Adopt an existing product. | Transaction script for the integration. |
| Supporting | Simple rules. | Active record, or transaction script if there is no rule. |
| Core | Complex rules and invariants. | Domain model. |
| Core | Complex rules, and the history of each change has business value. | Event-sourced domain model. |

Record the selection in a decision. Give the pattern in the `**Pattern:**` line of the aggregate
canvas.

## The domain model

    docs/domain/
        README.md                  The domain index and the core domain chart.
        context-map.md             The bounded contexts and their relationships.
        glossary.md                The ubiquitous language of each context.
        context-<name>/
            README.md              The bounded context canvas.
            agg-<name>.md          One aggregate canvas.

| Domain artifact | Content | Template |
| --- | --- | --- |
| Domain index | The purpose of the domain and the table of subdomains. | `templates/domain/README.md` |
| Context map | The contexts, their components, and their relationships. | `templates/domain/context-map.md` |
| Glossary | One row for each term of each context. | `templates/domain/glossary.md` |
| Bounded context canvas | The purpose, the language, the rules, the messages, and the aggregates of one context. | `templates/domain/context-name/README.md` |
| Aggregate canvas | The invariants, the commands, the events, and the pattern of one aggregate. | `templates/domain/context-name/agg-name.md` |

Use lowercase letters, digits, and hyphens in `<name>`. Leave a table row empty when a value is
not known. Do not record a status in a domain artifact.

## Procedure: add a bounded context

1. Copy `templates/domain/context-name/` to `docs/domain/context-<name>/`.
2. Write the purpose, the subdomain, the type, and the ubiquitous language in `README.md`.
3. Add the context to the tables of `docs/domain/README.md` and `docs/domain/context-map.md`.
4. Add the terms of the context to `docs/domain/glossary.md`.
5. Make the directory `services/<name>/` for the component of the context.

If the project uses the artifact-driven documentation model, read `artifact-driven.md` in this
directory. It maps each DDD step to one of the five phases.
