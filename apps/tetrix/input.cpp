#include "input.h"
#include <termios.h>
#include <unistd.h>

bool Input::pollKey(char& c) {
  termios oldt;
  termios newt;
  bool hasTermios = tcgetattr(STDIN_FILENO, &oldt) == 0;
  if (hasTermios) {
    newt = oldt;
    newt.c_lflag &= ~(ICANON | ECHO);
    newt.c_cc[VMIN] = 0;
    newt.c_cc[VTIME] = 0;
    tcsetattr(STDIN_FILENO, TCSANOW, &newt); // Setup.
  }
  char ch = 0;
  bool got = read(STDIN_FILENO, &ch, 1) == 1;
  if (hasTermios)
    tcsetattr(STDIN_FILENO, TCSANOW, &oldt); // Restore.
  if (got) {
    c = ch;
    return true;
  }
  return false;
}
