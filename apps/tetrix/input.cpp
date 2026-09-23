#include "input.h"
#include <termios.h>
#include <unistd.h>

namespace {
termios savedTermios;
bool rawModeActive = false;
}

void Input::enableRawMode() {
  rawModeActive = tcgetattr(STDIN_FILENO, &savedTermios) == 0;
  if (!rawModeActive)
    return;
  termios raw = savedTermios;
  raw.c_lflag &= ~(ICANON | ECHO);
  raw.c_cc[VMIN] = 0;
  raw.c_cc[VTIME] = 0;
  tcsetattr(STDIN_FILENO, TCSANOW, &raw);
}

void Input::restoreMode() {
  if (rawModeActive)
    tcsetattr(STDIN_FILENO, TCSANOW, &savedTermios);
}

// Non-blocking read; relies on enableRawMode() having been called already.
bool Input::pollKey(char& c) {
  char ch = 0;
  if (read(STDIN_FILENO, &ch, 1) == 1) {
    c = ch;
    return true;
  }
  return false;
}
