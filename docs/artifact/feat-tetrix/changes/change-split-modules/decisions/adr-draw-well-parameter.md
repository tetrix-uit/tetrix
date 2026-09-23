# adr-draw-well-parameter: The renderer receives the well as a parameter

**Relates to:** spec-render
**Context:** context-tetrix-gameplay

## Context

In version 1.0.0, the function draw() reads the global `char board[H][W]`.
After the split, the class `Renderer` lives in its own translation unit. It
must reach the well. The well stays in apps/tetrix/main.cpp as the global of
spec-board. The change README already fixes the call
`Renderer::draw(board)`. The test build includes main.cpp but never calls the
renderer.

## Options

1. The renderer receives the well as a parameter: draw takes
   `const char board[20][15]`, and the loop calls `Renderer::draw(board)`.
   Pro: the renderer depends on its argument only; a test can pass a fixture
   well; the interface names the data that the method reads. Con: the
   signature names the well size; the caller passes the global.
2. The renderer reads the global board. Pro: no method parameter. Con: the
   renderer depends on a global in another translation unit; a test cannot
   supply a fixture well; the dependency stays implicit.

## Decision

Option 1. The renderer receives the well as a const parameter. The interface
then states the data that the method reads, and a test can call the method
with a fixture well. The phase 1 artifact already fixes the call
`Renderer::draw(board)`.

## Consequences

- render.h states the well parameter as `const char board[20][15]`. The
  literals 20 and 15 are copies of the dimensions in spec-board. A change to
  a dimension must change spec-board, render.h, and render.cpp.
- The parameter `const char board[20][15]` decays to `const char (*)[15]`.
  The type does not carry the row count 20, so render.cpp supplies the row
  count 20 as a local constant or a literal.
- The renderer cannot change the well.
- The test build compiles tests/test_rotate.cpp only and does not link
  render.cpp. No test calls `Renderer::draw`. A test that calls
  `Renderer::draw` must add render.cpp to the test build command.
- A later change can move the well to another component and pass it in.

## Feasibility constraints

Review `R-SPLIT-P2-01`. This decision and spec-render record the resolutions.

| Constraint | Resolution | Owner |
| --- | --- | --- |
| C-P2-04 | render.h uses `const char board[20][15]`, not `H` and `W`. spec-render states the reason. | solution-expert and tetrix-expert |
| C-P2-05 | render.cpp supplies the row count 20 as a local constant or a literal. spec-render states it. | tetrix-expert |
| C-P2-06 | The 20 and 15 literals are copies of the spec-board dimensions. This change does not replace spec-board. spec-render states the copy rule. | solution-expert |
| C-P2-07 | render.cpp includes `<iostream>`; render.h has no stream header; main.cpp keeps its own `<iostream>`. spec-render states it. | tetrix-expert |
| C-P2-09 | No test calls `Renderer::draw`. A test that calls it must add render.cpp to the test build command. spec-render and this decision state it. | solution-expert |
