# spec-input: Non-blocking key read

**Master:** [Specifications](README.md)
**Covers:** req-falling
**Context:** context-tetrix-gameplay

## Description

This specification defines the `Input` class. The class wraps the
non-blocking POSIX termios key read. The game loop reads one key per frame
with it. The class keeps no game state and no domain logic.

The file apps/tetrix/input.h declares the class. The file apps/tetrix/input.cpp
defines the class. The header includes no POSIX header, so that the test
build can include apps/tetrix/main.cpp without termios. The source file
includes `<termios.h>` and `<unistd.h>`.

## Contract

```cpp
// input.h
class Input {
public:
  static bool pollKey(char& c);
};
```

Call site in apps/tetrix/main.cpp:

```cpp
char c = 0;
if (Input::pollKey(c)) {
  // Apply the key per spec-game-loop.
}
```

Method operation, identical to the function pollKey() of version 1.0.0:

1. Save the terminal settings with `tcgetattr(STDIN_FILENO, &oldt)`.
2. If the call succeeds, disable `ICANON` and `ECHO`, set `VMIN` to 0 and
   `VTIME` to 0, and apply the new settings with
   `tcsetattr(STDIN_FILENO, TCSANOW, &newt)`.
3. Read one byte with `read(STDIN_FILENO, &ch, 1)`.
4. If the save call succeeded, restore the saved settings with
   `tcsetattr(STDIN_FILENO, TCSANOW, &oldt)`.
5. If the read returns 1, set `c` to the byte and return true.
6. Else return false.

## Data model

- The input data is one character `c`.
- The method keeps no state between calls. Each call saves and restores the
  terminal settings.
- The call does not block, because `VMIN` is 0 and `VTIME` is 0.
- If the save call fails, the read still runs with the current settings.
- The class reads the Player key only. It reads no well data.

## Events

- None. The class is technical infrastructure and emits no domain event.

## Test build

- The file apps/tetrix/input.cpp is not part of the test build.
- The test build compiles apps/tetrix/tests/test_rotate.cpp. That file
  defines `TETRIX_TEST`, includes apps/tetrix/main.cpp, and defines its own
  `main()`.
- The test build never calls `Input::pollKey`, so the separate file gives
  the same POSIX exclusion as version 1.0.0.
- apps/tetrix/main.cpp keeps the `#ifndef TETRIX_TEST` guard around the
  production `main()`. If the guard goes away with the POSIX exclusion, the
  test build has two `main()` definitions and two undefined calls. The split
  removes the POSIX exclusion from main.cpp only. It does not remove the
  `main()` exclusion.

## Errors

- If no key is present, the method returns false and `c` keeps its old value.
- If the terminal is not a TTY, the save call fails. The read still runs and
  the method returns false when no byte is available.
