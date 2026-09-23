# task-input: Move the non-blocking key read into the Input class

Plan: Implementation plan
Member: SV2
Covers: req-input, spec-input
Context: context-tetrix-gameplay
Component: apps/tetrix
Aggregate: agg-input
Depends on: task-split-modules
can-parallel: yes

---

## Goal

Encapsulate the non-blocking keyboard input reading logic into a dedicated `Input` class to decouple input handling from the main game loop.

---

## Steps

1. Define the `Input` class with a method to perform non-blocking key reads (refactoring `pollKey`).
2. Integrate the `Input` class into the game loop in `apps/tetrix/main.cpp`.
3. Ensure terminal settings (termios) are properly configured and restored during input polling.

---

## Check

Rebuild with `g++ -std=c++17 -o tetrix main.cpp` in `apps/tetrix`. Run the game and verify that key presses (e.g., movement, rotation, quit) respond smoothly without blocking execution.

---

## Acceptance criteria

- Non-blocking key reading is fully handled inside the `Input` class.
- The main loop queries input via the `Input` instance instead of direct global functions.
- Terminal settings are safely restored upon exit.
