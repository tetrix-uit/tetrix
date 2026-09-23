# spec-render: Well drawing

**Master:** [Specifications](README.md)
**Covers:** req-square-ui
**Context:** context-tetrix-gameplay

## Description

This specification defines the `Renderer` class. The class draws the Game
well. It writes each well cell as two text columns, so the border and the
blocks look square. The class keeps no game state and no domain logic.

The file apps/tetrix/render.h declares the class. The file
apps/tetrix/render.cpp defines the class. The header includes no stream
header. The source file includes `<iostream>`. apps/tetrix/main.cpp keeps
its own `#include <iostream>` for the domain events.

## Contract

```cpp
// render.h
class Renderer {
public:
  static void draw(const char board[20][15]); // The well per spec-board.
};
```

Call site in apps/tetrix/main.cpp:

```cpp
Renderer::draw(board);
```

The method writes these items to `std::cout`, in this order:

1. The screen clear and home sequence `"\033[2J\033[H"`.
2. Each well row from row 0 to row 19.
3. Two copies of each cell character in the row.

```cpp
// For each cell (i, j) of the row:
std::cout << board[i][j] << board[i][j];
```

The method writes one line end with `std::endl` after each row. The last row
also gets a line end, as in version 1.0.0.

## Data model

- The well is the `char board[H][W]` global of spec-board, with 20 rows and
  15 columns.
- One well cell maps to two text columns.
- A wall cell `#` draws as `##`.
- A block cell with a letter draws as that letter twice, for example `TT`.
- An empty cell ` ` draws as two spaces.
- The full screen line has `2 * W` text columns.
- The method reads the well only. It does not change a cell.
- The header states the parameter as `const char board[20][15]`. It does not
  use `H` and `W`: apps/tetrix/main.cpp includes render.h before the
  `#define H 20` and `#define W 15` lines, so `const char board[H][W]` does
  not compile there.
- The literals 20 and 15 are copies of the well dimensions in spec-board.
  This change does not replace spec-board. A change to a dimension must
  change spec-board, render.h, and render.cpp.
- The parameter `const char board[20][15]` decays to `const char (*)[15]`.
  The type does not carry the row count 20. render.cpp supplies the row
  count 20 as a local constant or a literal.

## Test build

- No test calls `Renderer::draw`. The test build compiles
  apps/tetrix/tests/test_rotate.cpp only and does not link render.cpp.
- A test that calls `Renderer::draw` must add render.cpp to the test build
  command.

## Events

- None. The class is technical infrastructure and emits no domain event.

## Errors

- If the console is too narrow for `2 * W` columns, the display wraps. The
  game still runs; the well model does not change.
- The method has no failure return. It does not handle a failed `std::cout`
  write, as in version 1.0.0.
