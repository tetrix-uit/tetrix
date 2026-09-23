#include "render.h"
#include <iostream>

void Renderer::draw(const char board[20][15]) {
  std::cout << "\033[2J\033[H";

  for (int i = 0; i < 20; i++) {
    for (int j = 0; j < 15; j++)
      std::cout << board[i][j] << board[i][j];
    std::cout << std::endl;
  }
}
