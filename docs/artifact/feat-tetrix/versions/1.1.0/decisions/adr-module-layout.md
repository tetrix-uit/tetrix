# adr-module-layout: One translation unit for each leaf class

**Relates to:** spec-input, spec-render
**Context:** context-tetrix-gameplay

## Context

The file apps/tetrix/main.cpp holds the whole game in free functions over
global state. Two leaf parts have no domain logic: the non-blocking termios
key read and the well renderer. Every task in this component changes one
file, so the tasks run in sequence. The project needs separate files, so
that later tasks in this component can run in parallel. The test build
compiles apps/tetrix/tests/test_rotate.cpp, which includes
apps/tetrix/main.cpp.

## Options

1. Separate header and source for each class: input.h with input.cpp, and
   render.h with render.cpp. Pro: one translation unit for each class; two
   later tasks change two file pairs and run in parallel; the test build
   leaves the POSIX file out. Con: four new files; the build command lists
   the new sources.
2. Header-only classes: input.h and render.h with inline methods. Pro: two
   new files only. Con: each includer compiles both classes; two tasks that
   edit one header still conflict; the test build cannot leave the POSIX key
   read out as easily.
3. One header and one source for both classes: leaf.h with leaf.cpp. Pro:
   one build pair; small. Con: both classes share one file, so the tasks do
   not run in parallel, and the current problem stays.

## Decision

Option 1. Each class gets its own header and source. The reason for the
change is parallel tasks in separate files. One translation unit for each
class gives independent compilation and independent edits. The test build
compiles one file today, so it continues to leave the POSIX key read out.

## Consequences

- apps/tetrix/main.cpp includes the headers with quotes:
  `#include "input.h"` and `#include "render.h"`. The test build command
  compiles tests/test_rotate.cpp and passes no include path, so the quotes
  are necessary.
- The production build compiles `main.cpp`, `input.cpp`, and `render.cpp`.
- input.cpp is not part of the test build. main.cpp keeps the
  `#ifndef TETRIX_TEST` guard around `main()`.
- The component apps/tetrix has no README. The phase 3 task states the new
  build command.
- Later tasks in this component change different files and can run in
  parallel.

The production build command:

```sh
g++ -std=c++17 -Wall -Wextra -pedantic -o tetrix main.cpp input.cpp render.cpp
./tetrix
```

The command `g++ -std=c++17 -o tetrix main.cpp` no longer links, because
`Input::pollKey` and `Renderer::draw` are defined in the two new sources.

## Feasibility constraints

Review `R-SPLIT-P2-01`. This decision and spec-input record the resolutions.

| Constraint | Resolution | Owner |
| --- | --- | --- |
| C-P2-01 | The production build compiles main.cpp, input.cpp, and render.cpp. The command is above. | solution-expert writes the phase 3 task; tetrix-expert runs the build |
| C-P2-02 | main.cpp keeps the `#ifndef TETRIX_TEST` guard around `main()`. spec-input states it. | solution-expert |
| C-P2-03 | spec-input states that the production `main()` stays excluded, not only `pollKey`. | solution-expert |
| C-P2-08 | main.cpp includes the two headers with quotes. The test build passes no include path. | solution-expert and tetrix-expert |
| C-P2-10 | apps/tetrix has no README. The phase 3 task states the new build command. | solution-expert and tetrix-expert |
