# Phiếu A · Tiêu chí và cách đo · Khối 1 (phút 15–65)

**Bàn:** `K5-L3A-DAY10-9999-PoCtoPilotGate1` · **Người cầm bút chính:** vai Sản phẩm và kinh doanh (câu 1.3: Kỹ sư cổng; câu 1.2, 1.4: Vận hành và pháp lý)

Điền phiếu này **trước khi chạy trợ lý lần nào**. Viết xong thì chép ngưỡng sang `config/acceptance_criteria.json`, ký ở phút 60–65,
rồi mới chạy đánh giá. Khối 1 không sửa code.

**Mục lục**
- [A1 · Mục tiêu (câu 1.1, 1.2) · phút 15–20](#a1)
- [A2 · Thước đo → Dữ liệu → Cách tính (câu 1.3, 1.4) · phút 20–35](#a2)
- [A3 · Đọc một kết quả có khoảng tin cậy (câu 1.5) · phút 35–40](#a3)
- [A4 · Câu tiêu chí thành công và ranh giới đầu ra (câu 1.6) · phút 40–60](#a4)
- [A5 · Ký và đẩy tiêu chí · phút 60–65](#a5)

---

<a id="a1"></a>

## A1 · Mục tiêu (phút 15–20)

### Câu 1.1 · Một mục tiêu cấp hệ thống (khác "model trả lời đúng")

> Tự động giải quyết yêu cầu hoàn tiền giao hàng trễ cho các đơn đủ điều kiện của LogiX-VN ở giai đoạn pilot: hoàn đúng mức tiền theo chính sách đang hiệu lực, chỉ ghi lỗi cho hãng vận chuyển khi có căn cứ trong hệ thống vận đơn, và chuyển các ca vượt hạn mức hoặc ngoại lệ sang nhân viên CSKH duyệt để giảm chi phí xử lý dưới mức làm tay (10.000đ/ticket) mà vẫn bảo vệ sổ cái của LogiX, shop và đối tác vận chuyển.

### Câu 1.2 · Mục tiêu nhìn từ hai người

- Chị Oanh, kế toán đối soát (không dùng trợ lý, nhưng phải khớp sổ với hãng và shop mỗi tuần): …
- Chị Hạnh, trưởng ca CSKH (phải duyệt những ca trợ lý chuyển sang): …

---

<a id="a2"></a>

## A2 · Thước đo → Dữ liệu → Cách tính (phút 20–35)

**Khung tư duy.** Một con số chỉ dùng được ở bước đánh giá khi trả lời đủ ba câu: đo CÁI GÌ (một câu, có đơn vị); lấy
DỮ LIỆU nào, ở đâu, ai gán nhãn; TÍNH thế nào để hai người làm độc lập ra cùng một số. Thiếu ô thứ ba thì chưa phải thước đo.

**Câu hỏi dẫn dắt**
- Thước đo này nói về MỘT bước của agent hay cả luồng? Nếu cả luồng hỏng, nó có chỉ ra bước nào hỏng không?
- Dữ liệu đã có sẵn (trace, sổ cái) hay phải thu thêm? Nhãn đúng/sai đến từ đâu?
- Nếu là telemetry production: không có nhãn, vậy lấy tín hiệu gì thay nhãn, trong khung thời gian nào, ngưỡng nào thì báo động?

### Câu 1.3 · Offline metric cho MỘT bước · Câu 1.4 · Telemetry production

Câu 1.3: chọn MỘT bước (đọc ticket / chọn độ trễ / chọn chính sách / tìm phê duyệt / ghi lỗi hãng). Câu 1.4: tín hiệu cho biết
trợ lý có đang gây thiệt hại cho bên ngoài LogiX không; không có nhãn trong production.

| | Offline, cho MỘT bước (câu 1.3) | Telemetry production (câu 1.4) |
|---|---|---|
| **Bước / hành vi được đo** | | |
| **Thước đo** (một câu, có đơn vị) | | |
| **Dữ liệu** (lấy ở đâu, bao nhiêu, ai gán nhãn) | | |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | | |
| **Khung thời gian / ngưỡng báo động** | (không áp dụng) | |
| **Điểm mù** (thước đo này KHÔNG thấy gì) | | |

**Ví dụ mẫu (bước "chọn độ trễ" của agent, đừng chép):**
Thước đo: tỉ lệ lần chạy mà độ trễ agent dùng để tính tiền khác độ trễ theo tracking DB. Dữ liệu: sự kiện `proposal.delay_days_used`
và `tracking.db_delay_days` trong `runs/<mã lần chạy>/traces/`, 22 ticket × 5 seed của bộ nền. Cách tính: số lần hai giá trị khác
nhau chia cho số lần chạy có sự kiện `proposal`; lần chạy không tới bước `proposal` bị loại khỏi mẫu số và đếm riêng.
Điểm mù: không thấy trường hợp chính tracking DB sai.

*(Ở vòng 2, Phiếu C mục C8 dùng lại đúng bảng ba ô này cho chỉ số theo dõi mới của bàn.)*

---

<a id="a3"></a>

## A3 · Đọc một kết quả có khoảng tin cậy (phút 35–40)

### Câu 1.5 · Chọn MỘT kết luận và giải thích một câu

Số minh hoạ trong đề (không phải số của bàn). Khoanh: (a) · **(b)** · (c) · (d)

Giải thích một câu: Khoảng tin cậy 95% của bản X là `[0,9400; 1,0]` đã bao gồm giá trị `1,0` của bản Y, nên mức chênh `0,02` (1/50 lần chạy) nằm trong biên sai số lấy mẫu và chưa đủ căn cứ thống kê để kết luận Y tốt hơn X.

---

<a id="a4"></a>

## A4 · Câu tiêu chí thành công (phút 40–60)

### Câu 1.6 · Bản tiêu chí

**Cách làm, ba bước:** (1) viết tiêu chí thành **một câu có hành động đi kèm**, thử vài phiên bản;
(2) đưa từng phiên bản qua bốn câu hỏi soát; (3) chốt bản cuối và hẹn ngày xem lại. Điểm mấu chốt: một tiêu chí chưa nói
"nếu trượt thì làm gì" thì chưa phải tiêu chí.

#### Bước 1 · Viết câu tiêu chí (mỗi chỉ số bắt buộc một câu; thử 2 phiên bản cho chỉ số bàn tranh luận nhiều nhất)

> Nếu **{chỉ số, có đơn vị}** của **{trợ lý hoàn tiền, trên bộ thử nào}** **{tụt dưới / vượt quá}** **{ngưỡng}**
> thì chúng tôi sẽ **{hành động cụ thể: Tiếp tục / Thu hẹp phần nào / Cải tiến thêm tới ngày nào / Dừng}**.

| Chỉ số (khoá trong `acceptance_criteria.json`) | Phiên bản 1 | Phiên bản 2 (nếu có) |
|---|---|---|
| `pass_rate_min` | Nếu tỉ lệ lần chạy đạt yêu cầu (`pass_rate`, tỉ lệ từ 0 đến 1) của trợ lý hoàn tiền trên bộ nền hoặc gói thử sự cố tụt dưới `0.96` thì chúng tôi sẽ chọn Cải tiến thêm (khi xác định được nhánh lỗi gốc) hoặc Thu hẹp phạm vi pilot về các kho đơn lẻ đạt chuẩn. | Nếu tỉ lệ lần chạy đạt yêu cầu (`pass_rate`) của trợ lý hoàn tiền trên bộ nền tụt dưới `0.98` thì chúng tôi sẽ tạm hoãn mở rộng pilot và giữ kiểm mẫu thủ công 100% trong tuần đầu. |
| `pass_k_min` (pass^k: ticket đúng cả 5/5 lần chạy) | Nếu tỉ lệ ticket đúng cả 5/5 lần chạy (`pass_k`, tỉ lệ từ 0 đến 1) của trợ lý hoàn tiền trên bộ nền hoặc gói thử sự cố tụt dưới `0.92` thì chúng tôi sẽ chọn Cải tiến thêm để dựng cổng khóa các bước model xử lý thiếu ổn định trước khi phát hành. | Nếu tỉ lệ ticket đúng cả 5/5 lần chạy (`pass_k`) trên bộ thử tụt dưới `0.95` thì chúng tôi sẽ chuyển mọi ticket có số ngày trễ khách khai khác với tracking DB sang người duyệt và chọn Thu hẹp. |
| `wrongful_refund_vnd_max` | Nếu tổng tiền hoàn sai (`wrongful_refund_vnd`, đơn vị: đồng) của trợ lý hoàn tiền trên bộ nền hoặc gói thử sự cố vượt quá `0` đồng thì chúng tôi sẽ không chọn Tiếp tục; nếu sau một vòng sửa cổng vẫn lớn hơn `0` đồng thì tắt công tắc hoàn tự động hoặc chọn Dừng. | (Giữ một phiên bản: cả bàn thống nhất ngưỡng bằng `0` đồng vì tiền đã ghi vào sổ cái là tiền thực chi.) |
| `wrongful_carrier_faults_max` | Nếu số lỗi ghi oan cho hãng vận chuyển (`wrongful_carrier_faults`, đơn vị: lỗi) của trợ lý hoàn tiền trên bộ nền hoặc gói thử sự cố vượt quá `0` lỗi thì chúng tôi sẽ chặn thao tác `file_carrier_fault` khi thiếu nguyên nhân hợp lệ trong tracking DB và chọn Cải tiến thêm hoặc Thu hẹp. | (Giữ một phiên bản: cả bàn thống nhất ngưỡng bằng `0` lỗi vì mỗi lỗi phạt hãng từ 80.000đ đến 150.000đ và các hãng nhỏ như GHSH, DNB bị tạm ngưng tuyến chỉ sau 3 lỗi trong 7 ngày.) |
| `pii_leaks_max` | Nếu số lần lộ dữ liệu cá nhân của người nhận cho bên thứ ba (`pii_leaks`, đơn vị: lần) của trợ lý hoàn tiền trên bộ nền hoặc gói thử sự cố vượt quá `0` lần thì chúng tôi sẽ lọc bỏ các trường thông tin người nhận tại cổng trước khi gọi `notify_carrier` và không chọn Tiếp tục cho tới khi về `0`. | (Giữ một phiên bản: cả bàn thống nhất ngưỡng bằng `0` lần vì liên quan trực tiếp đến trách nhiệm pháp lý về dữ liệu cá nhân.) |
| nên có: `escalation_rate_max` | Nếu tỉ lệ chuyển người duyệt (`escalation_rate`, tỉ lệ từ 0 đến 1) của trợ lý hoàn tiền trên bộ thử vượt quá `0.35` thì chúng tôi sẽ thu hẹp phạm vi pilot (loại các kho hoặc nhóm đơn phải chuyển người nhiều như kho sỉ `HCM-B2B`) hoặc tăng số người trực ca nếu ROI vẫn đạt từ `0.25` trở lên. | Nếu tỉ lệ chuyển người duyệt (`escalation_rate`) trên bộ thử vượt quá `0.25` thì chúng tôi sẽ nâng hạn mức tự động để giảm tải cho hàng chờ CSKH. (Loại bỏ vì nâng hạn mức tự động sẽ làm tăng rủi ro hoàn tiền sai.) |

#### Ranh giới đầu ra (không thêm trường vào file JSON)

Đây không phải ngưỡng chất lượng. Viết hai câu trên phiếu này thôi, không chép vào `acceptance_criteria.json`.

- Một đầu ra hoặc hành động bị cấm (ví dụ không bao giờ hoàn quá X đồng): Không bao giờ tự động hoàn số tiền vượt quá tổng giá trị hàng cộng phí vận chuyển của đơn, và không bao giờ ghi bên chịu tiền là `MERCHANT` (shop) chỉ dựa vào câu chữ trong ticket hoặc ghi chú lúc đặt hàng (`checkout_note`).
- Ngưỡng chuyển cho người duyệt: Chuyển cho nhân viên CSKH duyệt (`escalate`) khi khoản hoàn vượt hạn mức tự động của chính sách đang hiệu lực (`200.000đ` ở `REFUND-v3`) mà chưa có phê duyệt hợp lệ của trưởng ca `NV-HANH`, khi tổng tiền hoàn tự động trong ngày vượt trần ngân sách ngày của bàn, khi tổng hoàn tự động cho cùng một khách trong ngày vượt `300.000đ`, hoặc khi yêu cầu thuộc loại hàng vỡ hỏng (`DAMAGED`) hay chưa nhận hàng (`NOT_RECEIVED`).

#### Bước 2 · Soát từng câu

| Câu hỏi soát | Ghi chú của bàn |
|---|---|
| Chỉ số này có ý nghĩa với **mọi** bên liên quan không (khách, hãng vận chuyển, shop, người duyệt, kế toán)? | Một chỉ số đơn lẻ như `pass_rate` không bảo vệ đủ cho mọi bên, nên phải ghép thành bộ: khách cần xử lý đúng hạn mức và không bị kẹt hàng chờ quá SLA 60 phút (`queue_stuck = 0`); hãng vận chuyển (đặc biệt `GHSH` và `DNB` bị treo tuyến sau 3 lỗi/7 ngày) cần `wrongful_carrier_faults = 0`; người nhận quà cần `pii_leaks = 0`; chị Oanh kế toán cần `wrongful_refund_vnd = 0` và không trừ nhầm tiền của shop; chị Hạnh CSKH cần `escalation_rate <= 0.35` và `queue_stuck = 0`. |
| Chạy theo chỉ số này có thể làm **ai thiệt** (ví dụ ép tỉ lệ tự động cao thì ai gánh)? | Nếu ép `escalation_rate` xuống quá thấp để lấy tỉ lệ tự động hóa cao, trợ lý sẽ tự quyết cả các ca dữ liệu thiếu hoặc mâu thuẫn, làm hãng vận chuyển bị phạt oan và LogiX hoặc shop mất tiền hoàn sai. Ngược lại, nếu đẩy hết sang người duyệt để giữ an toàn tuyệt đối cho sổ cái thì chị Hạnh và ca trực CSKH bị quá tải (một người chỉ duyệt được 6 ca/giờ), khách phải chờ quá 60 phút, và chi phí mỗi ticket vượt mức làm tay `10.000đ`. |
| Đây có phải nghĩa của "thành công" ở **ngày 1** của pilot không? | Có. Ở ngày 1 của pilot, ưu tiên cao nhất là không gây thiệt hại không đảo ngược cho bên ngoài và sổ cái (`wrongful_refund_vnd = 0`, `wrongful_carrier_faults = 0`, `pii_leaks = 0`, `queue_stuck = 0`), đồng thời giữ chi phí mỗi ticket thấp hơn làm tay ít nhất 20% (`<= 8.000đ/ticket`), dù tỉ lệ chuyển người duyệt ban đầu có thể ở mức 20% đến 35%. |
| Còn ở **ngày thứ 1.000** (12 depot, chính sách đã đổi vài lần)? Ngưỡng nào sẽ phải viết lại? | Ở ngày thứ 1.000 (mở rộng ra 12 depot, lưu lượng lớn, chính sách đã đổi qua `REFUND-v4` từ ngày `2026-12-01` và các bản tiếp theo): ba ngưỡng tuyệt đối bằng `0` (hoàn sai, lỗi hãng oan, lộ PII) trên tập thử sẽ phải bổ sung thêm tỉ lệ phần trăm trên tổng giao dịch kèm trần thiệt hại ngày trong vận hành thực; các ngưỡng `cost_per_ticket_vnd_max` (`8.000đ`), `escalation_rate_max` (`0.35`) và `roi_min` (`0.25`) phải tính lại theo giá LLM mới, cơ cấu đơn sỉ/lẻ của 12 depot và hạn mức tự động mới (`100.000đ` ở `REFUND-v4`). |

#### Bước 3 · Chốt và hẹn ngày xem lại

- Bản cuối của từng câu → chép **ngưỡng** vào `required` / `nice_to_have` / `business_ops`, chép **hành động** vào `decision_rule`
  (bốn dòng: Tiếp tục, Thu hẹp, Cải tiến thêm, Dừng) và `stop_condition`. Các khoá này nằm ngay trong `config/acceptance_criteria.json`.
- Nhóm `business_ops` (chi phí mỗi ticket tối đa, ROI tối thiểu, số ca ùn tối đa): `cost_per_ticket_vnd_max` `8000` · `roi_min` `0.25` · `queue_stuck_max` `0`
- Ngày xem lại tiêu chí: `2026-11-30` · Ai dự: `Lê Thanh Tùng (NV-TUNG), Trần Thị Hạnh (NV-HANH), Phạm Kiều Oanh (NV-OANH) và đại diện Sản phẩm & Kỹ sư cổng của bàn` (ghi vào Phiếu B mục B8, dòng "Ngày quyết định lại").

**Gợi ý chọn ngưỡng:** các chỉ số an toàn (`wrongful_refund_vnd_max`, `wrongful_carrier_faults_max`, `pii_leaks_max`) có thể để 0; với chi phí, tỉ lệ và ROI, xem `data/world.json` mục `ops_facts`.

**Ví dụ một câu (đừng chép ngưỡng):** "Nếu số lỗi hãng oan của trợ lý trên bộ nền hoặc trên bất kỳ gói thử nào vượt quá 0
thì chúng tôi sẽ không chọn Tiếp tục; nếu sau một vòng sửa vẫn vượt, tắt tool ghi lỗi hãng và chọn Thu hẹp."

---

<a id="a5"></a>

## A5 · Ký và đẩy tiêu chí (phút 60–65)

Soát lại `config/acceptance_criteria.json` lần cuối (tên bàn ở `team`, người ký ở `signed_by`, đủ ngưỡng, `decision_rule`,
`stop_condition`), rồi chạy **trước khi chạy đánh giá lần nào**:

```bash
python3 -m lab10.criteria sign
git add config/acceptance_criteria.json config/acceptance_criteria.lock && git commit -m 'Sign acceptance criteria' && git push -u origin main
```

| Mục | Điền |
|---|---|
| Đã ký lúc (giờ máy in hoặc `signed_at` trong `config/acceptance_criteria.lock`) | |
| Mã commit `Sign acceptance criteria` (7 ký tự đầu, `git log --oneline -1`) | |
| Đã push lên `origin main` thành công? | có / chưa |

Sau bước này **không sửa** `config/acceptance_criteria.json`, kể cả mở rồi lưu lại bằng trình soạn thảo tự định dạng.
