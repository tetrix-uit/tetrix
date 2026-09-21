# task-line-clear: Remove full rows and drop rows above

**Plan:** [Implementation plan](README.md)
**Member:** SV2
**Covers:** req-line-clear, spec-line-clear
**Context:** context-tetrix-gameplay
**Component:** apps/tetrix
**Aggregate:** agg-board
**Depends on:** task-falling
**can-parallel:** no — same file; runs inside the lock step of the loop.

## Goal

The game removes each full row after a lock and moves each row above down.

## Steps

1. Implement `removeLine()` to return `int` per spec-line-clear: scan rows
   H-2 to 1, remove each row with no empty inner cell, move rows above
   down, restore side walls. This completes the lock-step stub hook left
   by task-falling; no other task touches this call.
2. Call `removeLine()` after each lock and before the next spawn.
3. Pass the returned count to the speedup step.

## Check

Rebuild with `g++ -std=c++17 -o tetrix main.cpp` in `apps/tetrix`.
Fill one row and lock a block. The full row disappears and rows above drop.

## Acceptance criteria

- Only rows with no empty inner cell are removed.
- Rows above move down by the count of removed rows; freed top rows are empty with side walls.
- Border cells keep `#` after the move.
- `Full row cleared` fires with `{ clearedRows }` when the count is above 0.
- A count of 0 changes nothing in the well.
