# Nghiên cứu: Tính năng cốt lõi (02-core-features.md)

---

## 1. Ma trận bàn cờ (Playfield / Matrix)

- Kích thước bàn chơi: **10 cột × 20 hàng**.
- Dữ liệu có thể lưu bằng mảng hai chiều:

```text
board[20][10]
```

- Mỗi ô lưu trạng thái **trống** hoặc **đã có block cố định**.
- Có thể chừa thêm vài hàng ẩn phía trên để hỗ trợ spawn, nhưng đây không phải yêu cầu bắt buộc của MVP.

Ví dụ:

```text
+----------+
|..........|
|..........|
|..........|
|..........|
|..........|
+----------+
```

---

## 2. Hệ thống 7 khối gạch (The 7 Tetrominoes)

Game sử dụng 7 tetromino cơ bản: **I, O, T, S, Z, J, L**.

| Khối | Màu thường dùng | Cấu trúc ASCII | Hướng spawn |
| :---: | :--- | :--- | :--- |
| **I** | Cyan | `####` | Nằm ngang |
| **O** | Yellow | `##`<br>`##` | Khối vuông 2×2 |
| **T** | Purple | `###`<br>`.#.` | Nhánh giữa hướng xuống |
| **S** | Green | `.##`<br>`##.` | Dạng zíc-zắc |
| **Z** | Red | `##.`<br>`.##` | Zíc-zắc ngược |
| **J** | Blue | `#..`<br>`###` | Móc bên trái |
| **L** | Orange | `..#`<br>`###` | Móc bên phải |

Trong đó:

- `#` là block thuộc tetromino.
- `.` là ô trống trong bounding box.
- Mỗi tetromino gồm đúng **4 block**.

### Thuật toán sinh khối ngẫu nhiên (7-Bag Random Generator)

- Trò chơi không dùng hàm random ngẫu nhiên thuần túy (nhằm tránh tình trạng người chơi bị thiếu
  một loại khối quá lâu hoặc ra trùng một khối liên tục).
- Thuật toán tạo một túi ("bag") chứa đủ 7 khối khác nhau, xáo trộn thứ tự túi đó rồi phân phối
  cho người chơi. Khi hết túi, túi mới gồm 7 khối lại được sinh ra.

---

## 3. Spawn ở giữa

Khi một tetromino mới được tạo:

- Mảnh xuất hiện ở **phía trên và gần giữa board**.
- Sử dụng orientation mặc định như bảng ở trên.
- Vị trí ngang được tính sao cho bounding box của mảnh gần tâm board.

Ví dụ:

```text
....###...
.....#....
..........
```

Nếu vị trí spawn bị block cố định chiếm và không thể đặt mảnh hợp lệ, game chuyển sang **Game Over**.

---

## 4. Di chuyển và xoay

Điều khiển tối thiểu:

| Phím | Hành động |
|---|---|
| `a` | Sang trái 1 ô |
| `d` | Sang phải 1 ô |
| `w` | Xoay 90° theo chiều kim đồng hồ |

Mỗi thao tác chỉ được thực hiện khi:

- Không vượt khỏi biên board.
- Không va vào block đã lock.

Nếu phép xoay tạo ra vị trí không hợp lệ, thao tác bị hủy.

---

## 5. Rơi và Lock

Tetromino active tự động rơi xuống theo thời gian.

Luồng cơ bản:

```text
Spawn
  ↓
Fall
  ↓
Còn chỗ phía dưới?
 ├─ Có  → rơi thêm 1 hàng
 └─ Không → Lock
```

Khi mảnh không thể rơi tiếp:

1. Các block của mảnh được ghi vào `board`.
2. Mảnh trở thành block cố định.
3. Game kiểm tra hàng đầy.
4. Sau đó spawn tetromino mới.


---

## 6. Xóa hàng và tính điểm (Line Clear & Scoring)

Một hàng được xem là đầy khi cả **10 ô đều có block**:

```text
##########   ← xóa hàng
```

Khi xóa hàng:

1. Hàng đầy bị loại bỏ.
2. Các hàng phía trên dịch xuống.
3. Hàng trống mới được thêm ở phía trên.
4. Điểm được cập nhật.

Các trường hợp:

| Loại | Số hàng xóa | Điểm cơ bản |
|---|---:|---:|
| **Single** | 1 | 100 |
| **Double** | 2 | 300 |
| **Triple** | 3 | 500 |
| **Tetris** | 4 | 800 |

MVP dùng trực tiếp các giá trị trên.  
Nếu sau này có Level, điểm có thể mở rộng thành:

```text
Score = Base Score × Level
```

---

## 7. Game Over

Game kết thúc khi một tetromino mới **không thể spawn hợp lệ** vì khu vực spawn đã bị block cố định chiếm.

Khi Game Over:

- Dừng gravity.
- Không nhận input move/rotate.
- Hiển thị điểm cuối.

Ví dụ:

```text
GAME OVER
Score: 2400
```

---

## Out of Scope — Could

- **Hold Piece** — lưu tạm một mảnh để đổi lại sau.
- **Ghost Piece** — hiển thị vị trí dự kiến khi mảnh rơi xuống.
- **Next Queue** — hiển thị một hoặc nhiều mảnh tiếp theo.
- **T-Spin** — cơ chế xoay T đặc biệt và scoring liên quan.

---

## Gameplay Loop tổng quát

```text
Spawn
  ↓
Move / Rotate
  ↓
Fall
  ↓
Lock
  ↓
Clear Lines
  ↓
Update Score
  ↓
Spawn Next Piece
  ↓
...
  ↓
Game Over
```
---

## Tài liệu tham khảo

1. **The Tetris Company — About Tetris**  
   Tổng quan gameplay và 7 tetromino cơ bản.  
   https://www.tetris.com/about

2. **TetrisWiki — Tetris Guideline**  
   Tham khảo kích thước playfield, spawn, rotation và các quy tắc hiện đại.  
   https://tetris.wiki/Tetris_Guideline

3. **TetrisWiki — Tetromino**  
   Tham khảo hình dạng và orientation của 7 tetromino.  
   https://tetris.wiki/Tetromino

4. **TetrisWiki — Scoring**  
   Tham khảo hệ thống Single / Double / Triple / Tetris.  
   https://tetris.wiki/Scoring

5. **Hard Drop Tetris Wiki — Super Rotation System**  
   Tham khảo SRS và Wall Kick; không bắt buộc trong MVP.  
   https://harddrop.com/wiki/Super_Rotation_System

6. **Hard Drop Tetris Wiki — Random Generator**  
   Tham khảo cơ chế 7-Bag Random Generator.  
   https://harddrop.com/wiki/Random_Generator

7. **TetrisWiki — Top out**  
   Tham khảo điều kiện kết thúc game khi không thể spawn mảnh mới.  
   https://tetris.wiki/Top_out
