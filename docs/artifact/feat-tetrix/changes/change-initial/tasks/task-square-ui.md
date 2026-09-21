# task-square-ui: Draw square border and square blocks

**Plan:** [Implementation plan](README.md)
**Member:** SV3
**Covers:** req-square-ui, spec-square-ui
**Context:** context-tetrix-gameplay
**Component:** apps/tetrix
**Aggregate:** agg-board
**Depends on:** task-falling
**can-parallel:** no — same file; reworks the `draw()` used by the loop.

## Goal

Each well cell draws as two text columns so the border and the blocks look square.

## Steps

1. Rework `draw()` to write `"\033[2J\033[H"` then rows 0..H-1 per spec-square-ui.
2. Draw each cell as two columns: wall as `##`, block as letter plus letter, empty as two spaces.
3. Keep H=20 rows and W=15 columns per spec-board.

## Check

Rebuild with `g++ -std=c++17 -o tetrix main.cpp` in `apps/tetrix`.
Run the game. The border and the blocks look square with no wrapped lines on a wide console.

## Acceptance criteria

- One well cell maps to two text columns; each screen line has `2 * W` columns.
- Walls show as `##`, blocks as doubled letters, empty cells as two spaces.
- The well model (H, W, cell values) does not change.
