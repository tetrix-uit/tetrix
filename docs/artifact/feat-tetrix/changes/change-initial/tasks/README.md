# Implementation plan: Tetrix falling-block game

**Change:** [change-initial](../../../changes/change-initial/README.md)

## Order of work

| Step | Task | Depends on |
| --- | --- | --- |
| 1 | [task-screen](task-screen.md) | - |
| 2 | [task-block-shapes](task-block-shapes.md) | task-screen |
| 3 | [task-falling](task-falling.md) | task-screen, task-block-shapes |
| 4 | [task-line-clear](task-line-clear.md) | task-falling |
| 5 | [task-square-ui](task-square-ui.md) | task-falling |
| 6 | [task-rotate](task-rotate.md) | task-falling |
| 7 | [task-speedup](task-speedup.md) | task-line-clear |

Order respects the domain policy: lock (step 3) before clear rows (step 4)
before speedup (step 7). Spawn (step 2) precedes the loop (step 3) so the
game-over path via `spawnBlockOk()` exists before the loop uses it.

All tasks touch one component (`apps/tetrix`) and one context
(`context-tetrix-gameplay`). Tasks in the same component run in sequence.
Each task has `can-parallel: no`.

## Coverage

| Spec / ADR | Task |
| --- | --- |
| spec-board | task-screen |
| spec-blocks | task-block-shapes |
| spec-game-loop | task-falling |
| spec-line-clear | task-line-clear |
| spec-square-ui | task-square-ui |
| spec-rotate | task-rotate |
| spec-speedup | task-speedup |
| adr-portable-console | task-falling (termios, chrono), task-square-ui (ANSI clear) |
| adr-aggregate-pattern | task-screen, task-block-shapes, task-falling, task-line-clear, task-rotate, task-speedup (each maps to its aggregate) |

## Definition of done

- The check of each task passes.
- The acceptance criteria of each requirement pass.
