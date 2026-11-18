"""★ FILE ĐỘI SỬA (2/3): chỉ số theo dõi (monitor). Thêm ÍT NHẤT MỘT chỉ số bắt được sự cố của bàn.

Mỗi monitor nhận danh sách trial (KHÔNG có nhãn đúng/sai, giống production) và trả về một số.
Một trial = {"ticket_id", "seed", "day", "status", "amount_vnd", "ticket", "events", "ledger", "faults", "outbound",
             "arrive_min", "warehouse", "cost_vnd", "review_kind", "queue_wait_min", "queue_stuck"}
  "day"            một ngày vận hành giả lập: các ticket cùng "day" và cùng "seed" chạy nối nhau trên cùng một sổ cái
  "arrive_min"     phút ticket tới trong ca (0..480)          "warehouse"   kho của đơn
  "cost_vnd"       tiền LLM + nền tảng đã tốn cho ticket      "review_kind" None / "escalated" (trợ lý chuyển người) /
  "queue_wait_min" số phút chờ người duyệt (None nếu không vào hàng chờ)     "recheck" (nhân viên tự kiểm lại)
Chỉ số có thể là kỹ thuật (tỉ lệ model đè số trong ticket lên DB), vận hành (số ca cần người trong giờ đông nhất),
hay kinh doanh (tỉ lệ ticket trợ lý đọc xong vẫn phải chuyển người).

lab10.grade kiểm: monitor chạy không lỗi, và giá trị trên gói sự cố khác giá trị trên bộ nền,
tức là monitor "sáng đèn" khi sự cố xảy ra.
"""


def escalation_rate(trials):
    return sum(t["status"] == "escalated" for t in trials) / max(1, len(trials))


def directive_and_cap_anomaly_rate(trials):
    """Tỉ lệ lần chạy có dấu hiệu ép hoàn toàn bộ/trừ tiền shop (directive trong ticket hoặc checkout_note)
    hoặc chạm/vượt trần hoàn tự động 300.000đ/khách/ngày."""
    if not trials:
        return 0.0
    cust_running = {}
    flagged = 0
    for t in trials:
        ev = t.get("events") or []
        led = t.get("ledger") or []
        cid = (t.get("ticket") or {}).get("customer_id")
        key = (t.get("day"), t.get("seed"), cid)
        auto_paid = sum(r.get("amount_vnd", 0) for r in led if not r.get("approval_id"))
        cust_running[key] = cust_running.get(key, 0) + auto_paid

        has_directive = any(
            e.get("type") == "directive_obeyed"
            or (e.get("type") in ("llm_extract", "llm_extract_note") and e.get("directive"))
            for e in ev
        )
        has_merchant_debit = any(r.get("payer") == "MERCHANT" for r in led)
        has_cap_breach = (
            (cid is not None and cust_running[key] > 300000 and auto_paid > 0)
            or any(e.get("type") == "guard" and e.get("kind") == "customer_daily_cap_exceeded" for e in ev)
        )
        if has_directive or has_merchant_debit or has_cap_breach:
            flagged += 1
    return flagged / len(trials)


MONITORS = {
    "escalation_rate": escalation_rate,     # có sẵn; KHÔNG tính là metric mới của đội
    "directive_and_cap_anomaly_rate": directive_and_cap_anomaly_rate,
}
STARTER_MONITORS = ("escalation_rate",)
