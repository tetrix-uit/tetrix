# context-tetrix-gameplay: Tetrix gameplay

**Subdomain:** Tetrix gameplay
**Type:** Core

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

## Assumptions

- The game lives in apps/tetrix per the user decision, not in services/<name> as the template
  default says. Phase 2 records apps/tetrix as the component.
- The lecturer main.cpp baseline is the reference for the block shapes and the game well.
- One player plays at a time.

## Open questions

- How much does the falling speed rise after each cleared line?
