# Báo cáo Bàn giao Nghiên cứu: Tetrix CLI (00-handover-report.md)

| Thông tin | Chi tiết |
| :--- | :--- |
| **Dự án** | Tetrix (Terminal/CLI Tetris Game) |
| **Giai đoạn** | Giai đoạn 0: Nghiên cứu tiền khả thi (Pre-development Research) |
| **Vai trò phụ trách** | Research Lead -- Điều phối & Bàn giao |
| **Thời điểm lập báo cáo** | 12/09/2026 |
| **Trạng thái nghiệm thu** | **HOÀN THÀNH (ĐẠT TẤT CẢ TIÊU CHÍ)** |

---

## 1. Mục đích và Phạm vi báo cáo

Báo cáo này được lập bởi **Research Lead** nhằm:

1. Tổng kết toàn bộ kết quả nghiên cứu tiền khả thi về trò chơi **Tetrix CLI** từ 3 tài liệu
   chuyên đề thành phần (`01-what-is.md`, `02-core-features.md`, `03-how-to-play.md`).
2. Kiểm tra và xác nhận tính hợp lệ, đầy đủ của các nguồn tài liệu tham khảo theo đúng tiêu chí
   nghiệm thu (Acceptance Criteria: mỗi tài liệu thành phần phải chứa tối thiểu $\ge 1$ nguồn tham khảo).
3. Chính thức bàn giao cơ sở lý thuyết, quy chuẩn kỹ thuật và đặc tả cơ chế cho nhóm thiết kế
   kiến trúc (Domain / Architecture) và nhóm lập trình (Development) để bước vào các pha triển
   khai tiếp theo theo mô hình Artifact-Driven.

---

## 2. Tóm tắt kết quả nghiên cứu từ các tài liệu thành phần

### 2.1. Nghiên cứu tổng quan: Tetrix CLI là gì? (`01-what-is.md`)

- **Khái niệm:** Trò chơi xếp gạch Tetris kinh điển được mô phỏng hoàn toàn trong môi trường dòng
  lệnh (Terminal / Console), sử dụng mã escape ANSI và bộ ký tự khối Unicode để dựng giao diện.
- **Mục tiêu:** Tạo ra một ứng dụng console gọn nhẹ, đa nền tảng (Linux, macOS, Windows), tách biệt
  tuyệt đối giữa logic nghiệp vụ (Core Domain) và tầng hiển thị terminal (Presentation Layer).
- **Kiến trúc mức cao:** Gồm 4 khối chức năng:
  - Bộ điều khiển nhập liệu bất đồng bộ không chặn (Non-blocking Input Controller).
  - Nhân xử lý logic nghiệp vụ game (Core Game Engine).
  - Bộ đếm nhịp thời gian thực (Game Ticker & Timer).
  - Bộ đệm dựng hình terminal (ANSI Terminal Renderer).

### 2.2. Nghiên cứu tính năng cốt lõi (`02-core-features.md`)

- **Bàn cờ:** Ma trận 10 cột x 20 hàng hiển thị, bổ sung 2 đến 4 hàng đệm phía trên (Buffer Zone)
  phục vụ việc sinh khối (Spawn).
- **Hệ thống khối gạch & thuật toán:** Đầy đủ 7 khối chuẩn (I, J, L, O, S, T, Z) với màu sắc quy
  chuẩn; áp dụng thuật toán **7-Bag Random Generator** giúp phân phối khối công bằng và chuẩn xác.
- **Cơ chế chuyển động & Xoay:** Tuân thủ hệ thống siêu xoay **Super Rotation System (SRS)** cùng
  bảng thử nghiệm Wall Kick 5 điểm khi khối bị va chạm sát mép hoặc chèn giữa các khối.
- **Hạ khối & Khóa:** Hỗ trợ Soft Drop, Hard Drop tức thì, và khoảng trễ khóa (Lock Delay ~0.5s)
  trước khi khối bị cố định vào ma trận.
- **Tính điểm & Tính năng tiện ích:** Công thức tính điểm theo cấp độ (Single, Double, Triple,
  Tetris), hỗ trợ Ghost Piece (hình bóng khối gạch), Next Queue (xem trước), và Hold Piece (lưu trữ).

