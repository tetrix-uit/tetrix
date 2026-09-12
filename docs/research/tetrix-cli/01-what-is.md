# Nghiên cứu: Tetrix CLI là gì? (01-what-is.md)

## 1. Định nghĩa và Khái niệm tổng quan

**Tetrix CLI** là phiên bản trò chơi điện tử giải đố kinh điển (dựa trên nguyên bản Tetris)
được phát triển để chạy trực tiếp trong môi trường giao diện dòng lệnh (Command Line
Interface - CLI / Terminal).

Trò chơi Tetris gốc được thiết kế bởi kỹ sư người Nga **Alexey Pajitnov** vào năm 1984.
Trò chơi xoay quanh việc điều khiển các khối hình học gồm 4 ô vuông (gọi là *Tetrominoes*)
rơi từ trên xuống một ma trận chữ nhật. Người chơi cần di chuyển, xoay các khối hình này để
xếp khít thành các hàng ngang liên tục mà không chừa khoảng trống, từ đó kích hoạt cơ chế
xóa hàng và ghi điểm.

Tetrix CLI kế thừa trọn vẹn tinh thần và cơ chế vật lý của Tetris hiện đại nhưng tối giản hóa
tầng biểu diễn (presentation layer), sử dụng các ký tự văn bản, khối Unicode (như `██`, `[]`)
và mã màu escape ANSI để hiển thị bàn cờ trên màn hình console.

---

## 2. Bối cảnh và Mục tiêu dự án

### 2.1. Bối cảnh

Trong chương trình đào tạo kỹ năng nghề nghiệp và kiến trúc phần mềm, việc xây dựng một tựa
game hoàn chỉnh chạy trên terminal giúp nhóm phát triển tập trung tối đa vào:

- Thiết kế mô hình miền (Domain-Driven Design - DDD).
- Tách biệt rạch ròi giữa logic nghiệp vụ trò chơi (Core Domain Engine) và giao diện hiển thị
  (Terminal Presentation).
- Quản lý vòng lặp trò chơi thời gian thực (Real-time Game Loop) và xử lý sự kiện bất đồng bộ
  (Non-blocking I/O).

### 2.2. Mục tiêu dự án

1. **Trải nghiệm mượt mà:** Đảm bảo độ trễ thấp, phản hồi phím tức thì và không bị giật lag
   hay nhấp nháy màn hình (flickering) khi vẽ lại trên terminal.
2. **Tuân thủ chuẩn Tetris Guideline:** Áp dụng hệ thống sinh khối ngẫu nhiên chuẩn (7-Bag),
   hệ thống siêu xoay (Super Rotation System - SRS), và bảng điểm tiêu chuẩn.
3. **Đa nền tảng:** Chạy ổn định trên các terminal hiện đại của Linux, macOS và Windows
   (Windows Terminal, PowerShell).
4. **Kiến trúc module hóa:** Tách bạch các thành phần theo mô hình nhiều kho mã nguồn (Multiple
   Repositories Architecture), tạo tiền đề tích hợp các dịch vụ khác (như lưu điểm, bảng xếp hạng).

---

## 3. Kiến trúc tổng quan của Game CLI (High-level Architecture)

Hệ thống Tetrix CLI bao gồm 4 thành phần chính hoạt động phối hợp:

1. **Input Controller (Non-blocking I/O):**
   - Đọc tín hiệu phím bấm từ bàn phím người chơi mà không làm chặn (blocking) luồng xử lý
     chính của trò chơi.
   - Hỗ trợ cả phím mũi tên và các phím ký tự phổ biến (`WASD`, phím chức năng).

2. **Game Engine / Domain Core:**
   - Quản lý trạng thái bàn cờ (Playfield matrix), vị trí khối gạch hiện tại (Active Tetromino),
     hàng đợi khối tiếp theo (Next Queue), và khối lưu trữ (Hold Piece).
   - Kiểm tra va chạm (Collision Detection), quy tắc xoay và tính toán xóa hàng.

3. **Ticker & Game Timer:**
   - Đồng hồ nhịp (Game Tick) điều khiển tốc độ rơi tự nhiên của khối dựa trên cấp độ (Level)
     hiện tại của người chơi.

4. **Terminal Renderer:**
   - Quản lý bộ đệm màn hình (Frame Buffer).
   - Sử dụng các chuỗi mã thoát ANSI (ANSI Escape Sequences) để xóa màn hình, định vị con trỏ
     và gán màu sắc trực tiếp cho từng ô gạch.

---

## 4. Tài liệu tham khảo (References)

1. **Thầy Nguyễn Văn Toàn (Giảng viên hướng dẫn)**: *Video hướng dẫn lập trình dự án Tetrix*.  
   Nguồn: [YouTube - Video hướng dẫn code từ Thầy Nguyễn Văn Toàn](https://www.youtube.com/watch?v=vcXaTVjdlJ0)
2. **The Tetris Company**: *Tetris Guideline* (Tiêu chuẩn thiết kế trò chơi Tetris chính thức).  
   Nguồn: [Tetris Guideline](https://tetris.fandom.com/wiki/Tetris_Guideline)
3. **Hard Drop Tetris Wiki**: *Tetris Overview & History* (Bách khoa toàn thư Tetris thế giới).  
   Nguồn: [Hard Drop - Tetris](https://harddrop.com/wiki/Tetris)
4. **Wikipedia**: *Tetris* (Lịch sử, nguồn gốc và sự phát triển của dòng game Tetris).  
   Nguồn: [Wikipedia - Tetris](https://en.wikipedia.org/wiki/Tetris)
