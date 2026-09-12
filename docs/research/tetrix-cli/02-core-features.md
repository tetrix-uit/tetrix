# Nghiên cứu: Tính năng cốt lõi (02-core-features.md)

## 1. Ma trận bàn cờ (Playfield / Matrix)

- **Kích thước tiêu chuẩn:** 10 cột x 20 hàng hiển thị chính thức.
- **Vùng đệm sinh khối (Buffer Zone):** Tối thiểu 2 đến 4 hàng ẩn phía trên hàng 20. Khối gạch
  được sinh ra (spawn) ở vùng này trước khi trôi dần vào vùng nhìn thấy của người chơi.
- **Mô hình tọa độ:** Biểu diễn dưới dạng lưới 2 chiều `grid[20][10]`. Mỗi ô lưu trữ trạng thái:
  trống (empty) hoặc màu sắc/loại của khối gạch đã cố định.

---

## 2. Hệ thống 7 khối gạch chuẩn (The 7 Tetrominoes)

Theo chuẩn Tetris Guideline, trò chơi bao gồm 7 loại khối hình tương ứng với 7 ký tự:

| Khối | Màu chuẩn | Cấu trúc khối | Tọa độ xuất phát (Spawn Orientation) |
| :--- | :--- | :--- | :--- |
| **I** | Cyan | Thanh dài 4 ô | Trục giữa hàng 20-21, nằm ngang |
| **O** | Yellow | Khối vuông 2x2 | Giữa bàn cờ, không thay đổi hình dạng khi xoay |
| **T** | Purple | Chữ T (3 ô ngang, 1 ô nhô) | Hàng 20, đáy hướng xuống |
| **S** | Green | Chữ S bậc thang zíc-zắc | Hàng 20, bậc thang hướng lên phải |
| **Z** | Red | Chữ Z bậc thang zíc-zắc | Hàng 20, bậc thang hướng lên trái |
| **J** | Blue | Chữ J (3 ô ngang, 1 ô móc trái) | Hàng 20, móc hướng lên |
| **L** | Orange | Chữ L (3 ô ngang, 1 ô móc phải) | Hàng 20, móc hướng lên |

### Thuật toán sinh khối ngẫu nhiên (7-Bag Random Generator)

- Trò chơi không dùng hàm random ngẫu nhiên thuần túy (nhằm tránh tình trạng người chơi bị thiếu
  một loại khối quá lâu hoặc ra trùng một khối liên tục).
- Thuật toán tạo một túi ("bag") chứa đủ 7 khối khác nhau, xáo trộn thứ tự túi đó rồi phân phối
  cho người chơi. Khi hết túi, túi mới gồm 7 khối lại được sinh ra.

---

## 3. Cơ chế xoay và Hệ thống siêu xoay (Super Rotation System - SRS)

- **Super Rotation System (SRS):** Là chuẩn xoay chính thức của Tetris Company.
- **Tâm xoay:** Mỗi khối gạch xoay quanh một tâm cố định nằm trong hộp giới hạn 3x3 (hoặc 4x4
  đối với khối I).
- **Wall Kick (Đẩy tường & Đẩy khối):**
  - Khi xoay khối tại vị trí sát mép tường hoặc sát cạnh các khối khác, nếu vị trí mới bị va chạm,
    hệ thống sẽ tự động thử nghiệm một bảng kiểm tra độ dịch chuyển (offset tests) gồm 5 vị trí
    khả thi để dịch chuyển khối sang trái, phải, lên hoặc xuống nhằm giúp khối xoay thành công.
  - Nếu tất cả các vị trí kiểm tra đều va chạm, lệnh xoay sẽ bị hủy.

---

## 4. Cơ chế di chuyển, hạ khối và khóa (Drop Mechanics & Lock Delay)

1. **Di chuyển ngang (Horizontal Shift):** Dịch chuyển khối sang trái hoặc phải theo từng ô.
2. **Trọng lực tự nhiên (Gravity Drop):** Khối tự động hạ xuống 1 ô sau mỗi khoảng thời gian `G`
   (giảm dần theo cấp độ).
3. **Soft Drop:** Người chơi giữ phím xuống để khối rơi nhanh hơn tốc độ bình thường (thường gấp
   10-20 lần), nhận thêm điểm thưởng cho mỗi hàng hạ xuống.
4. **Hard Drop:** Thả khối rơi thẳng tức thì xuống vị trí thấp nhất có thể và khóa chặt khối vào
   bàn cờ ngay lập tức.
5. **Lock Delay (Độ trễ khóa):**
   - Khi một khối tiếp đất, nó không bị cố định ngay mà có khoảng trễ xấp xỉ 0.5 giây.
   - Trong khoảng thời gian này, người chơi vẫn có thể di chuyển hoặc xoay khối để tìm vị trí
     phù hợp trước khi khối chính thức biến thành gạch cố định trên ma trận.

---

## 5. Cơ chế xóa hàng và tính điểm (Line Clear & Scoring)

### 5.1. Xóa hàng (Line Clear)

- Khi toàn bộ 10 ô của một hàng ngang được lấp đầy, hàng đó sẽ bị xóa.
- Các hàng nằm phía trên hàng vừa bị xóa sẽ hạ xuống tương ứng với số hàng đã mất.
- Các kiểu xóa hàng:
  - **Single:** Xóa 1 hàng.
  - **Double:** Xóa 2 hàng cùng lúc.
  - **Triple:** Xóa 3 hàng cùng lúc.
  - **Tetris:** Xóa 4 hàng cùng lúc (chỉ thực hiện được với khối I).

### 5.2. Công thức tính điểm (Guideline Scoring)

Điểm số tỉ lệ thuận với Cấp độ hiện tại ($Level$) của trò chơi:

- Single: $100 \times Level$
- Double: $300 \times Level$
- Triple: $500 \times Level$
- Tetris: $800 \times Level$
- Soft Drop: 1 điểm / ô rơi
- Hard Drop: 2 điểm / ô rơi

---

## 6. Các tính năng nâng cao (Quality of Life)

- **Next Queue:** Khung hiển thị trước từ 1 đến 3 khối sắp xuất hiện giúp người chơi tính toán
  chiến thuật đặt gạch.
- **Hold Piece:** Cho phép người chơi lưu tạm thời khối hiện tại vào khay dự trữ để sử dụng sau.
  Chỉ được phép đổi khối một lần cho mỗi lượt hạ gạch mới.
- **Ghost Piece (Khối bóng mờ):** Hình chiếu bóng của khối gạch hiện tại xuống đáy bàn cờ, giúp
  người chơi biết chính xác vị trí khối sẽ hạ xuống khi thực hiện Hard Drop.

---

## 7. Tài liệu tham khảo (References)

1. **Hard Drop Tetris Wiki**: *Super Rotation System (SRS)* (Chi tiết ma trận xoay và bảng offset
   kiểm tra Wall Kick).  
   Nguồn: [Hard Drop - Super Rotation System](https://harddrop.com/wiki/Super_Rotation_System)
2. **Hard Drop Tetris Wiki**: *Scoring* (Hệ thống tính điểm chuẩn và các hệ số thưởng).  
   Nguồn: [Hard Drop - Scoring](https://harddrop.com/wiki/Scoring)
3. **Hard Drop Tetris Wiki**: *Random Generator* (Quy cách hoạt động của thuật toán 7-Bag).  
   Nguồn: [Hard Drop - Random Generator](https://harddrop.com/wiki/Random_Generator)
