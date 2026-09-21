# task-screen: Draw the bordered game well

**Plan:** [Implementation plan](README.md)
**Member:** SV1
**Covers:** req-screen, spec-board
**Context:** context-tetrix-gameplay
**Component:** apps/tetrix
**Aggregate:** agg-board
**Depends on:** -
**can-parallel:** no — first task in the single-file component; sets the grid that later tasks use.

## Goal

The game holds a 20 by 15 well with walls and draws it.

## Steps

1. Keep `H 20`, `W 15`, and `board[H][W]` per spec-board.
2. Implement `initBoard()` to set `#` on the border and ` ` inside.
3. Call `initBoard()` once at program start.

## Check

Build with `g++ -std=c++17 -o tetrix main.cpp` in `apps/tetrix`
(portable headers: `<iostream>`, `<cstdlib>`, `<ctime>`, `<chrono>`,
`<thread>`, `<termios.h>`, `<unistd.h>`; no `conio.h`).
Start it. The well shows with intact walls.

## Acceptance criteria

- Each border cell holds `#` at all times.
- Each inner cell holds only ` ` or one block letter.
- No block cell leaves the inner area.
