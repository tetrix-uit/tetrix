# spec-game-loop: Fall timer, movement, lock, and controls

**Master:** [Specifications](README.md)
**Covers:** req-falling
**Context:** context-tetrix-gameplay
**Aggregate:** agg-falling-piece

## Description

This specification defines the game loop. The loop moves the Falling block
down on a timer, moves it on player demand, locks it when it lands, and ends
the game on quit.

## Contract

```cpp
bool canMove(int dx, int dy); // Returns true if the shape at (x+dx, y+dy)
                              // stays inside the walls and avoids stacked cells.
bool canPlace(char grid[4][4], int px, int py); // Returns true if each filled
                              // cell of grid at (px, py) stays inside the walls
                              // and avoids stacked cells.
void block2Board();           // Writes the shape cells into the well.
void boardDelBlock();         // Clears the shape cells from the well.
void draw();                  // Draws the full well per spec-square-ui.
bool pollKey(char& c);        // Non-blocking key read via POSIX termios.
                              // Returns true and sets c when a key is present.
int main();                   // Runs the loop below.
```

Portable API per adr-portable-console: no `conio.h`, no `kbhit()`/`getch()`,
no `_sleep()`, no `system("cls")`. The wait uses
`std::this_thread::sleep_for(std::chrono::milliseconds(delayMs))`.

Loop order per frame:

1. Clear the shape from the well with `boardDelBlock()`.
2. Read one key with `pollKey(c)` if present: `a` = left, `d` = right,
   `x` = down, `w` = rotate per spec-rotate, `q` = quit.
3. Apply the key move only if `canMove()` returns true. Apply rotation only
   via `tryRotate()` per spec-rotate. `q` ends the game.
4. Move the shape down by one row if `canMove(0, 1)` returns true.
5. Else lock the shape: call `block2Board()`, then clear lines per
   spec-line-clear, then call `spawnBlockOk()` per spec-blocks. If
   `spawnBlockOk()` returns false, draw the last well state and end the game
   with `Game over`.
6. Write the shape with `block2Board()`, call `draw()`, wait `delayMs`
   per spec-speedup.

Events:

- `Falling block landed` after the lock step.
- `Game quit` after the `q` key.
- `Game over` when `spawnBlockOk()` returns false.

## Errors

- If the key is not `a`, `d`, `x`, `w`, or `q`, the game ignores the key.
- If the target cells are outside the walls or hold stacked blocks, the move
  does not occur.
