# req-falling: Fall on a timer and move on player demand

**Master:** [Requirements](README.md)
**Priority:** Must
**Context:** context-tetrix-gameplay

## Statement

The game must move the falling block down on a timer, let the player move it left, right, and
down, and let the player quit the game on demand.

## Acceptance criteria

- Given the falling block in the well, when the timer fires, then the block moves down by one row.
- Given the falling block in the well, when the player moves left, right, or down, then the block
  moves in that direction if space allows.
- Given a running game, when the player quits, then the game ends.

## Notes

The timer period follows the lecturer baseline until req-speedup changes it. Phase 4 owner: SV1.
