# task-falling: Run the fall timer, movement, lock, and controls

**Plan:** [Implementation plan](README.md)
**Member:** SV1
**Covers:** req-falling, spec-game-loop
**Context:** context-tetrix-gameplay
**Component:** apps/tetrix
**Aggregate:** agg-falling-piece
**Depends on:** task-screen, task-block-shapes
**can-parallel:** no — same file; the loop binds the well and the shapes together.

## Goal

The game falls on a timer, moves on player demand, locks landed blocks,
and quits on demand with portable calls only.

## Steps

1. Implement `canMove()`, `canPlace()`, `block2Board()`, and
   `boardDelBlock()` per spec-game-loop.
2. Implement `pollKey()` with POSIX termios (non-blocking read) including
   setup and restore of the terminal.
3. Implement the loop order of spec-game-loop: clear shape, read one key
   (`a` left, `d` right, `x` down, `w` rotate, `q` quit), move or rotate
   if allowed, fall or lock, write shape, draw, wait `delayMs` with
   `std::this_thread::sleep_for` and `std::chrono::milliseconds`.
   Leave two stub hooks only: the `w` key calls a `tryRotate()` stub that
   returns false, and the lock step calls a `removeLine()` stub that
   returns 0. Task-rotate completes the `w` wiring and task-line-clear
   completes the lock-step call.
4. Remove all Windows-only calls (`conio.h`, `kbhit()`, `getch()`,
   `_sleep()`, `system("cls")`) per adr-portable-console. Use the portable
   headers `<iostream>`, `<cstdlib>`, `<ctime>`, `<chrono>`, `<thread>`,
   `<termios.h>`, and `<unistd.h>`.
5. On lock: call `block2Board()`, call the `removeLine()` stub (completed
   by task-line-clear), then call `spawnBlockOk()` per spec-blocks. If it
   returns false, draw the last well state and end with `Game over`.
   Note: spec-game-loop step 5 names `spawnBlock()`; the correct call is
   `spawnBlockOk()->bool`. Phase 4 corrects that spec wording in place.

## Check

Build with `g++ -std=c++17 -o tetrix main.cpp` in `apps/tetrix`.
Play the game. The block falls, keys `a`/`d`/`x` move it, `q` quits,
and a full well ends with `Game over`.

## Acceptance criteria

- Unknown keys are ignored.
- A move into a wall or a stacked cell does not occur.
- `Falling block landed` fires after each lock.
- A blocked spawn draws the last well state and ends the game with
  `Game over`.
- The code uses no Windows-only console calls.
