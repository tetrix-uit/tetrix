# task-speedup: Increase falling speed after each cleared line

**Plan:** [Implementation plan](README.md)
**Member:** SV5
**Covers:** req-speedup, spec-speedup
**Context:** context-tetrix-gameplay
**Component:** apps/tetrix
**Aggregate:** agg-board
**Depends on:** task-line-clear
**can-parallel:** no — same file; consumes the cleared-row count of the line-clear step.

## Goal

The game shortens the fall delay after each cleared line with a floor of 100 ms.

## Steps

1. Add `delayMs` (base 500) and `clearedTotal` per spec-speedup.
2. Implement `applySpeedup(clearedRows)` with `delayMs = max(100, 500 - 50 * clearedTotal)`.
3. Call `applySpeedup()` with the `removeLine()` count after each lock; the loop waits `delayMs`.

## Check

Rebuild with `g++ -std=c++17 -o tetrix main.cpp` in `apps/tetrix`.
Clear lines and observe faster falling: 1 line gives 450 ms, 8 lines give 100 ms,
more lines stay at 100 ms.

## Acceptance criteria

- A count of 0 changes no delay.
- `Falling speed increased` fires with `{ clearedTotal, delayMs }`.
- The delay never drops below 100 ms.
