# spec-line-clear: Full-row detection, removal, and drop

**Master:** [Specifications](README.md)
**Covers:** req-line-clear
**Context:** context-tetrix-gameplay
**Aggregate:** agg-board

## Description

This specification defines line clearing. After each lock, the game removes
each full row and moves each row above down.

## Contract

```cpp
int removeLine(); // Scans rows 1..H-2 after each lock.
                  // Removes each row with no empty inner cell.
                  // Moves each row above down by the count of removed rows.
                  // Restores the side walls of moved rows.
                  // Returns the count of removed rows (0 or more).
```

Data model:

- A row is full when each inner column (1 to W-2) holds a block letter.
- The scan runs from the bottom row (H-2) to the top row (1).
- After removal, each row above moves down by the count of cleared rows.
- The top freed rows become empty with side walls.

Invariants:

- The border cells keep `#` after the move.
- The count of stacked cells drops by `clearedRows * (W-2)` minus the cells
  of the rows that moved down.

Events:

- `Full row cleared` with payload `{ clearedRows }` when the count is above 0.

## Errors

- If no row is full, the well does not change and the count is 0.
