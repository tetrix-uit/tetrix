# spec-blocks: Falling block shapes and spawn

**Master:** [Specifications](README.md)
**Covers:** req-blocks
**Context:** context-tetrix-gameplay
**Aggregate:** agg-falling-piece

## Contract

```cpp
class Blocks {
public:
  char shape[4][4];
  explicit Blocks(const char initial[4][4]);
  virtual ~Blocks() = default;
  void reset();
  virtual void rotatedShape(char out[4][4]) const = 0;
private:
  char initialShape[4][4];
};

class RotatingBlocks : public Blocks {
public:
  using Blocks::Blocks;
  void rotatedShape(char out[4][4]) const override;
};

class SquareBlocks : public Blocks {
public:
  using Blocks::Blocks;
  void rotatedShape(char out[4][4]) const override;
};

Blocks* blocks[7];    // Index 0=I, 1=O, 2=T, 3=S, 4=Z, 5=J, 6=L.
int x, y, b;          // x, y = left-top corner of the 4x4 shape in the well.
                      // b = shape index 0..6.

void spawnBlock();    // Calls spawnBlockOk(); discards the result.
bool spawnBlockOk();  // Sets x=5, y=0, b=rand()%7; resets blocks[b].
                     // Returns canPlace(blocks[b]->shape, x, y).
```

The constructor copies the supplied grid into `shape` and `initialShape`.
`reset()` copies `initialShape` into `shape`. No turn changes `initialShape`.
The virtual method writes a candidate grid without a change to the object.
Its behavior is in [spec-rotate](spec-rotate.md).

## Data model

- Each shape fills a 4 by 4 grid.
- Each grid has four filled cells. A space is empty; the shape letter fills a cell.
- Six `RotatingBlocks` objects hold I, T, S, Z, J, and L.
- One `SquareBlocks` object holds O.
- All seven objects exist for the game lifetime. The pointer table refers to these objects without copies into base objects.
- I: one full row of `I` in the grid.
- O: a 2 by 2 square of `O`.
- T: one `T` above three `T` in a row.
- S: two `S` above two `S`, shifted left by one column.
- Z: two `Z` above two `Z`, shifted right by one column.
- J: one `J` above three `J` in a row, stem at the left.
- L: one `L` above three `L` in a row, stem at the right.

The initial grids keep these filled cells. Each pair gives a zero-based row and column.

| Shape | Filled cells |
| --- | --- |
| I | (1,0), (1,1), (1,2), (1,3) |
| O | (1,1), (1,2), (2,1), (2,2) |
| T | (1,1), (2,0), (2,1), (2,2) |
| S | (1,1), (1,2), (2,0), (2,1) |
| Z | (1,0), (1,1), (2,1), (2,2) |
| J | (1,0), (2,0), (2,1), (2,2) |
| L | (1,2), (2,0), (2,1), (2,2) |

## Spawn and integration rules

- The game calls `spawnBlockOk()` at start and after each lock.
- The new shape appears at x=5, y=0.
- The selected object resets before the collision check, including a check that fails.
- A new block always uses its initial orientation, regardless of earlier turns of the same shape.
- `canMove()` and `spawnBlockOk()` pass `blocks[b]->shape` to `canPlace()`.
- `block2Board()` and `boardDelBlock()` read `blocks[b]->shape[i][j]`.
- The `spawnBlock()` wrapper stays available. The loop uses the result from `spawnBlockOk()`.
- If `spawnBlockOk()` returns false, the loop of spec-game-loop draws the
  last well state and ends the game with `Game over`.

## Errors

- If the spawn cells are not free, `spawnBlockOk()` returns false and the
  game ends per spec-board. The well keeps the last locked state.
