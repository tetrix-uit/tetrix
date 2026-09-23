# spec-speedup: Higher falling speed after each cleared line

**Master:** [Specifications](README.md)
**Covers:** req-speedup
**Context:** context-tetrix-gameplay
**Aggregate:** agg-board

## Description

This specification defines the speedup rule. The game shortens the fall
timer after each cleared line. This closes the open question of phase 1.

## Contract

```cpp
int delayMs;        // Fall delay in milliseconds. Base value 500.
int clearedTotal;   // Total count of cleared lines in this game.

void applySpeedup(int clearedRows); // clearedTotal += clearedRows;
                                    // delayMs = max(100, 500 - 50 * clearedTotal).
```

Data model:

- Base delay is 500 ms before any cleared line.
- Each cleared line cuts 50 ms from the delay.
- The floor is 100 ms. More cleared lines do not cut below 100 ms.
- Example: 1 line -> 450 ms; 2 lines -> 400 ms; 8 lines -> 100 ms; 9 lines
  -> 100 ms.

Events:

- `Falling speed increased` with payload `{ clearedTotal, delayMs }`.

## Errors

- If `clearedRows` is 0, the delay does not change.
