# task-rotate: Rotate the falling block on demand

**Plan:** [Implementation plan](README.md)
**Member:** SV4
**Covers:** req-rotate, spec-blocks, spec-rotate
**Context:** context-tetrix-gameplay
**Component:** apps/tetrix
**Aggregate:** agg-falling-piece
**Depends on:** task-falling
**can-parallel:** no — same file; changes the block data and uses the game-loop hooks.

## Goal

The player turns the falling block 90 degrees clockwise with key `w` when free space allows it.
The implementation uses `class Blocks` and runtime polymorphism.
The user selects this task after `task-falling`, before the other remaining tasks in the master plan.

## Steps

1. Keep the branch baseline for the integration exercise described below.
2. Add `Blocks`, `RotatingBlocks`, and `SquareBlocks` in `apps/tetrix/main.cpp` per spec-blocks.
3. Replace the raw array with seven persistent concrete objects and the ordered `Blocks* blocks[7]` table.
4. Preserve all seven initial grids from spec-blocks.
5. Change `canMove()`, `spawnBlockOk()`, `block2Board()`, and `boardDelBlock()` to use `blocks[b]->shape` in the integrated code.
6. Reset the selected object before each spawn collision check, including a check that fails.
7. Keep the `spawnBlock()` wrapper and the result from `spawnBlockOk()` in the loop.
8. Implement the virtual candidate methods per spec-rotate.
9. Implement `tryRotate()` with a temporary grid and `canPlace(turned, x, y)`.
10. Apply the candidate only after the collision check passes.
11. Emit the exact event from spec-rotate once after success, including a valid O turn.
12. Preserve the merged `w` hook that calls `tryRotate()` after `boardDelBlock()`.
13. Add `apps/tetrix/tests/test_rotate.cpp` to test the production classes and functions.
14. Define `TETRIX_TEST` in that file before it includes `../main.cpp`.
15. Exclude POSIX headers, `pollKey()`, and production `main()` when `TETRIX_TEST` is defined.
16. Keep the actual class, collision, spawn, and rotation code in the test build.
17. Add comments that explain virtual dispatch, the clockwise formula, the collision guard, and spawn reset for the report.
18. Complete the integration exercise before the final checks.

## Check

Run these commands from `apps/tetrix` on POSIX:

```sh
g++ -std=c++17 -Wall -Wextra -pedantic -o test_rotate tests/test_rotate.cpp
./test_rotate
g++ -std=c++17 -Wall -Wextra -pedantic -o tetrix main.cpp
./tetrix
```

The isolated tests also support Windows with a C++17 compiler:

```powershell
g++ -std=c++17 -Wall -Wextra -pedantic -o test_rotate.exe tests/test_rotate.cpp
./test_rotate.exe
```

Test the following conditions in the separate file:

- A call through `Blocks*` reaches an observable derived override.
- All seven templates keep four filled cells and the specified initial grids.
- Clockwise turns give the expected cells; four turns restore the starting grid.
- The centered O grid stays identical.
- Both side walls, the top border, and the floor reject blocked turns from valid initial placements.
- A stacked cell in the candidate alone rejects the turn.
- Rejected turns preserve the complete shape, board, and position and emit no event.
- Accepted turns preserve the board and emit the exact event once.
- Spawn resets the orientation before both accepted and rejected collision checks.

Reset each fixture. Restore any replaced pointer or `std::cout` stream buffer after its check.
Select random spawn fixtures without an assumption about a fixed seed result across platforms.
Do not duplicate the production rotation algorithm in the tests.

On POSIX, play the final integrated game and press `w` in open space and against an obstacle.
Check that movement, spawn, and lock still work with the selected grid.
The isolated test build does not check the excluded terminal input or game loop.
Report any unavailable POSIX build or manual check as a limitation.

## Integration exercise

The branch predates the merged screen, block, and falling changes.
Keep that history until the rotation work has a commit.
Merge the main-branch baseline with those changes into the rotation branch for the exercise.
Keep the main-branch board, seven templates, collision check, spawn behavior, and existing `w` hook when resolving overlaps.
Run the checks above on the final resolved code.

Record actual conflicting sections if Git reports them.
If Git merges without a conflict, record that result.
Identify any deliberately staged overlap as a simulation; do not describe it as an accidental failure.

## Feasibility constraints

The Tetrix implementation expert reviewed this task as `R-ROTATE-P3-01`.
The solution expert owns this task text. The Tetrix implementation expert owns the code and checks.

| Constraint | Required action |
| --- | --- |
| C-P3-01 | Use the `TETRIX_TEST` boundary above without a replacement implementation. |
| C-P3-02 | Cover both spec-blocks and spec-rotate. |
| C-P3-03 | Use valid initial placements and isolated fixtures; restore pointers and output buffers. |
| C-P3-04 | Check the final resolved code and preserve the merged hooks and grid consumers. |
| C-P3-05 | Check the production build and manual `w` workflow on POSIX separately from the isolated tests. |
| C-P3-06 | Keep this phase limited to this task file; add component test instructions in phase 4 only if permitted. |

## Acceptance criteria

- The O shape keeps its square form after the turn.
- A blocked turn (wall or stacked cell) keeps the old shape and place.
- `Falling block rotated` fires with `{ shape, x, y }` on success.
- `canMove()` is not used as the rotation guard.
- The rotation call uses runtime polymorphism through `Blocks*` or `Blocks&`.
- Each spawn starts from the selected initial grid.
- The separate test file checks production code and passes after integration.
- Comments explain the rotation design for the report.
