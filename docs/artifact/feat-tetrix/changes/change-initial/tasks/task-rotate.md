# task-rotate: Rotate the falling block on demand

**Plan:** [Implementation plan](README.md)
**Member:** SV4
**Covers:** req-rotate, spec-rotate
**Context:** context-tetrix-gameplay
**Component:** apps/tetrix
**Aggregate:** agg-falling-piece
**Depends on:** task-falling
**can-parallel:** no — same file; extends the key handling of the loop.

## Goal

The player turns the falling block 90 degrees clockwise with key `w` when free space allows it.

## Steps

1. Implement `tryRotate()` per spec-rotate: build the turned grid with cell
   `(i, j)` from old `(3-j, i)`, check it with `canPlace(turned, x, y)`,
   keep it only if the check passes. This completes the `w` stub hook left
   by task-falling; no other task touches this wiring.
2. Wire key `w` in the loop to `tryRotate()`.

## Check

Rebuild with `g++ -std=c++17 -o tetrix main.cpp` in `apps/tetrix`.
Play and press `w` in open space and against a wall. The block turns in open
space and stays unchanged at the wall.

## Acceptance criteria

- The O shape keeps its square form after the turn.
- A blocked turn (wall or stacked cell) keeps the old shape and place.
- `Falling block rotated` fires with `{ shape, x, y }` on success.
- `canMove()` is not used as the rotation guard.
