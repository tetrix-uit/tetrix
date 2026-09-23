# task-render: Move the well drawing into the Renderer class

**Plan:** [Implementation plan](README.md)
**Covers:** req-square-ui, spec-render
**Context:** context-tetrix-gameplay
**Component:** apps/tetrix
**Depends on:** task-input
**can-parallel:** no — same file as task-input; the two tasks run in sequence.

## Goal

The class `Renderer` in apps/tetrix/render.h and apps/tetrix/render.cpp draws
the well, and the game loop calls `Renderer::draw(board)`.

## Steps

1. Create apps/tetrix/render.h. Declare `class Renderer` with the public
   static method `static void draw(const char board[20][15]);` per spec-render
   and adr-draw-well-parameter. Include no stream header in the header.
2. Create apps/tetrix/render.cpp. Include `<iostream>` per C-P2-07. Define
   `Renderer::draw`. Write `"\033[2J\033[H"`, then each row 0 to 19, then each
   cell twice per spec-render. Write one line end after each row.
3. In apps/tetrix/render.cpp, supply the row count 20 as a local constant or a
   literal per C-P2-05. The parameter `const char board[20][15]` decays to
   `const char (*)[15]` and carries no row count.
4. In apps/tetrix/main.cpp, remove the free function `draw()`.
5. In apps/tetrix/main.cpp, add `#include "render.h"` with quotes per
   adr-module-layout and C-P2-08.
6. In apps/tetrix/main.cpp, change the call sites to `Renderer::draw(board)`.
   Keep `#include <iostream>` in main.cpp for the domain events per C-P2-07.
7. Do not change apps/tetrix/tests/test_rotate.cpp. No test calls
   `Renderer::draw` per C-P2-09.

## Check

Run these commands from `apps/tetrix`:

```sh
g++ -std=c++17 -Wall -Wextra -pedantic -o tetrix main.cpp input.cpp render.cpp
./tetrix
g++ -std=c++17 -Wall -Wextra -pedantic -o test_rotate tests/test_rotate.cpp
./test_rotate
```

The command `g++ -std=c++17 -o tetrix main.cpp` no longer links.

Manual step: play the game. The border and the blocks look square. No line
wraps on a wide console. The game acts as version 1.0.0.

## Feasibility constraints

Review `R-SPLIT-P2-01`. The decisions and spec-render record the resolutions.

| Constraint | Required action |
| --- | --- |
| C-P2-01 | The task check uses `g++ -std=c++17 -Wall -Wextra -pedantic -o tetrix main.cpp input.cpp render.cpp`. |
| C-P2-05 | render.cpp supplies the row count 20 as a local constant or a literal. |
| C-P2-07 | render.cpp includes `<iostream>`; main.cpp keeps its own `<iostream>`. |
| C-P2-08 | main.cpp includes `render.h` with quotes. |
| C-P2-09 | No test calls `Renderer::draw`. The test build command stays `g++ -std=c++17 -Wall -Wextra -pedantic -o test_rotate tests/test_rotate.cpp`. |
| C-P2-10 | apps/tetrix has no README. This task check states the new build command. |

## Acceptance criteria

- The class `Renderer` is in apps/tetrix/render.h and apps/tetrix/render.cpp.
- `Renderer::draw` receives the well as `const char board[20][15]`.
- The method writes the clear sequence and each cell as two text columns.
- render.cpp includes `<iostream>`; render.h includes no stream header;
  main.cpp keeps its own `<iostream>`.
- main.cpp includes render.h with quotes and calls `Renderer::draw(board)`.
- No test calls `Renderer::draw`.
- The test build compiles and passes.
