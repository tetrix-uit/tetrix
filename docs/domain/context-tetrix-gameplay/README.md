# context-tetrix-gameplay: Tetrix gameplay

**Subdomain:** Tetrix gameplay
**Type:** Core
**Component:** apps/tetrix

## Purpose

This context holds the rules of the Tetrix falling-block game. It decides how blocks fall, rotate,
and stack. It decides when full rows clear and how the speed rises.

## Ubiquitous language

| Term | Meaning |
| --- | --- |
| Game well | The bordered area in which blocks fall and stack. |
| Falling block | The block shape that the player moves. |
| Stacked blocks | The blocks that have landed at the bottom of the well. |
| Full row | A row of the well with no empty cell. |
| Cleared line | A full row that the game has removed. |
| Falling speed | The rate at which the falling block moves down. |
| Player | The person who plays the game. |

## Business rules

- The falling block moves down on a timer until it lands on stacked blocks or the bottom.
- The player moves the falling block left, right, and down and rotates it.
- A full row clears when a block lands, and each row above moves down.
- The falling speed rises after each cleared line.

## Inbound messages

| Message | Kind | From |
| --- | --- | --- |
| Move falling block | command | Player |
| Rotate falling block | command | Player |
| Quit game | command | Player |

## Outbound messages

| Message | Kind | To |
| --- | --- | --- |
| Falling block landed | event | Player |
| Full row cleared | event | Player |
| Falling speed increased | event | Player |
| Falling block rotated | event | Player |
| Game quit | event | Player |
| Game over | event | Player |

## Aggregates

- [agg-board](agg-board.md)
- [agg-falling-piece](agg-falling-piece.md)

## Assumptions

- The game lives in apps/tetrix per the user decision, not in services/<name> as the template
  default says. Phase 2 records apps/tetrix as the component.
- The lecturer main.cpp baseline is the reference for the block shapes and the game well.
- One player plays at a time.

## Open questions

- None. spec-speedup sets 50 ms per line with a 100 ms floor.
