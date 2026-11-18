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
