#include "render.h"
#include <iostream>

// Draws each well cell as two text columns so the border and the blocks
// look square: wall -> dotted frame, block -> solid square, empty -> two
// spaces. Every locked/falling cell renders the same regardless of piece,
// matching the reference mockup (no per-shape letters).
void Renderer::draw(const char board[20][15]) {
  std::cout << "\033[2J\033[H";

  for (int i = 0; i < 20; i++) {
    for (int j = 0; j < 15; j++) {
      char cell = board[i][j];
      if (cell == '#')
        std::cout << "..";
      else if (cell != ' ')
        std::cout << "██";
      else
        std::cout << "  ";
    }
    std::cout << std::endl;
  }
}
