# task-input: Move the non-blocking key read into the Input class

**Plan:** [Implementation plan](README.md)
**Covers:** req-falling, spec-input
**Context:** context-tetrix-gameplay
**Component:** apps/tetrix
**Depends on:** -
**can-parallel:** no — same file as task-render; the two tasks run in sequence.

## Goal

The class `Input` in apps/tetrix/input.h and apps/tetrix/input.cpp holds the
non-blocking termios key read, and the game loop calls `Input::pollKey(c)`.

## Steps

1. Create apps/tetrix/input.h. Declare `class Input` with the public static
   method `static bool pollKey(char& c);` per spec-input. Include no POSIX
   header in the header, so the test build can include main.cpp.
2. Create apps/tetrix/input.cpp. Include `#include "input.h"` with quotes,
   then `<termios.h>` and `<unistd.h>`. Define `Input::pollKey` with the six
   operations of spec-input: save the terminal settings, disable `ICANON` and
   `ECHO`, set `VMIN` to 0 and `VTIME` to 0, read one byte, restore the
   settings, and return the result.
3. In apps/tetrix/main.cpp, remove the free function `pollKey()`.
4. In apps/tetrix/main.cpp, add `#include "input.h"` with quotes per
   adr-module-layout and C-P2-08.
5. In apps/tetrix/main.cpp, change the call site to `Input::pollKey(c)`.
6. Keep the `#ifndef TETRIX_TEST` guard around `main()` in apps/tetrix/main.cpp
   per C-P2-02. The split removes the POSIX exclusion from main.cpp only.

## Check

Run these commands from `apps/tetrix`:

```sh
g++ -std=c++17 -Wall -Wextra -pedantic -o tetrix main.cpp input.cpp
g++ -std=c++17 -Wall -Wextra -pedantic -o test_rotate tests/test_rotate.cpp
./test_rotate
```

The command `g++ -std=c++17 -o tetrix main.cpp` no longer links. render.cpp
does not exist yet, so the full production build command of C-P2-01 runs in
task-render:

```sh
g++ -std=c++17 -Wall -Wextra -pedantic -o tetrix main.cpp input.cpp render.cpp
```

Manual step: run `./tetrix` in a terminal. Press `q` to quit. Do not run the
game as an unattended command; `main()` loops until the quit key. The keys
`a`, `d`, `x`, `w`, and `q` act as in version 1.0.0.

## Feasibility constraints

Reviews `R-SPLIT-P2-01` and `R-SPLIT-P3-01`. The decisions and spec-input
record the resolutions.

| Constraint | Required action |
| --- | --- |
| C-P2-01 | The full production build compiles main.cpp, input.cpp, and render.cpp. It runs in task-render. |
| C-P2-02 | main.cpp keeps the `#ifndef TETRIX_TEST` guard around `main()`. |
| C-P2-08 | main.cpp includes `input.h` with quotes. |
| C-P3-01 | The production run is a manual step with the quit key `q`. The check gives no unattended `./tetrix` command. |
| C-P3-02 | input.cpp includes `#include "input.h"` with quotes. |

## Acceptance criteria

- The class `Input` is in apps/tetrix/input.h and apps/tetrix/input.cpp.
- `Input::pollKey` keeps no state and does not block.
- input.h includes no POSIX header.
- input.cpp includes its own header `input.h` with quotes.
- main.cpp keeps the `#ifndef TETRIX_TEST` guard around `main()`.
- main.cpp includes input.h with quotes and calls `Input::pollKey(c)`.
- The test build compiles and passes.
