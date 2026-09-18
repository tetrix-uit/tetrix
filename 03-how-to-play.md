# Hướng Dẫn Chơi Tetris CLI

## 1. Điều Khiển (Controls)

| Phím | Hành động |
| :---: | :--- |
| **A** | Sang trái |
| **D** | Sang phải |
| **S** | Tới nhanh xuống dưới |
| **W** | Xoay khối hình |
| **P** | Tạm dừng game (Pause) |
| **Q** | Thoát game (Quit) |
| **R** | Chơi lại (Restart) |

---

## 2. Luồng Chơi (Game Flow)

1. **Spawn**: Khối hình xuất hiện ở đỉnh màn hình.
2. **Di chuyển/Xoay**: Dùng phím A/D để di chuyển, W để xoay, S để thả nhanh.
3. **Lock**: Khối hình chạm đáy hoặc chạm khối khác sẽ cố định vị trí.
4. **Clear**: Điền đầy một hàng ngang để xóa hàng và ghi điểm.

---

## 3. Thuật Ngữ (Terminology)

* **Tetromino**: Mảnh ghép gồm 4 ô vuông rơi từ trên xuống.
* **Board**: Bảng chơi kích thước 10x20.
* **Line Clear**: Hàng ngang được điền đầy và xóa khỏi bảng.
* **Game Over**: Kết thúc lượt chơi khi khối hình vượt quá chiều cao của bảng.

---

## 4. Bảng Chơi (Board 10x20)