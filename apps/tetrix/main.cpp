#include <algorithm>
#include <chrono>
#include <cstdlib>
#include <ctime>
#include <iostream>
#include <thread>

#include "input.h"
#include "render.h"

using namespace std;
#define H 20
#define W 15
char board[H][W] = {}; // ' ' = empty, '#' = wall, letter = stacked block

int x, y, b;
int delayMs = 500;      // Fall delay in milliseconds per spec-speedup.
int clearedTotal = 0;   // Total count of cleared lines in this game.
// Index 0=I, 1=O, 2=T, 3=S, 4=Z, 5=J, 6=L.
// ' ' = empty cell, letter = filled cell.
const char initialBlocks[7][4][4] = {
                        {{' ', ' ', ' ', ' '},
                         {'I', 'I', 'I', 'I'},
                         {' ', ' ', ' ', ' '},
                         {' ', ' ', ' ', ' '}},
                        {{' ', ' ', ' ', ' '},
                         {' ', 'O', 'O', ' '},
                         {' ', 'O', 'O', ' '},
                         {' ', ' ', ' ', ' '}},
                        {{' ', ' ', ' ', ' '},
                         {' ', 'T', ' ', ' '},
                         {'T', 'T', 'T', ' '},
                         {' ', ' ', ' ', ' '}},
                        {{' ', ' ', ' ', ' '},
                         {' ', 'S', 'S', ' '},
                         {'S', 'S', ' ', ' '},
                         {' ', ' ', ' ', ' '}},
                        {{' ', ' ', ' ', ' '},
                         {'Z', 'Z', ' ', ' '},
                         {' ', 'Z', 'Z', ' '},
                         {' ', ' ', ' ', ' '}},
                        {{' ', ' ', ' ', ' '},
                         {'J', ' ', ' ', ' '},
                         {'J', 'J', 'J', ' '},
                         {' ', ' ', ' ', ' '}},
                        {{' ', ' ', ' ', ' '},
                         {' ', ' ', 'L', ' '},
                         {'L', 'L', 'L', ' '},
                         {' ', ' ', ' ', ' '}}};

class Blocks {
public:
  char shape[4][4];
  explicit Blocks(const char initial[4][4]) {
    for (int i = 0; i < 4; ++i)
      for (int j = 0; j < 4; ++j)
        initialShape[i][j] = initial[i][j];
    reset();
  }
  virtual ~Blocks() = default;
  void reset() {
    for (int i = 0; i < 4; ++i)
      for (int j = 0; j < 4; ++j)
        shape[i][j] = initialShape[i][j];
  }
  virtual void rotatedShape(char out[4][4]) const = 0;

private:
  char initialShape[4][4];
};

class RotatingBlocks : public Blocks {
public:
  using Blocks::Blocks;
  void rotatedShape(char out[4][4]) const override {
    for (int i = 0; i < 4; ++i)
      for (int j = 0; j < 4; ++j)
        out[i][j] = shape[3 - j][i];
  }
};

class SquareBlocks : public Blocks {
public:
  using Blocks::Blocks;
  void rotatedShape(char out[4][4]) const override {
    for (int i = 0; i < 4; ++i)
      for (int j = 0; j < 4; ++j)
        out[i][j] = shape[i][j];
  }
};

RotatingBlocks blockI(initialBlocks[0]), blockT(initialBlocks[2]),
    blockS(initialBlocks[3]), blockZ(initialBlocks[4]),
    blockJ(initialBlocks[5]), blockL(initialBlocks[6]);
SquareBlocks blockO(initialBlocks[1]);
Blocks* blocks[7] = {&blockI, &blockO, &blockT, &blockS, &blockZ, &blockJ, &blockL};

bool canPlace(char grid[4][4], int px, int py) {
  for (int i = 0; i < 4; i++) {
    for (int j = 0; j < 4; j++) {
      if (grid[i][j] != ' ') {
        int xt = px + j;
        int yt = py + i;
        if (xt < 1 || xt >= W - 1 || yt < 1 || yt >= H - 1)
          return false;
        if (board[yt][xt] != ' ')
          return false;
      }
    }
  }
  return true;
}

bool canMove(int dx, int dy) {
  return canPlace(blocks[b]->shape, x + dx, y + dy);
}

bool spawnBlockOk() {
  x = 5;
  y = 0;
  b = rand() % 7;
  blocks[b]->reset();
  return canPlace(blocks[b]->shape, x, y);
}

