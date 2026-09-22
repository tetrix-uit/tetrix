// Run from apps/tetrix:
// g++ -std=c++17 -Wall -Wextra -pedantic -o test_rotate tests/test_rotate.cpp
// ./test_rotate
// Kiểm thử trực tiếp mã sản phẩm; không chạy vòng lặp bàn phím POSIX.
#define TETRIX_TEST
#include "../main.cpp"
#include <sstream>
#include <stdexcept>
#include <string>

namespace {
void check(bool value, const char* message) {
  if (!value)
    throw std::runtime_error(message);
}

std::string gridText(const char grid[4][4]) {
  std::string result;
  for (int i = 0; i < 4; ++i)
    for (int j = 0; j < 4; ++j)
      result += grid[i][j];
  return result;
}

std::string boardText() {
  std::string result;
  for (int i = 0; i < H; ++i)
    for (int j = 0; j < W; ++j)
      result += board[i][j];
  return result;
}

// Các kết quả được viết tay từ vị trí ô; không sao chép thuật toán xoay.
const std::string initial[] = {
    "    " "IIII" "    " "    ",
    "    " " OO " " OO " "    ",
    "    " " T  " "TTT " "    ",
    "    " " SS " "SS  " "    ",
    "    " "ZZ  " " ZZ " "    ",
    "    " "J   " "JJJ " "    ",
    "    " "  L " "LLL " "    "};
const std::string clockwise[] = {
    "  I " "  I " "  I " "  I ",
    "    " " OO " " OO " "    ",
    " T  " " TT " " T  " "    ",
    " S  " " SS " "  S " "    ",
    "  Z " " ZZ " " Z  " "    ",
    " JJ " " J  " " J  " "    ",
    " L  " " L  " " LL " "    "};

class Capture {
public:
  std::ostringstream output;
  Capture() : previous(std::cout.rdbuf(output.rdbuf())) {}
  ~Capture() { std::cout.rdbuf(previous); }
private:
  std::streambuf* previous;
};

void fixture(int index = 0, int px = 5, int py = 4) {
  initBoard();
  for (Blocks* block : blocks)
    block->reset();
  b = index;
  x = px;
  y = py;
}

void copyGrid(char target[4][4], const char source[4][4]) {
  for (int i = 0; i < 4; ++i)
    for (int j = 0; j < 4; ++j)
      target[i][j] = source[i][j];
}

void checkFour(const char grid[4][4]) {
  int filled = 0;
  for (char cell : gridText(grid))
    filled += cell != ' ';
  check(filled == 4, "Every shape must contain four filled cells");
}

void templatesAndTurns() {
  for (int index = 0; index < 7; ++index) {
    fixture(index, 5, 3);
    check(gridText(blocks[b]->shape) == initial[index], "Initial template changed");
    checkFour(blocks[b]->shape);
    char candidate[4][4];
    blocks[b]->rotatedShape(candidate);
    check(gridText(candidate) == clockwise[index], "Wrong clockwise candidate");
    check(gridText(blocks[b]->shape) == initial[index], "Candidate mutated source");
    const std::string savedBoard = boardText();
    for (int turn = 0; turn < 4; ++turn) {
      Capture capture;
      check(tryRotate(), "Open-space turn rejected");
      const std::string expected = std::string("Falling block rotated { shape: ") +
          "IOTSZJL"[index] + ", x: 5, y: 3 }\n";
      check(capture.output.str() == expected, "Wrong success event");
      check(boardText() == savedBoard && x == 5 && y == 3,
            "Accepted turn changed board or position");
      checkFour(blocks[b]->shape);
      if (turn == 0)
        check(gridText(blocks[b]->shape) == clockwise[index], "Wrong applied turn");
      if (index == 1)
        check(gridText(blocks[b]->shape) == initial[index], "O moved during turn");
    }
    check(gridText(blocks[b]->shape) == initial[index], "Four turns did not restore shape");
    copyGrid(blocks[b]->shape, candidate);
    blocks[b]->reset();
    check(gridText(blocks[b]->shape) == initial[index], "Reset lost initial template");
  }
}

// Override có dấu hiệu quan sát được, chứng minh tryRotate gọi qua hàm virtual.
class DispatchProbe : public Blocks {
public:
  mutable int calls = 0;
  DispatchProbe() : Blocks(initialBlocks[1]) {}
  void rotatedShape(char out[4][4]) const override {
    ++calls;
    copyGrid(out, shape);
  }
};

class PointerRestore {
public:
  explicit PointerRestore(Blocks* replacement) : old(blocks[1]) { blocks[1] = replacement; }
  ~PointerRestore() { blocks[1] = old; }
private:
  Blocks* old;
};

void runtimeDispatch() {
  fixture(1);
  DispatchProbe probe;
  PointerRestore restore(&probe);
  Capture capture;
  check(tryRotate(), "Probe turn rejected");
  check(probe.calls == 1, "Derived override not called exactly once");
}

void rejectUnchanged() {
  check(canPlace(blocks[b]->shape, x, y), "Rejection fixture starts invalid");
  const std::string oldShape = gridText(blocks[b]->shape);
  const std::string oldBoard = boardText();
  const int oldX = x, oldY = y, oldB = b;
  Capture capture;
  check(!tryRotate(), "Blocked turn accepted");
  check(gridText(blocks[b]->shape) == oldShape, "Rejected turn changed shape");
  check(boardText() == oldBoard, "Rejected turn changed board");
  check(x == oldX && y == oldY && b == oldB, "Rejected turn changed position/index");
  check(capture.output.str().empty(), "Rejected turn emitted event");
}

void collisions() {
  // I dọc sát hai vách vẫn hợp lệ; xoay ngang mới vượt biên.
  for (int px : {-1, W - 4}) {
    fixture(0, px, 4);
    char vertical[4][4];
    blocks[0]->rotatedShape(vertical);
    copyGrid(blocks[0]->shape, vertical);
    rejectUnchanged();
  }
  fixture(0, 5, 0);
  rejectUnchanged();
  fixture(0, 5, H - 3);
  rejectUnchanged();
  fixture();
  board[y][x + 2] = 'Z'; // Ô này chỉ thuộc hình sau xoay, không thuộc hình hiện tại.
  rejectUnchanged();
}

void spawnReset() {
  // Tìm seed trong thư viện đang chạy; không giả định rand giống giữa các hệ.
  unsigned seed = 0;
  int selected = 1;
  while (selected == 1 && seed < 10000) {
    srand(++seed);
    selected = rand() % 7;
  }
  check(selected != 1, "Cannot select a non-O spawn fixture");
  for (bool blocked : {false, true}) {
    fixture(selected);
    char turned[4][4];
    blocks[selected]->rotatedShape(turned);
    copyGrid(blocks[selected]->shape, turned);
    check(gridText(blocks[selected]->shape) != initial[selected], "Spawn fixture did not rotate");
    // Chặn một ô của hướng gốc; reset phải xảy ra ngay cả khi sinh thất bại.
    if (blocked) {
      for (int k = 0; k < 16; ++k) {
        if (initial[selected][k] != ' ') {
          board[k / 4][5 + k % 4] = 'Z';
          break;
        }
      }
    }
    const std::string oldBoard = boardText();
    srand(seed);
    Capture capture;
    check(spawnBlockOk() == !blocked, "Wrong spawn collision result");
    check(b == selected && x == 5 && y == 0, "Wrong spawn selection/position");
    check(gridText(blocks[b]->shape) == initial[selected], "Spawn did not reset orientation");
    check(boardText() == oldBoard, "Spawn changed board");
    check(capture.output.str().empty(), "Spawn emitted rotation event");
  }
}

void gridConsumers() {
  fixture(2);
  { Capture capture; check(tryRotate(), "Consumer fixture turn failed"); }
  const std::string emptyBoard = boardText();
  check(canMove(-1, 0), "Movement rejected in open space");
  board[y + 1][x + 3] = 'Z';
  check(!canMove(1, 0), "Movement ignored rotated grid collision");
  board[y + 1][x + 3] = ' ';
  block2Board();
  for (int i = 0; i < H; ++i)
    for (int j = 0; j < W; ++j) {
      char expected = emptyBoard[i * W + j];
      if (i >= y && i < y + 4 && j >= x && j < x + 4 &&
          clockwise[2][(i - y) * 4 + j - x] != ' ')
        expected = 'T';
      check(board[i][j] == expected, "Board overlay used wrong grid");
    }
  boardDelBlock();
  check(boardText() == emptyBoard, "Overlay removal changed board");
}
} // namespace

int main() {
  try {
    templatesAndTurns();
    runtimeDispatch();
    collisions();
    spawnReset();
    gridConsumers();
    std::cout << "PASS: templates, rotation, dispatch, collisions, spawn reset, events, grid consumers\n";
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "FAIL: " << error.what() << '\n';
    return 1;
  }
}
