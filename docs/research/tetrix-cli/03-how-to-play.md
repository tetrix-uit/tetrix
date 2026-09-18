# Nghiên cứu: Cách chơi & Điều khiển (03-how-to-play.md)

## 1. Bố cục giao diện dòng lệnh (Terminal UI Layout)

Giao diện Tetrix CLI được thiết kế theo bố cục 3 cột trực quan, gọn gàng, hiển thị rõ ràng trên
màn hình console tối thiểu 80x24 ký tự:

```text
+-------------------------------------------------------------+
|                        T E T R I X                          |
+-------------------+---------------------+-------------------+
|  [ HOLD ]         | . . . . . . . . . . |  [ NEXT ]         |
|  +-------------+  | . . . . . . . . . . |  +-------------+  |
|  |     [ ]     |  | . . . . . . . . . . |  |   [ ][ ][ ] |  |
|  |   [ ][ ][ ] |  | . . . . [ ] . . . . |  |       [ ]   |  |
|  +-------------+  | . . . [ ][ ][ ] . . |  +-------------+  |
|                   | . . . . . . . . . . |                   |
|  [ STATS ]        | . . . . . . . . . . |  [ SCORE ]        |
|  Level : 01       | . . . . . . . . . . |  0012400          |
|  Lines : 14       | . . [ ] [ ] [ ] . . |                   |
|  Goal  : 20       | . [ ][ ][ ][ ][ ] . |  [ HIGH SCORE ]   |
|                   | [ ][ ][ ][ ][ ][ ][ |  0035000          |
+-------------------+---------------------+-------------------+
| Controls: [<-/->] Move  [^/Z] Rotate  [v] Soft Drop         |
|           [Space] Hard Drop  [C] Hold  [P] Pause  [Q] Quit  |
+-------------------------------------------------------------+
```

- **Cột trái:** Khung lưu trữ khối gạch (Hold Piece) và các thông số cấp độ (Level, Lines).
- **Cột giữa:** Bàn cờ chính 10x20 hiển thị các khối gạch rơi tự do, khối bóng mờ (Ghost Piece)
  và các chướng ngại vật đã cố định.
- **Cột phải:** Khung hiển thị trước khối tiếp theo (Next Queue) và bảng điểm hiện tại, điểm cao.
- **Chân trang (Footer):** Thanh hướng dẫn phím bấm nhanh và trạng thái của ván đấu.

---

## 2. Bảng ánh xạ phím điều khiển (Keybindings Mapping)

Để phục vụ thói quen thao tác đa dạng của người dùng terminal, trò chơi hỗ trợ đồng thời hai
sơ đồ phím: **Sơ đồ phím mũi tên truyền thống** và **Sơ đồ phím ký tự (WASD / Vim-friendly)**.

| Hành động | Phím chính | Phím thay thế | Mô tả chi tiết |
| :--- | :--- | :--- | :--- |
| **Sang trái** | `Left Arrow` | `A` hoặc `H` | Di chuyển khối gạch sang trái 1 ô |
| **Sang phải** | `Right Arrow` | `D` hoặc `L` | Di chuyển khối gạch sang phải 1 ô |
| **Xoay thuận (CW)** | `Up Arrow` | `W` hoặc `K` | Xoay khối 90 độ theo chiều kim đồng hồ |
| **Xoay ngược (CCW)** | `Z` | `J` | Xoay khối 90 độ ngược chiều kim đồng hồ |
| **Soft Drop** | `Down Arrow` | `S` | Tăng tốc độ rơi của khối gạch |
| **Hard Drop** | `Spacebar` | `Enter` | Thả rơi lập tức xuống đáy và cố định vị trí |
| **Hold Piece** | `C` | `Shift` (nếu có) | Đổi khối gạch hiện tại với khối trong ngăn Hold |
| **Tạm dừng / Tiếp tục** | `P` | `Escape` | Đóng băng vòng lặp game, hiện menu tạm dừng |
| **Thoát trò chơi** | `Q` | `Ctrl + C` | Hủy game loop và khôi phục lại terminal ban đầu |

---

## 3. Quy tắc chơi và Điều kiện kết thúc (Game Rules & Game Over)

### 3.1. Quy tắc chơi cơ bản

1. Khi ván đấu bắt đầu, khối gạch đầu tiên xuất hiện ở đỉnh bàn cờ và bắt đầu rơi xuống.
2. Người chơi dùng các phím điều khiển để xoay và dịch chuyển khối vào vị trí mong muốn.
3. Khi xếp đầy một hàng ngang không có lỗ hổng, hàng đó biến mất, người chơi nhận điểm và số
   hàng tích lũy tăng lên.
4. Cứ mỗi khi xóa đủ 10 hàng, cấp độ (Level) sẽ tăng lên 1 bậc, đồng thời tốc độ rơi tự nhiên
   của khối gạch sẽ nhanh hơn.

### 3.2. Điều kiện kết thúc (Game Over / Top Out)

Ván chơi kết thúc khi xảy ra một trong các trường hợp sau:

- **Block Out:** Một khối gạch mới được sinh ra (spawn) nhưng vị trí xuất phát của nó đã bị
  chiếm bởi các khối gạch cũ trên bàn cờ.
- **Lock Out:** Toàn bộ khối gạch bị khóa lại (lock) khi đang nằm hoàn toàn phía trên hàng hiển thị
  cao nhất (vượt quá giới hạn hàng 20).

Khi Game Over, màn hình sẽ hiển thị bảng thông báo tổng kết điểm, cấp độ đạt được và cho phép
người chơi chọn:

- `[R]`: Chơi lại ván mới (Restart).
- `[Q]`: Thoát về terminal (Quit).

---

## 4. Tài liệu tham khảo (References)

1. **Thầy Nguyễn Văn Toàn (Giảng viên hướng dẫn)**: *Video bài giảng hướng dẫn lập trình Tetrix*.  
   Nguồn: [YouTube - Hướng dẫn code từ Thầy Nguyễn Văn Toàn](https://www.youtube.com/watch?v=vcXaTVjdlJ0)
2. **Hard Drop Tetris Wiki**: *Tetris Controls* (Sơ đồ phím điều khiển Tetris chuẩn quốc tế).  
   Nguồn: [Hard Drop - Controls](https://harddrop.com/wiki/Controls)
3. **Tint Repository (Tetris in Terminal)**: *ANSI Terminal UI & Game Loop Specification*.  
   Nguồn: [GitHub - nodiscc/tint](https://github.com/nodiscc/tint)
4. **Bastet (Bastard Tetris)**: *Terminal-based C++ Tetris Architecture & Input Handling*.  
   Nguồn: [GitHub - fph/bastet](https://github.com/fph/bastet)
