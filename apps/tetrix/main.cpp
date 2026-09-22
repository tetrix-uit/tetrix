#include <chrono>
#include <cstdlib>
#include <ctime>
#include <iostream>
#include <thread>
#ifndef TETRIX_TEST
#include <termios.h>
#include <unistd.h>
#endif

using namespace std;
#define H 20
#define W 15
char board[H][W] = {}; // ' ' = empty, '#' = wall, letter = stacked block

int x, y, b;
int delayMs = 500; // Fall delay in milliseconds per spec-speedup.
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
// Draws each well cell as two text columns so the border and the blocks
// look square: wall -> "##", block -> letter + letter, empty -> two spaces.
void draw() {
  cout << "\033[2J\033[H";

  for (int i = 0; i < H; i++, cout << endl)
    for (int j = 0; j < W; j++)
      cout << board[i][j] << board[i][j];
}

#ifndef TETRIX_TEST
// Non-blocking key read via POSIX termios. Returns true and sets c when a key
// is present.
bool pollKey(char &c) {
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

int main() {
  initBoard();
  srand(time(0));
  if (!spawnBlockOk()) {
    draw();
    cout << "Game over" << endl;
    return 0;
  }
  while (true) {
    boardDelBlock();
    char c = 0;
    if (pollKey(c)) {
      if (c == 'a' && canMove(-1, 0))
        x--;
      else if (c == 'd' && canMove(1, 0))
        x++;
      else if (c == 'x' && canMove(0, 1))
        y++;
      else if (c == 'w')
        tryRotate();
      else if (c == 'q') {
        cout << "Game quit" << endl;
        break;
      }
    }
    if (canMove(0, 1))
      y++;
    else {
      block2Board();
      int clearedRows = removeLine();
      (void)clearedRows; // Consumed by task-speedup.
      cout << "Falling block landed" << endl;
      if (!spawnBlockOk()) {
        draw();
        cout << "Game over" << endl;
        break;
      }
    }
    block2Board();
    draw();
    std::this_thread::sleep_for(std::chrono::milliseconds(delayMs));
  }
  return 0;
}
#endif
