# spec-rotate: Rotation of the falling block

**Master:** [Specifications](README.md)
**Covers:** req-rotate
**Context:** context-tetrix-gameplay
**Aggregate:** agg-falling-piece

## Description

This specification defines rotation. The player turns the Falling block 90
degrees clockwise when free space allows it.

## Contract

```cpp
bool canPlace(char grid[4][4], int px, int py); // Per spec-game-loop: true if
                              // each filled cell of grid at (px, py) stays
                              // inside the walls and avoids stacked cells.
bool tryRotate(); // Builds a 4x4 grid turned 90 degrees clockwise.
                  // Checks the turned grid with canPlace(turned, x, y).
                  // Returns true and keeps the turned grid only if the check
                  // passes. Else returns false and keeps the old grid.
```

Rotation rule:

- The turned cell at `(i, j)` takes the old cell at `(3-j, i)`.
- The O shape keeps its square form after the turn.
- The game reads the `w` key as the rotate demand in the loop of
  spec-game-loop.

Guard:

- The turn applies only if `canPlace()` on the turned grid at (x, y)
  returns true. `canMove()` tests only the current shape and cannot guard
  rotation (C-02).
- Else the shape and the place do not change.

Events:

- `Falling block rotated` with payload `{ shape, x, y }` on success.

## Errors

- If the turned shape hits a wall or a stacked cell, the shape does not turn.
