#include <conio.h>
#include <iostream>

using namespace std;
#define H 20
#define W 15
char board[H][W] = {}; // ' ' = empty, '#' = wall, letter = stacked block

int x, y, b;
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
  system("cls");

  for (int i = 0; i < H; i++, cout << endl)
    for (int j = 0; j < W; j++)
      cout << board[i][j];
}
int main() {
  initBoard();
  srand(time(0));
  if (!spawnBlockOk()) {
    draw();
    cout << "Game over" << endl;
    return 0;
  }
  while (1) {
    boardDelBlock();
    if (kbhit()) {
      char c = getch();
      if (c == 'a' && canMove(-1, 0))
        x--;
      if (c == 'd' && canMove(1, 0))
        x++;
      if (c == 'x' && canMove(0, 1))
        y++;
      if (c == 'q')
        break;
    }
    if (canMove(0, 1))
      y++;
    else {
      block2Board();
      if (!spawnBlockOk()) {
        draw();
        cout << "Game over" << endl;
        break;
      }
    }
    block2Board();
    draw();
    _sleep(500);
  }
  return 0;
}
