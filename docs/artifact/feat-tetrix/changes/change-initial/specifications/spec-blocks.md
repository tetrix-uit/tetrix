# spec-blocks: Falling block shapes and spawn

**Master:** [Specifications](README.md)
**Covers:** req-blocks
**Context:** context-tetrix-gameplay
**Aggregate:** agg-falling-piece

## Description

This specification defines the seven Falling block shapes and the spawn rule.
The player sees the full shape when a new block enters the well.

## Contract

```cpp
char blocks[7][4][4]; // Index 0=I, 1=O, 2=T, 3=S, 4=Z, 5=J, 6=L.
                      // ' ' = empty cell, letter = filled cell.
int x, y, b;          // x, y = left-top corner of the 4x4 shape in the well.
                      // b = shape index 0..6.

void spawnBlock();    // Sets x=5, y=0, b=rand()%7. Legacy form; prefer below.
bool spawnBlockOk();  // Sets x=5, y=0, b=rand()%7. Returns true if each filled
                      // cell of the new shape at (5, 0) is free per canPlace().
                      // Returns false on spawn collision (game over).
```

Data model:

- Each shape fills a 4 by 4 grid.
- I: one full row of `I` in the grid.
- O: a 2 by 2 square of `O`.
- T: one `T` above three `T` in a row.
- S: two `S` above two `S`, shifted left by one column.
- Z: two `Z` above two `Z`, shifted right by one column.
- J: one `J` above three `J` in a row, stem at the left.
- L: one `L` above three `L` in a row, stem at the right.

Spawn rule:

- The game calls `spawnBlockOk()` at start and after each lock.
- The new shape appears at x=5, y=0.
- If `spawnBlockOk()` returns false, the loop of spec-game-loop draws the
  last well state and ends the game with `Game over`.

## Errors

- If the spawn cells are not free, `spawnBlockOk()` returns false and the
  game ends per spec-board. The well keeps the last locked state.
