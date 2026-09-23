# task-line-clear: Clear filled rows and shift upper rows down

**Plan:** [Implementation plan](implementation-plan.md)  
**Member:** SV2  
**Covers:** req-line-clear, spec-line-clear  
**Context:** context-tetrix-gameplay  
**Component:** apps/tetrix  
**Aggregate:** agg-board  
**Depends on:** task-falling  
**can-parallel:** no — modifies same file; executed during loop's lock step.

---

## Goal

Automatically detect and clear completed horizontal lines whenever a piece locks into place, then drop all higher rows to fill the gap.

---

## Steps

1. Develop `removeLine()` to output an `int` following `spec-line-clear`: check inner cells across rows H-2 down to 1, eliminate any row lacking empty spaces, shift upper rows downward, and maintain border walls. This fulfills the lock-step hook introduced in `task-falling`; no other tasks modify this function call.
2. Execute `removeLine()` right after a block locks and prior to spawning a new piece.
3. Forward the cleared row count to the speed increment handler.

---

## Check

Compile using `g++ -std=c++17 -o tetrix main.cpp` inside `apps/tetrix`. Complete any horizontal row and trigger a block lock. Verify that the completed line disappears and the blocks above drop down.

---

## Acceptance criteria

- Only rows that have zero empty inner cells get cleared.
- Upper rows shift down corresponding to the number of cleared lines; newly cleared top rows are reset to empty with side walls intact.
- Boundary cells strictly retain `#` after rows shift.
- The log `Full row cleared` triggers with `{ clearedRows }` whenever the count exceeds 0.
- A cleared count of 0 makes no modifications to the playing field.
