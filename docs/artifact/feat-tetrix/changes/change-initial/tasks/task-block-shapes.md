# task-block-shapes: Define the seven shapes and the spawn rule

**Plan:** [Implementation plan](README.md)
**Member:** SV1
**Covers:** req-blocks, spec-blocks
**Context:** context-tetrix-gameplay
**Component:** apps/tetrix
**Aggregate:** agg-falling-piece
**Depends on:** task-screen
**can-parallel:** no — same file as task-screen; the spawn area refers to the well grid.

## Goal

The game defines the seven canonical 4 by 4 shapes and spawns each new block at x=5, y=0.

## Steps

1. Narrow the `blocks` array to 7 entries in order I, O, T, S, Z, J, L
   per spec-blocks.
2. Implement `spawnBlockOk()` to set x=5, y=0, b=rand()%7 and return true
   only if each filled cell at (5, 0) is free per `canPlace()`.
3. Keep `spawnBlock()` as a wrapper only if existing callers need it;
   new code calls `spawnBlockOk()`.

## Check

Rebuild with `g++ -std=c++17 -o tetrix main.cpp` in `apps/tetrix`.
Start the game several times. Each new block shows one full shape at the top center.

## Acceptance criteria

- The array holds exactly the seven shapes of spec-blocks.
- A new shape appears at x=5, y=0 at start and after each lock.
- If the spawn cells are blocked, `spawnBlockOk()` returns false and the
  game ends with `Game over`, keeping the last locked well state.
