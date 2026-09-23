# spec-board: Game well grid and walls

**Master:** [Specifications](README.md)
**Covers:** req-screen
**Context:** context-tetrix-gameplay
**Aggregate:** agg-board

## Description

This specification defines the Game well. The well holds the falling and
stacked blocks inside a border. It keeps each block inside the border.

## Contract

```cpp
#define H 20
#define W 15
char board[H][W]; // ' ' = empty, '#' = wall, letter = stacked block

void initBoard(); // Sets walls on row 0, row H-1, column 0, column W-1.
                  // Sets ' ' in all inner cells.
```

Data model:

- The well has 20 rows and 15 columns.
- The border cells hold `#`.
- The inner cells hold ` ` or one block letter (`I`, `O`, `T`, `S`, `Z`, `J`, `L`).
- The spawn area is row 0 to row 3, column 5 to column 8.

Invariants:

- Each border cell always holds `#`.
- Each inner cell holds only ` ` or one block letter.
- No block cell leaves the inner area.

## Errors

- If a spawn cell holds a stacked block at spawn time, `spawnBlockOk()` per
  spec-blocks returns false. The game draws the last well state and ends
  with `Game over` per spec-game-loop step 5.
