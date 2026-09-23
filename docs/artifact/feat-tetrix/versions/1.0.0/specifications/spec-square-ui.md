# spec-square-ui: Square border and square blocks

**Master:** [Specifications](README.md)
**Covers:** req-square-ui
**Context:** context-tetrix-gameplay

## Description

This specification defines the square display. Each well cell draws with
equal height and width so the border and the blocks look square.

## Contract

```cpp
void draw(); // Writes "\033[2J\033[H", then draws rows 0..H-1.
             // Draws each cell as two text columns:
             //   wall  -> "##"
             //   block -> letter + letter (e.g. "TT")
             //   empty -> two spaces
```

Data model:

- One well cell maps to two text columns.
- The full screen line has `2 * W` text columns.
- The well keeps H=20 rows and W=15 columns per spec-board.

## Errors

- If the console is too narrow for `2 * W` columns, the display wraps. The
  game still runs; the well model does not change.
