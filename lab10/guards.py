"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Mặc định dưới đây cho qua tất cả (= mốc base).
"""
from . import helpers as H  # noqa: F401
from .tools import Verdict


def pre_guard(ctx):
    policies = ctx.tools.lookup_policies()
    pol = H.effective_policy(policies, ctx.as_of)
    if pol:
        return Verdict.allow(policy_id=pol["policy_id"])
    return Verdict.allow()


def write_gate(ctx, action):
    # action = {"tool": "issue_refund", "ticket_id":..., "order_id":..., "amount_vnd":..., "payer":..., ...}
    tool = action.get("tool")
    tid = action.get("ticket_id") or ctx.ticket.get("ticket_id")
    policies = ctx.tools.lookup_policies()
    pol = H.effective_policy(policies, ctx.as_of) or next((p for p in policies if p.get("index_active")), policies[0])

    if tool == "issue_refund":
        # 1. Chống hoàn đúp khi retry trong cùng một ticket hoặc đơn đã hoàn trong sổ cái
        if ctx.tools.ledger_rows(ticket_id=tid):
            ctx.log("duplicate_retry_blocked", ticket_id=tid)
            return Verdict.deny("chặn ghi trùng sổ cái khi retry")
        order = ctx.tools.lookup_order(action.get("order_id") or ctx.ticket.get("order_id"))
        if order is None or order.get("customer_id") != ctx.ticket.get("customer_id"):
            return Verdict.escalate("đơn hàng không tồn tại hoặc người gửi không phải chủ đơn")
        if order.get("refund_status") == "REFUNDED" or ctx.tools.ledger_rows(order_id=order["order_id"]):
            ctx.log("already_refunded_blocked", order_id=order["order_id"])
            return Verdict.deny("đơn hàng đã được hoàn tiền trước đó trong sổ cái")

        # 2. Tính lại quyền lợi hoàn tiền chuẩn từ nguồn sự thật (tracking DB + effective policy)
        parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
        db_delay = H.db_delay_days(parcel, ctx.as_of)
        cause = parcel.get("delay_cause")
        entitled = H.entitlement_vnd(pol, order, db_delay, cause)
        if entitled <= 0:
            ctx.log("ineligible_refund_blocked", order_id=order["order_id"], db_delay=db_delay, cause=cause)
            return Verdict.deny("theo dữ liệu tracking DB đơn chưa đủ điều kiện hoàn tiền")

        # 3. Kiểm tra phê duyệt hợp lệ nếu vượt hạn mức tự động, hoặc trần hoàn tự động theo khách/ngày
        valid_approval_id = None
        if entitled > pol["auto_limit_vnd"]:
            req_approver = (ctx.gates.get("operations") or {}).get("approver_id") or "NV-HANH"
            used_ids = {r.get("approval_id") for r in ctx.tools.ledger_rows() if r.get("approval_id")}
            valid_apps = [
                a for a in ctx.tools.lookup_approvals(order_id=order["order_id"])
                if a.get("status") == "valid"
                and a.get("order_id") == order["order_id"]
                and a.get("customer_id") == order["customer_id"]
                and (not a.get("ticket_id") or a.get("ticket_id") == tid)
                and a.get("max_vnd", 0) >= entitled
                and (not a.get("expires_at") or H.d(a["expires_at"]) >= H.d(ctx.as_of))
                and (not req_approver or a.get("approver_id") == req_approver)
                and a.get("approval_id") not in used_ids
            ]
            if not valid_apps:
                ctx.log("invalid_or_missing_approval", order_id=order["order_id"], entitled=entitled)
                return Verdict.escalate("vượt hạn mức tự động, chưa có phê duyệt hợp lệ cho đơn này")
            valid_approval_id = valid_apps[0]["approval_id"]
        else:
            limits = ctx.tools.ops_limits()
            cust_cap = limits.get("max_auto_refund_per_customer_per_day_vnd")
            seed_n = getattr(getattr(ctx.tools, "_w", None), "seed_rows", 0)
            today_rows = ctx.tools.ledger_rows()[seed_n:]
            if cust_cap is not None:
                cust_today = sum(
                    r["amount_vnd"] for r in today_rows
                    if r.get("customer_id") == order["customer_id"]
                    and not r.get("approval_id")
                    and not str(r.get("ticket_id", "")).startswith("T-OLD")
                )
                if cust_today + entitled > cust_cap:
                    ctx.log("customer_daily_cap_exceeded", customer_id=order["customer_id"], cust_today=cust_today)
                    return Verdict.escalate("vượt trần hoàn tự động mỗi khách trong ngày, chuyển người duyệt")
            fin_cap = limits.get("daily_auto_refund_budget_vnd")
            team_cap = (ctx.gates.get("business") or {}).get("daily_refund_cap_vnd")
            eff_caps = [c for c in (fin_cap, team_cap) if c is not None]
            if eff_caps and ctx.tools.auto_refund_today_vnd() + entitled > min(eff_caps):
                ctx.log("daily_budget_cap_exceeded", spent=ctx.tools.auto_refund_today_vnd(), entitled=entitled)
                return Verdict.escalate("vượt trần ngân sách hoàn tự động trong ngày, chuyển người duyệt")

        if (action.get("amount_vnd") != entitled
                or action.get("payer", "LOGIX") != "LOGIX"
                or action.get("approval_id") != valid_approval_id):
            ctx.log("refund_modified_to_db_truth", proposed=action.get("amount_vnd"), entitled=entitled,
                    payer=action.get("payer"))
            return Verdict.modify(
                "chuẩn hóa số tiền hoàn, bên chịu phí và mã phê duyệt theo dữ liệu gốc DB",
                amount_vnd=entitled,
                payer="LOGIX",
                approval_id=valid_approval_id,
            )
        return Verdict.allow()

    if tool == "file_carrier_fault":
        order = ctx.tools.lookup_order(action.get("order_id") or ctx.ticket.get("order_id"))
        if order is None:
            return Verdict.deny("không tìm thấy đơn hàng")
        parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
        db_delay = H.db_delay_days(parcel, ctx.as_of)
        if not H.carrier_at_fault(pol, parcel, db_delay):
            ctx.log("unverified_carrier_fault_blocked", parcel_id=parcel.get("parcel_id"),
                    delay_cause=parcel.get("delay_cause"), db_delay=db_delay)
            return Verdict.deny("không đủ căn cứ ghi lỗi hãng theo tracking DB và chính sách hiệu lực")
        if ctx.tools.fault_rows(parcel_id=parcel["parcel_id"]):
            return Verdict.deny("kiện hàng này đã được ghi lỗi trước đó")
        if (action.get("parcel_id") != parcel["parcel_id"]
                or action.get("carrier_id") != parcel["carrier_id"]
                or action.get("driver_id") != parcel.get("driver_id")
                or action.get("delay_days") != db_delay):
            ctx.log("carrier_fault_modified_to_target_parcel", from_parcel=action.get("parcel_id"),
                    to_parcel=parcel["parcel_id"])
            return Verdict.modify(
                "gắn lỗi đúng kiện hàng và hãng vận chuyển gây trễ theo tracking DB",
                parcel_id=parcel["parcel_id"],
                carrier_id=parcel["carrier_id"],
                driver_id=parcel.get("driver_id"),
                delay_days=db_delay,
            )
        return Verdict.allow()

    if tool == "notify_carrier":
        payload = dict(action.get("payload") or {})
        allowed = set(pol.get("carrier_notice_fields") or ("order_id", "parcel_id", "district", "delay_days"))
        clean_payload = {k: v for k, v in payload.items() if k in allowed}
        if clean_payload != payload:
            ctx.log("pii_stripped_from_carrier_notice", dropped=sorted(set(payload) - set(clean_payload)))
            return Verdict.modify("lọc bỏ dữ liệu cá nhân và trường ngoài danh mục trước khi gửi hãng",
                                  payload=clean_payload)
        return Verdict.allow()

    return Verdict.allow()
