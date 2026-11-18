# Team

## Thông tin nhóm

- Tên nhóm: 9999
- Lớp: `L3A`
- Repo của bàn: `K5-L3A-DAY10-9999-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): `S2`

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; thêm dòng nếu cần. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên        | MSSV        | Vai                       | Trưởng nhóm |
| --: | ------------------- | ----------- | ------------------------- | :------------: |
|   1 | Hoàng Nguyên Long | 2A202603476 | Kỹ sư cổng             |       X       |
|   2 | Lê Anh Sơn        | 2A202603440 | Vận hành và pháp lý  |                |
|   3 | Nguyễn Quang Hiệp | 2A202603509 | Sản phẩm và kinh doanh |                |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## HoangNguyenLong-2A202603476

### Phần việc phụ trách

Vai **Kỹ sư cổng** kiêm **Trưởng nhóm**: thiết lập repo & nhánh upstream; làm Câu 1.3 (Offline metric ở Phiếu A mục A2) và ký tiêu chí ở A5; đo mốc `base`, dò trace `T-002@55`, viết cổng phòng ngừa Vòng 1 trong `lab10/guards.py`, chạy behavioral test (`--adhoc`), chốt `checkpoint` (`prepared`) và hoàn thiện các mục `B0, B1, B2, B6, B7.1–B7.3, B8` trên Phiếu B; kéo gói sự cố `S2`, chạy `grade`/`trace`, nâng cấp `lab10/guards.py` và viết chỉ số theo dõi mới `directive_and_cap_anomaly_rate` trong `lab10/monitors.py`, điền các mục `C0, C1, C2, C6, C7, C8, C9` trên Phiếu C.

### Đóng góp cụ thể

- Thiết kế và lập trình `pre_guard` (ghim `effective_policy(as_of)`) và `write_gate` trong `lab10/guards.py` đối chiếu trực tiếp quyền lợi hoàn tiền chuẩn `H.entitlement_vnd`, khóa `payer = "LOGIX"`, kiểm tra `approval` hợp lệ của `NV-HANH`, kiểm tra trần lũy kế `300.000đ/khách/ngày` & trần ngân sách ngày, kiểm tra `H.carrier_at_fault` trên đúng `H.ticket_parcel` và lọc sạch PII khỏi `notify_carrier`.
- Thiết kế và cài đặt hàm monitor `directive_and_cap_anomaly_rate` trong `lab10/monitors.py` bắt chính xác 100% các ca tấn công chèn chỉ thị (`ticket.text` và `checkout_note`) cũng như các ca vượt trần hoàn tự động theo khách/ngày trên thẻ `S2` (`0.6` trên `S2` so với `0.0` trên `base`).
- Sử dụng trợ lý AI để hỗ trợ rà soát luồng code `lab10/agent.py`, `lab10/tools.py`, kiểm tra công thức cổng và định dạng bảng phân tích trên Phiếu A, B, C (mọi ngưỡng tiêu chí, thông số cổng và quyết định Gate 1 đều do nhóm thảo luận và chốt dựa trên dữ liệu `data/world.json`).

### Bằng chứng

- Commit ký tiêu chí: `473ed33`; hash chốt cổng vòng 1 (`prepared`): `729b57f1`.
- Mã lần chạy Vòng 1: `R-base-before-20261118-152020-8fc71e`, `R-base-after-20261118-155653-304c70`, `R-base-prepared-20261118-160026-304c70`.
- Mã lần chạy Vòng 2 (thẻ `S2`): `R-S2-grade-20261118-163157-304c70` (Bước 0), `R-S2-after-20261118-163528-305bfb`, `R-base-after-20261118-163529-305bfb`, `R-S2-grade-20261118-163529-305bfb` (`PASS-VISIBLE`, 5/5 mục `✅`).
- Các mục trên phiếu: Phiếu A (`A2` cột trái, `A5`), Phiếu B (`B0`, `B1`, `B2`, `B6`, `B7.1–B7.3`, `B8`), Phiếu C (`C0`, `C1`, `C2`, `C6`, `C7`, `C8`, `C9`).

### Exit ticket

- **Một điều học được:** Mọi văn bản đi vào LLM (không chỉ `ticket.text` khách gõ mà cả các trường dữ liệu trong DB như `orders.checkout_note`) đều là dữ liệu không đáng tin cậy; vì vậy các bất biến an toàn về tiền bạc, bên chịu phí (`payer`) và hạn mức phê duyệt bắt buộc phải được cưỡng chế bằng cổng code tất định (`write_gate`) đối chiếu trực tiếp với nguồn sự thật ngoài model, nhờ đó cổng Vòng 1 đã chặn đứng 100% sự cố `S2` ngay từ mốc `prepared`.
- **Một điều còn chưa chắc:** Khi ra môi trường production thực tế với lưu lượng lớn và hành vi gian lận tạo nhiều tài khoản (`customer_id` khác nhau nhưng cùng SĐT/địa chỉ nhận hàng), việc chỉ khóa trần `300.000đ/customer_id/ngày` trong `write_gate` sẽ cần kết hợp thêm định danh thực thể (entity resolution theo SĐT/tài khoản ngân hàng/địa chỉ) mà không làm tăng độ trễ xử lý của từng ticket.

## LeAnhSon-2A202603440

### Phần việc phụ trách

Vai **Vận hành và pháp lý**: điền Câu `1.2` và `1.4` (Telemetry production) trên Phiếu A (`A1`, `A2`); thiết lập mục `operations` và `legal` trong `config/operating_gates.json`; hoàn thành `B4` (HAZOP vòng 1), `B5` (Checklist 9 nhóm việc lần 1), `B7.5` (Runbook phần 1–3) và `B7.6` (Giờ cao điểm) trên Phiếu B; xử lý thẻ sự cố `S2` ở mục `C3.1` (Mức kiểm soát của con người), `C4` (HAZOP của thẻ `S2`), `C10` (Risk register) và `C11` (Cập nhật checklist & Runbook phần 4–5) trên Phiếu C.

### Đóng góp cụ thể

- Cấu hình các cổng vận hành và pháp lý trong `config/operating_gates.json` dựa trên `data/world.json`: chỉ định `pic = "NV-TUNG"`, `approver_id = "NV-HANH"`, `reviewers_on_shift = 1`, `review_capacity_per_hour = 6`, `max_queue_wait_minutes = 60`, khóa chặn PII sang bên thứ ba (`pii_fields_blocked_to_third_party`) và bật `carrier_fault_requires_recorded_cause = true`.
- Thực hiện HAZOP vòng 1 trên `file_carrier_fault` kèm 3 nhánh mở rộng ngoài kỹ thuật (Người duyệt, Dữ liệu gửi bên thứ ba, Ngân sách) và viết Runbook 1–3 cùng kịch bản Giờ cao điểm (B7.5–B7.6).
- Phân tích mức kiểm soát của con người (`C3.1`) và HAZOP `issue_refund` (`C4`) cho thẻ sự cố `S2`, đồng thời cập nhật Risk register (`C10`), Checklist 9 nhóm và Runbook phần 4–5 (`C11`) để xử lý sự cố trừ tiền `MERCHANT` và lách trần hoàn `300.000đ/khách/ngày`.

### Bằng chứng

- File cấu hình: `config/operating_gates.json` (mục `operations`, `legal`).
- Các mục trên phiếu: Phiếu A (`A1` câu 1.2, `A2` câu 1.4), Phiếu B (`B4`, `B5`, `B7.5`, `B7.6`), Phiếu C (`C3.1`, `C4`, `C10`, `C11`).
- Đối chiếu mã lần chạy: `R-base-prepared-20261118-160026-304c70` (Vòng 1) và `R-S2-grade-20261118-163529-305bfb` (Vòng 2, `PASS-VISIBLE`).

### Exit ticket

- **Một điều học được:** An toàn với bên thứ ba (shop `MERCHANT`, hãng vận chuyển, người nhận quà) không thể chỉ dựa vào lời khai trong ticket hay trường `checkout_note`, mà cần kết hợp cổng kỹ thuật tất định với phân định rõ thẩm quyền phê duyệt của con người (`NV-HANH`, `NV-OANH`) và quy trình dừng khẩn cấp trong Runbook.
- **Một điều còn chưa chắc:** Khi triển khai pilot thật và bật kiểm mẫu hoặc vào giờ cao điểm thực tế, lượng ca chuyển cho `NV-HANH` duyệt thủ công có vượt ngưỡng 6 ca/giờ buộc phải tăng `reviewers_on_shift` lên 2 hay không.

## NguyenQuangHiep-2A202603509

### Phần việc phụ trách

Vai **Sản phẩm và kinh doanh**: thiết lập tiêu chí nghiệm thu Vòng 1 tại Phiếu A (`A1` câu 1.1, `A2` câu 1.3 và 1.4 cho các ngưỡng kinh doanh, `A3` ngưỡng đi tiếp, `A4` quy tắc quyết định) và điền `config/acceptance_criteria.json`; cấu hình khối `business` trong `config/operating_gates.json`; hoàn thành các mục `B3` (bảng dò 5 con số trong `data/world.json`), `B5` (checklist các nhóm kinh doanh và quyết định), `B6` (hành trình 1 ticket qua 4 tầng) và `B7.4` (ngân sách và phạm vi) trên Phiếu B; phân tích `C5` (Specification và giả định môi trường cho thẻ `S2`), cập nhật dòng quyết định ở `C11`, chốt quyết định Gate 1 cột `v2` cùng ba dòng bắt buộc tại `C12` trên Phiếu C và hoàn thiện `submission/submission.json`.

### Đóng góp cụ thể

- Xác định và khóa bộ ngưỡng nghiệm thu trong `config/acceptance_criteria.json` (ký tại commit `473ed33`, hash `620ff5ff`) cùng cấu hình kinh doanh trong `config/operating_gates.json`: `daily_refund_cap_vnd = 1500000`, `cost_budget_per_ticket_vnd = 1200`, `roi_min = 0.25` và phạm vi `pilot_scope` toàn bộ 4 kho (`HN, HCM, DN, CT`).
- Đối chiếu số liệu tài chính và phân khúc kho/hãng giữa các mốc `base`, `prepared` và `after` trên bộ nền và thẻ sự cố `S2` (chứng minh cổng chặn hoàn toàn `32.750.000đ` trừ tiền shop oan và `33.580.000đ` hoàn sai, giữ chi phí `4.660đ/ticket <= 8.000đ`, `ROI = 1.15 >= 0.25`, tổng hoàn tự động ngày `282.000đ <= 1.500.000đ`), từ đó viết mục `C5`, chốt quyết định `v2 = Tiếp tục` ở `C12` và đồng bộ sang `submission/submission.json`.
- Sử dụng trợ lý AI để hỗ trợ tra cứu nhanh cấu trúc dữ liệu trong `data/world.json`, kiểm tra độ khớp số liệu giữa các file `report.json` và biên tập văn phong trên Phiếu A, B, C (toàn bộ ngưỡng kinh doanh, quy tắc quyết định và lựa chọn Gate 1 đều do cá nhân và nhóm tự tính toán, kiểm chứng).

### Bằng chứng

- Commit tiêu chí và cổng Vòng 1: `6525256` (Phiếu A và `acceptance_criteria.json`), `473ed33` (`Sign acceptance criteria`, hash `620ff5ff`), `87b166f` (cấu hình `business` trong `operating_gates.json` và Phiếu B).
- Mã lần chạy đối chiếu: Vòng 1 (`R-base-before-20261118-152020-8fc71e`, `R-base-prepared-20261118-160026-304c70`) và Vòng 2 trên thẻ `S2` (`R-S2-before-20261118-163158-304c70`, `R-S2-prepared-20261118-163158-304c70`, `R-S2-after-20261118-163530-305bfb`, `R-S2-grade-20261118-163529-305bfb`).
- Các mục trên phiếu và bài nộp: Phiếu A (`A1`–`A5`), Phiếu B (`B3`, `B5`, `B6`, `B7.4`), Phiếu C (`C5`, `C11` nhóm 9, `C12`), `submission/submission.json`.

### Exit ticket

- **Một điều học được:** Một hệ thống AI có thể đạt tỉ lệ qua bài và ROI rất tốt trên bộ kiểm thử nền nhưng vẫn gây thiệt hại tài chính nghiêm trọng cho đối tác (`32,75 triệu đồng` trừ nhầm vào tài khoản shop trên thẻ `S2`) nếu chỉ kiểm tra hạn mức từng đơn lẻ mà thiếu cổng cưỡng chế nguồn tiền (`payer = LOGIX`) và trần lũy kế theo khách hàng/ngày (`300.000đ/khách/ngày`).
- **Một điều còn chưa chắc:** Trong giai đoạn pilot thật sắp tới, khi khách hàng biết tới ngưỡng hoàn tự động `200.000đ/đơn` và trần `300.000đ/khách/ngày`, hành vi chia nhỏ đơn qua nhiều tài khoản sẽ làm tăng bao nhiêu phần trăm khối lượng ca `escalate` sang `NV-HANH` và ảnh hưởng thế nào tới `cost_per_ticket_vnd` ở kho `DN` (nơi đang có chi phí cao nhất là `4.916đ/ticket`).
