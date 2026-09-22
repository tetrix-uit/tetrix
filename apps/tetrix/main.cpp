#include <chrono>
#include <cstdlib>
#include <ctime>
#include <iostream>
#include <termios.h>
#include <thread>
#include <unistd.h>

using namespace std;
#define H 20
#define W 15
char board[H][W] = {}; // ' ' = empty, '#' = wall, letter = stacked block

int x, y, b;
int delayMs = 500; // Fall delay in milliseconds per spec-speedup.
// Index 0=I, 1=O, 2=T, 3=S, 4=Z, 5=J, 6=L.
// ' ' = empty cell, letter = filled cell.
char blocks[7][4][4] = {{{' ', ' ', ' ', ' '},
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
  return canPlace(blocks[b], x + dx, y + dy);
}

bool spawnBlockOk() {
  x = 5;
  y = 0;
  b = rand() % 7;
  return canPlace(blocks[b], x, y);
}

void spawnBlock() {
  spawnBlockOk();
}
// Stub: task-rotate completes the w wiring.
bool tryRotate() { return false; }

// Stub: task-line-clear completes the lock-step call.
int removeLine() { return 0; }

void block2Board() {
  for (int i = 0; i < 4; i++)
    for (int j = 0; j < 4; j++)
      if (blocks[b][i][j] != ' ')
        board[y + i][x + j] = blocks[b][i][j];
}
void boardDelBlock() {
  for (int i = 0; i < 4; i++)
    for (int j = 0; j < 4; j++)
      if (blocks[b][i][j] != ' ')
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
void draw() {
  cout << "\033[2J\033[H";

  for (int i = 0; i < H; i++, cout << endl)
    for (int j = 0; j < W; j++)
      cout << board[i][j];
}

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
      removeLine();
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
