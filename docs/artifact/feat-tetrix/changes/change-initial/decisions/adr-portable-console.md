# adr-portable-console: Portable console, input, and timing API

**Relates to:** spec-game-loop, spec-square-ui
**Context:** context-tetrix-gameplay

## Context

The baseline uses Windows-only calls: `conio.h` with `kbhit()`/`getch()`,
`_sleep()`, and `system("cls")`. The build must run on a portable
Linux/ISO C++ toolchain. The game needs non-blocking key input, a timed
wait, and a screen clear without these calls.

## Options

1. ANSI escape codes plus POSIX termios plus ISO C++ chrono. Pro: no new
   dependency; small change to the baseline; works on Linux terminals. Con:
   the team owns a small termios setup and restore step.
2. ncurses library. Pro: full screen and key API in one library. Con: new
   third-party dependency; larger rewrite of `draw()` and the input loop.

## Decision

Option 1. The game uses ANSI escape codes for the screen clear and the
square cells, POSIX termios for non-blocking key reads, and
`std::this_thread::sleep_for` with `std::chrono::milliseconds` for the
fall delay.

## Consequences

- The code builds with ISO C++ plus POSIX termios and no new library.
- Phase 3 tasks cover the termios setup and restore as part of the loop.
- The Windows-only calls leave the codebase.
