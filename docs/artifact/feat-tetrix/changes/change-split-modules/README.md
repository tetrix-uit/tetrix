# Change: Split leaf modules into classes

**Feature:** [Tetrix falling-block game](../../README.md)
**From:** 1.0.0
**To:** 1.1.0
**Type:** Specifications

## Reason

The file `apps/tetrix/main.cpp` holds the whole game in free functions over global state. Two
parts of the file are leaf modules with no domain logic. The first part is the non-blocking
termios key read. The second part is the well renderer that writes each cell as two text columns.
The project needs a small, self-contained task that a student can own. The project also needs
separate files, so that later tasks in this component can run in parallel. Today every task in
this feature changes one file, and the tasks must run in sequence.

This change specifies two classes in their own files. The class `Input` wraps the termios key
read. The class `Renderer` wraps the drawing. The game loop then calls `Input::pollKey(c)` and
`Renderer::draw(board)`. The behavior of the game must not change. These classes are technical
infrastructure. They add no domain logic, so the domain model stays the same.

## Artifacts

- [Specifications](specifications/README.md)
- [Implementation plan](tasks/README.md)
