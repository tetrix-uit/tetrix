# Implementation plan: Tetrix falling-block game

**Change:** [change-split-modules](../../../changes/change-split-modules/README.md)

## Order of work

| Step | Task | Depends on |
| --- | --- | --- |
| 1 | [task-input](task-input.md) | - |
| 2 | [task-render](task-render.md) | task-input |

Both tasks change apps/tetrix/main.cpp in one component (`apps/tetrix`) and
one context (`context-tetrix-gameplay`). Tasks in one component run in
sequence. task-input removes the free function `pollKey()` and adds
`#include "input.h"`. task-render then removes the free function `draw()`
and adds `#include "render.h"`. The order keeps one writer on main.cpp at a
time. Each task has `can-parallel: no`.

The production build command for the change is:

```sh
g++ -std=c++17 -Wall -Wextra -pedantic -o tetrix main.cpp input.cpp render.cpp
./tetrix
```

## Coverage

| Spec | Task |
| --- | --- |
| spec-input | task-input |
| spec-render | task-render |

## Definition of done

- The check of each task passes.
- The acceptance criteria of each requirement pass.
