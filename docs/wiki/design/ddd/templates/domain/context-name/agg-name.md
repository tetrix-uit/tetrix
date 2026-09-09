# agg-name: <title>

**Context:** context-name
**Pattern:** Transaction script | Active record | Domain model | Event-sourced domain model

## Description

<The responsibility of the aggregate, why these boundaries, and the trade-offs.>

## State transitions

| From | Command | To |
| --- | --- | --- |
| <State> | <Command> | <State> |

## Enforced invariants

- <One rule that is true at the end of each transaction.>

## Corrective policies

| Event | Policy |
| --- | --- |
| <Event> | <The command that repairs the state when a relaxed rule is broken.> |

## Handled commands

| Command | Result | Emits |
| --- | --- | --- |
| <Command> | <The change of state, or the error.> | <Event> |

## Created events

| Event | Payload |
| --- | --- |
| <Event> | <The fields of the event.> |

## References by identity

| Aggregate | Context |
| --- | --- |
| agg-name | context-name |

## Notes

<Throughput, size, sources, open questions.>
