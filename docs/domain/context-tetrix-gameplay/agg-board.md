# agg-board: Game well and stacked blocks

**Context:** context-tetrix-gameplay
**Pattern:** Domain model

## Description

This aggregate owns the Game well and the Stacked blocks. It enforces the
border rule and the full-row rule. It owns the fall delay and the cleared
line count. It is small: one grid plus two counters.

## State transitions

| From | Command | To |
| --- | --- | --- |
| Empty well | Lock falling block | Well with new stacked cells |
| Well with full row | Clear full rows | Well with rows removed and rows above dropped |
| Delay D | Increase falling speed | Delay max(100, D - 50 * clearedRows) |

## Enforced invariants

- Each border cell holds `#` at the end of each transaction.
- Each inner cell holds only ` ` or one block letter.
- A full row clears only after a lock, never mid-fall.
- The delay never drops below 100 ms.

## Corrective policies

| Event | Policy |
| --- | --- |
| Falling block landed | Clear full rows on this aggregate. |
| Full row cleared | Increase falling speed on this aggregate. |

## Handled commands

| Command | Result | Emits |
| --- | --- | --- |
| Lock falling block | Writes the shape cells as stacked cells. | Falling block landed |
| Clear full rows | Removes each full row; drops rows above. | Full row cleared |
| Increase falling speed | Cuts the delay per spec-speedup. | Falling speed increased |

## Created events

| Event | Payload |
| --- | --- |
| Falling block landed | `{ shape, x, y }` |
| Full row cleared | `{ clearedRows }` |
| Falling speed increased | `{ clearedTotal, delayMs }` |

## References by identity

| Aggregate | Context |
| --- | --- |
| agg-falling-piece | context-tetrix-gameplay |

## Notes

- Size: 20 by 15 cells plus two counters. Fits one transaction per command.
- On `Game over` from agg-falling-piece, this aggregate keeps the last
  locked well state; no further command runs.