### 2.3. Nghiên cứu cách chơi & điều khiển (`03-how-to-play.md`)

- **Bố cục TUI:** Thiết kế 3 cột trực quan (Cột trái: Hold & Level; Cột giữa: Bàn cờ 10x20;
  Cột phải: Next & Điểm số; Chân trang: Phím tắt và trạng thái).
- **Sơ đồ phím bấm (Keybindings):** Hỗ trợ song song cả phím mũi tên truyền thống và các phím
  ký tự thuận tay (`WASD` / Vim keys `HJKL`), phím `Space` cho Hard Drop, `C` cho Hold, `P` cho Pause.
- **Vòng đời ván đấu & Điều kiện thua (Game Over):** Xác định rõ ràng trạng thái Top Out thông
  qua hai cơ chế Block Out (tắc nghẽn vị trí xuất phát) và Lock Out (khóa khối trên đỉnh ma trận).

---

## 3. Bảng kiểm tra tiêu chí nghiệm thu (Acceptance Checklist)

Tiêu chí nghiệm thu quy định: **Duyệt đủ 3 file, mỗi file chứa $\ge 1$ nguồn tham khảo hợp lệ.**

| STT | Tên file thành phần | Nội dung trọng tâm | Số lượng nguồn | Danh sách nguồn tham khảo | Kết quả duyệt |
| :-: | :--- | :--- | :-: | :--- | :-: |
| 1 | `01-what-is.md` | Định nghĩa, mục tiêu, kiến trúc tổng quan CLI | **4 nguồn** | - **Thầy Nguyễn Văn Toàn** (*Video hướng dẫn code Tetrix*)<br>- The Tetris Company (*Tetris Guideline*)<br>- Hard Drop Wiki (*Tetris Overview & History*)<br>- Wikipedia (*Tetris*) | **ĐẠT** |
| 2 | `02-core-features.md` | Ma trận 10x20, 7 Tetrominoes, SRS, Scoring, Bag-7 | **3 nguồn** | - Hard Drop Wiki (*Super Rotation System*)<br>- Hard Drop Wiki (*Scoring*)<br>- Hard Drop Wiki (*Random Generator*) | **ĐẠT** |
| 3 | `03-how-to-play.md` | Bố cục TUI 3 cột, Keybindings (Arrow/WASD), Rules | **4 nguồn** | - **Thầy Nguyễn Văn Toàn** (*Video bài giảng hướng dẫn Tetrix*)<br>- Hard Drop Wiki (*Tetris Controls*)<br>- nodiscc/tint (*Terminal Tetris Repo*)<br>- fph/bastet (*Bastard Tetris Repo*) | **ĐẠT** |

**Đánh giá của Research Lead:**

- Cả 3 file thành phần đều đã được tạo, biên soạn chi tiết và lưu trữ chuẩn xác trong thư mục
  `docs/research/tetrix-cli/`.
- 100% các file đều đáp ứng vượt mức yêu cầu về nguồn tham khảo (mỗi file sở hữu từ 3 đến 4 nguồn
  chính thống, đặc biệt tích hợp trực tiếp **Video hướng dẫn lập trình của Giảng viên Nguyễn Văn Toàn**
  tại [YouTube](https://www.youtube.com/watch?v=vcXaTVjdlJ0)).

---

## 4. Kết luận và Kế hoạch bàn giao (Handover Next Steps)

1. **Kết luận về tính khả thi:**
   - Dự án Tetrix CLI hoàn toàn khả thi về mặt kỹ thuật, logic rõ ràng và có thể mô hình hóa
     chặt chẽ theo phương pháp Domain-Driven Design (DDD).
2. **Đối tượng nhận bàn giao:**
   - **Lead Architect / System Designer:** Sử dụng tài liệu `01` và `02` để xây dựng Bounded
     Context và Domain Model (đặt tại `docs/domain/`).
   - **Core Developers:** Sử dụng tài liệu `02` và `03` để triển khai viết Master Requirement
     và Master Specification tại `docs/artifact/` trước khi lập trình.
3. **Trạng thái bàn giao:** Chính thức hoàn tất và đóng giai đoạn nghiên cứu ban đầu.
