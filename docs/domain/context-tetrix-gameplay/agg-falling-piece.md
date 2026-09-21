# agg-falling-piece: Falling block shape and place

**Context:** context-tetrix-gameplay
**Pattern:** Domain model

## Description

This aggregate owns the Falling block: its shape, its place, its move, and
its turn. It checks each move and turn against the walls and the stacked
cells by identity reference to agg-board. It is small: one 4 by 4 shape plus
x, y, b.

## State transitions

| From | Command | To |
| --- | --- | --- |
| Spawn place | Move left, right, down | New place if free, else same place |
| Shape S | Rotate shape | Turned shape if free, else same shape |
| Falling | Lock falling block | Locked; next spawn starts |

## Enforced invariants

- The shape is one of the seven 4 by 4 shapes.
- Each filled cell stays inside the walls after a move or turn.
- No filled cell overlaps a stacked cell after a move or turn.
- One command changes only this aggregate; the well changes via events.

## Corrective policies

| Event | Policy |
| --- | --- |
| Falling block landed | Spawn next falling block on this aggregate. |

## Handled commands

| Command | Result | Emits |
| --- | --- | --- |
| Move left, right, down | Changes x, y if the target cells are free. | - |
| Rotate shape | Checks the turned grid with canPlace(); turns 90 degrees clockwise if free. | Falling block rotated |
| Spawn next falling block | Sets x=5, y=0, b=rand()%7. Returns false on spawn collision. | Game over on false |

## Created events

| Event | Payload |
| --- | --- |
| Falling block rotated | `{ shape, x, y }` |
| Game over | `{ reason: spawn-blocked }` |

## References by identity

| Aggregate | Context |
| --- | --- |
| agg-board | context-tetrix-gameplay |

## Notes

- The O shape keeps its square form under rotation.
- The `w` key demands rotation; `a`, `d`, `x` demand moves; `q` quits.
