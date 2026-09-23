# task-line-clear: Remove full rows and drop rows above

**Plan:** [Implementation plan](implementation-plan.md)  
**Member:** SV2  
**Covers:** req-line-clear, spec-line-clear  
**Context:** context-tetrix-gameplay  
**Component:** apps/tetrix  
**Aggregate:** agg-board  
**Depends on:** task-falling  
**can-parallel:** no — same file; runs inside the lock step of the loop.

---

## Goal

The game removes each full row from the Game well after a falling block locks and moves stacked blocks above down.

---

## Steps

1. Implement `removeLine()` to return `int` per spec-line-clear: scan rows H-2 to 1 in the Game well, remove each full row with no empty inner cell, move stacked blocks above down, and restore side walls. This completes the lock-step stub hook left by task-falling; no other task touches this call.
2. Call `removeLine()` after each falling block locks and before the next spawn.
3. Pass the cleared line count to adjust the falling speed.

---

## Check

Rebuild with `g++ -std=c++17 -o tetrix main.cpp` in `apps/tetrix`. Fill one full row in the Game well and lock a falling block. The full row disappears and stacked blocks above drop down.

---

## Acceptance criteria

- Only full rows with no empty inner cell are removed.
- Stacked blocks above move down by the count of cleared lines; freed top rows are empty with side walls in the Game well.
- Border cells keep `#` after the move.
- `Full row cleared` fires with `{ clearedRows }` when the count is above 0.
- A count of 0 changes nothing in the Game well.
