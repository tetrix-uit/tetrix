# Specifications: Tetrix falling-block game

**Change:** [change-split-modules](../../../changes/change-split-modules/README.md)

## Solution

The game lives in apps/tetrix as one console program. It keeps the Game well
in a 20 by 15 grid and the Falling block in a 4 by 4 shape. The game loop
moves the block down on a timer and locks it when it lands. The well clears
each full row, drops the rows above, draws square cells, rotates on demand,
and falls faster after each cleared line. The console uses portable calls
only: ANSI escape codes, POSIX termios input, and ISO C++ chrono timing.
Rotation checks the turned grid, and a blocked spawn ends the game.

This change splits two leaf parts of apps/tetrix/main.cpp into two classes
in their own files. The class `Input` in apps/tetrix/input.h and
apps/tetrix/input.cpp wraps the non-blocking termios key read. The class
`Renderer` in apps/tetrix/render.h and apps/tetrix/render.cpp wraps the well
drawing that writes each well cell as two text columns. The game loop calls
`Input::pollKey(c)` and `Renderer::draw(board)`. The two classes are
technical infrastructure with no domain logic. The behavior of the game does
not change.

## Teardown specifications

| ID | Specification | Covers |
| --- | --- | --- |
| [spec-board](spec-board.md) | The well grid, the walls, and the cell states. | req-screen |
| [spec-blocks](spec-blocks.md) | The seven shapes and the spawn rule. | req-blocks |
| [spec-game-loop](spec-game-loop.md) | The fall timer, the collision check, the lock step, and the controls. | req-falling |
| [spec-line-clear](spec-line-clear.md) | The full-row detection, the removal, and the drop of rows above. | req-line-clear |
| [spec-square-ui](spec-square-ui.md) | The square border and the square block cells. | req-square-ui |
| [spec-rotate](spec-rotate.md) | The 90-degree rotation with the wall and collision guard. | req-rotate |
| [spec-speedup](spec-speedup.md) | The delay reduction per cleared line with a floor. | req-speedup |
| [spec-input](spec-input.md) | The non-blocking key read class. | req-falling |
| [spec-render](spec-render.md) | The well drawing class. | req-square-ui |

## Decisions

- [adr-aggregate-pattern](../decisions/adr-aggregate-pattern.md)
- [adr-portable-console](../decisions/adr-portable-console.md)
- [adr-module-layout](../decisions/adr-module-layout.md)
- [adr-draw-well-parameter](../decisions/adr-draw-well-parameter.md)
