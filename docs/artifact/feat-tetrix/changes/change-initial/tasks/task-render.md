# task-render: Move the well drawing into the Renderer class

Plan: Implementation plan
Member: SV2
Covers: req-render, spec-render
Context: context-tetrix-gameplay
Component: apps/tetrix
Aggregate: agg-renderer
Depends on: task-split-modules
can-parallel: yes

---

## Goal

Encapsulate the Game well rendering logic into a dedicated `Renderer` class to separate display code from game state logic.

---

## Steps

1. Create a `Renderer` class to encapsulate the `draw()` functionality for rendering the Game well.
2. Update `apps/tetrix/main.cpp` to utilize the `Renderer` instance for drawing the Game well in the game loop.
3. Ensure border walls and double-column block rendering formats remain intact.

---

## Check

Rebuild with `g++ -std=c++17 -o tetrix main.cpp` in `apps/tetrix`. Run the application and confirm the Game well renders correctly on screen without visual regressions.

---

## Acceptance criteria

- Game well drawing logic is fully contained within the `Renderer` class.
- The game loop invokes rendering via the `Renderer` instance.
- Visual layout of the Game well, including borders and blocks, remains completely unchanged.
