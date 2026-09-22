# spec-rotate: Rotation of the falling block

**Master:** [Specifications](README.md)
**Covers:** req-rotate
**Context:** context-tetrix-gameplay
**Aggregate:** agg-falling-piece

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

`tryRotate()` calls `blocks[b]->rotatedShape(turned)` through the base pointer
defined in [spec-blocks](spec-blocks.md). The selected derived object supplies the candidate.
The candidate is a separate mutable `char[4][4]` grid for `canPlace()`.

## Rotation rules

- `RotatingBlocks::rotatedShape()` takes the old cell at `(3-j, i)` for each turned cell at `(i, j)`.
- `SquareBlocks::rotatedShape()` copies the centered O grid without a change.
- Neither method changes the active grid or the initial grid.
- Each candidate has four filled cells. Four clockwise turns restore the starting grid.
- The game reads the `w` key as the rotate demand in the loop of
  spec-game-loop.

## Collision guard

- The caller removes the active block from the board before the turn. The game loop already calls `boardDelBlock()` before key handling.
- The turn applies only if `canPlace()` on the turned grid at (x, y)
  returns true. `canMove()` tests only the current shape and cannot guard
  rotation (C-02).
- Else the shape and the place do not change.
- The filled cells must satisfy `1 <= x+j < W-1` and `1 <= y+i < H-1`.
- Each target board cell must be empty. The turn does not shift `x` or `y` to avoid an obstacle.
- A turn at spawn can fail if a filled cell reaches row zero.
- The function does not change the board on success or failure.

## Events

- `Falling block rotated` with payload `{ shape, x, y }` on success.
- The function copies the candidate to `blocks[b]->shape` before it emits the event once.
- `shape` is the letter I, O, T, S, Z, J, or L selected by `b`.
- For T at `(5, 3)`, the exact output is `Falling block rotated { shape: T, x: 5, y: 3 }` plus one newline.
- A valid O turn returns true and emits the event once, although its grid stays identical.
- A rejected turn returns false and emits no event.

## Test contract

The separate file `apps/tetrix/tests/test_rotate.cpp` tests the production classes and functions.
The test build excludes POSIX headers, `pollKey()`, and the interactive `main()`.
The tests do not contain a replacement rotation implementation.

- A call through `Blocks*` must reach an observable derived override.
- Checks cover all seven templates, clockwise results, four filled cells, four-turn restoration, and the unchanged O grid.
- Checks cover both side walls, the top border, the floor, and stacked cells.
- Rejection checks compare full shape and board snapshots, `x`, `y`, and event output.
- Spawn checks cover orientation reset before both accepted and rejected collision checks.
- Fixtures select the expected random index without an assumption about a platform-specific seed result.
- Event checks compare the exact output on success and its absence on failure.

## Errors

- If the turned shape hits a wall or a stacked cell, the shape does not turn.