void spawnBlock() {
  spawnBlockOk();
}
bool tryRotate() {
  char turned[4][4];
  blocks[b]->rotatedShape(turned);
  if (!canPlace(turned, x, y))
    return false;
  for (int i = 0; i < 4; ++i)
    for (int j = 0; j < 4; ++j)
      blocks[b]->shape[i][j] = turned[i][j];
  const char shapeNames[] = "IOTSZJL";
  cout << "Falling block rotated { shape: " << shapeNames[b]
       << ", x: " << x << ", y: " << y << " }\n";
  return true;
}

// Scans rows H-2..1 for a full inner row, removes it, and drops the rows
// above by one per removed row. Re-checks the same row index after a removal
// since the row shifted into that slot may itself be full.
int removeLine() {
  int clearedRows = 0;
  int i = H - 2;
  while (i >= 1) {
    bool full = true;
    for (int j = 1; j <= W - 2; j++) {
      if (board[i][j] == ' ') {
        full = false;
        break;
      }
    }
    if (full) {
      for (int k = i; k > 1; k--)
        for (int j = 1; j <= W - 2; j++)
          board[k][j] = board[k - 1][j];
      for (int j = 1; j <= W - 2; j++)
        board[1][j] = ' ';
      clearedRows++;
    } else {
      i--;
    }
  }
  if (clearedRows > 0)
    cout << "Full row cleared { clearedRows: " << clearedRows << " }\n";
  return clearedRows;
}

// Shortens the fall delay by 50 ms per cleared line, floored at 100 ms. A
// count of 0 changes no delay and fires no event.
void applySpeedup(int clearedRows) {
  if (clearedRows <= 0)
    return;
  clearedTotal += clearedRows;
  delayMs = max(100, 500 - 50 * clearedTotal);
  cout << "Falling speed increased { clearedTotal: " << clearedTotal
       << ", delayMs: " << delayMs << " }\n";
}

void block2Board() {
  for (int i = 0; i < 4; i++)
    for (int j = 0; j < 4; j++)
      if (blocks[b]->shape[i][j] != ' ')
        board[y + i][x + j] = blocks[b]->shape[i][j];
}
void boardDelBlock() {
  for (int i = 0; i < 4; i++)
    for (int j = 0; j < 4; j++)
      if (blocks[b]->shape[i][j] != ' ')
        board[y + i][x + j] = ' ';
}
void initBoard() {
  for (int i = 0; i < H; i++)
    for (int j = 0; j < W; j++)
      if (i == 0 || i == H - 1 || j == 0 || j == W - 1)
        board[i][j] = '#';
      else
        board[i][j] = ' ';
}
#ifndef TETRIX_TEST
int main() {
  initBoard();
  srand(time(0));
  if (!spawnBlockOk()) {
    Renderer::draw(board);
    cout << "Game over" << endl;
    return 0;
  }

  Input::enableRawMode();

  // How often the loop checks for input, independent of the fall speed
  // (delayMs). Keeps controls responsive even while delayMs is still 500ms.
  const int pollMs = 16;
  auto lastFall = std::chrono::steady_clock::now();
  bool quit = false;
  while (!quit) {
    boardDelBlock();
    char c = 0;
    bool dirty = false;
    if (Input::pollKey(c)) {
      if (c == 'a' && canMove(-1, 0)) {
        x--;
        dirty = true;
      } else if (c == 'd' && canMove(1, 0)) {
        x++;
        dirty = true;
      } else if (c == 'x' && canMove(0, 1)) {
        y++;
        dirty = true;
      } else if (c == 'w') {
        dirty = tryRotate();
      } else if (c == 'q') {
        cout << "Game quit" << endl;
        quit = true;
      }
    }

    auto now = std::chrono::steady_clock::now();
    if (!quit && std::chrono::duration_cast<std::chrono::milliseconds>(
                     now - lastFall)
                         .count() >= delayMs) {
      lastFall = now;
      dirty = true;
      if (canMove(0, 1)) {
        y++;
      } else {
        block2Board();
        int clearedRows = removeLine();
        applySpeedup(clearedRows);
        cout << "Falling block landed" << endl;
        if (!spawnBlockOk()) {
          Renderer::draw(board);
          cout << "Game over" << endl;
          quit = true;
        }
      }
    }

    if (!quit) {
      block2Board();
      if (dirty)
        Renderer::draw(board);
      std::this_thread::sleep_for(std::chrono::milliseconds(pollMs));
    }
  }

  Input::restoreMode();
  return 0;
}
#endif
