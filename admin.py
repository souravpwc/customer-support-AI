"""
TechNova Support Dashboard — Admin / Human Support Agent Streamlit application.
Run with: streamlit run admin.py --server.port 8502
"""
import json
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

from config import ADMIN_TITLE, COMPANY_NAME, CONVERSATIONS_FILE, TICKETS_FILE
from integrations.ticket_api import TicketAPI
from evaluation.metrics import get_metrics
from governance.audit_logger import get_audit_logger
from governance.confidence_scorer import get_scorer
from ui_theme import apply_theme, render_header

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title=ADMIN_TITLE,
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme("admin")
# Styling is shared with app.py via `ui_theme` — both dashboards use the
# same colour tokens, typography, badges, expander and card styles so the
# customer chat and admin console feel like the same product.

# ── Singleton services ─────────────────────────────────────────────────────────
_ticket_api = TicketAPI()
_metrics = get_metrics()
_audit = get_audit_logger()
_scorer = get_scorer()


# ── Helpers ───────────────────────────────────────────────────────────────────
def load_conversations() -> list:
    if not CONVERSATIONS_FILE.exists():
        return []
    try:
        return list(json.loads(CONVERSATIONS_FILE.read_text()).values())
    except Exception:
        return []


def load_tickets() -> list:
    return _ticket_api.list_tickets(limit=200)


def priority_html(p: str) -> str:
    cls = f"priority-{p.lower()}"
    return f"<span class='{cls}'>{p}</span>"


def status_badge(s: str) -> str:
    if s in ("Resolved", "Closed"):
        return f"<span class='resolved-badge'>{s}</span>"
    if s == "Open":
        return f"<span class='open-badge'>{s}</span>"
    return f"<span class='escalation-badge'>{s}</span>"


# ── Header ─────────────────────────────────────────────────────────────────────
render_header(
    f"🛡️ {COMPANY_NAME} Support Dashboard",
    "Human Support Operations · Escalation Queue · Audit & Governance · Metrics",
)

# Auto-refresh button
col_refresh, col_time, _ = st.columns([1, 2, 5])
with col_refresh:
    if st.button("🔄 Refresh Data"):
        st.rerun()
with col_time:
    st.caption(f"Last refresh: {datetime.utcnow().strftime('%H:%M:%S UTC')}")

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab_overview, tab_escalation, tab_tickets, tab_conversations, tab_audit, tab_governance, tab_eval = st.tabs([
    "📊 Overview",
    "🚨 Escalation Queue",
    "🎫 Tickets",
    "💬 Conversations",
    "📋 Audit Logs",
    "🛡️ Governance",
    "📈 Evaluation",
])


# ════════════════════════════════════════════════════════════════════════════════
# TAB 1: OVERVIEW
# ════════════════════════════════════════════════════════════════════════════════
with tab_overview:
    conversations = load_conversations()
    tickets = load_tickets()
    audit_stats = _audit.get_stats()

    total_convos = len(conversations)
    escalated = sum(1 for c in conversations if c.get("escalated"))
    avg_conf = (
        sum(c.get("confidence_score", 0) for c in conversations) / total_convos
        if total_convos else 0
    )
    ticket_stats = _ticket_api.get_stats()

    # Highlight open escalations at the top of the overview so admins
    # immediately see anything pending human action.
    _open_escalations = [
        t for t in tickets
        if t.get("escalated") and t.get("status") not in ("Resolved", "Closed")
    ]
    if _open_escalations:
        _crit = sum(1 for t in _open_escalations if t["priority"] == "Critical")
        _high = sum(1 for t in _open_escalations if t["priority"] == "High")
        st.error(
            f"🚨 **{len(_open_escalations)} open escalation(s)** waiting on a human agent "
            f"&nbsp;·&nbsp; 🔴 {_crit} Critical &nbsp;·&nbsp; 🟠 {_high} High "
            f"&nbsp;·&nbsp; *See the **Escalation Queue** tab to take action.*"
        )

    # KPI row
    st.markdown("### Key Performance Indicators")
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

    def kpi(col, value, label, delta="", delta_color="normal"):
        # Darker colours so the delta row reads clearly on the white card.
        _delta_color = (
            "#15803d" if delta_color == "good"
            else "#b91c1c" if delta_color == "bad"
            else "#475569"
        )
        col.markdown(
            f"""<div class="kpi-card">
            <div class="kpi-value">{value}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-delta" style="color:{_delta_color}">{delta}</div>
            </div>""",
            unsafe_allow_html=True,
        )

    kpi(kpi1, total_convos, "Total Conversations", "📊 All time")
    kpi(kpi2, f"{avg_conf:.0%}", "Avg Confidence", "🎯 Response quality",
        "good" if avg_conf >= 0.65 else "bad")
    kpi(kpi3, escalated, "Escalations", f"{escalated/total_convos:.0%} rate" if total_convos else "",
        "good" if escalated == 0 else "bad")
    kpi(kpi4, ticket_stats.get("open", 0), "Open Tickets",
        f"{ticket_stats.get('total', 0)} total")
    kpi(kpi5, ticket_stats.get("resolved", 0), "Resolved Tickets",
        f"{ticket_stats.get('total', 0)} total", "good")

    st.markdown("---")
    col_chart1, col_chart2 = st.columns(2)

    # Intent distribution chart
    with col_chart1:
        st.markdown("### Intent Distribution")
        intent_data = _metrics.get_intent_distribution()
        if intent_data and "error" not in intent_data:
            df_intent = pd.DataFrame([
                {"Intent": k, "Count": v["count"], "Pct": v["percentage"]}
                for k, v in intent_data.items()
            ])
            fig = px.pie(
                df_intent, values="Count", names="Intent",
                color_discrete_sequence=px.colors.qualitative.Set2,
                hole=0.4,
            )
            fig.update_layout(margin=dict(t=20, b=20, l=10, r=10), height=320)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No conversation data yet. Start some chat sessions first.")

    # Confidence distribution
    with col_chart2:
        st.markdown("### Confidence Score Distribution")
        if conversations:
            conf_labels = [c.get("confidence_label", "unknown") for c in conversations]
            label_counts = {}
            for lb in conf_labels:
                label_counts[lb] = label_counts.get(lb, 0) + 1
            color_map = {"high": "#28a745", "medium": "#007bff", "low": "#fd7e14", "critical_low": "#dc3545"}
            df_conf = pd.DataFrame([
                {"Label": k, "Count": v, "Color": color_map.get(k, "#6c757d")}
                for k, v in label_counts.items()
            ])
            fig2 = px.bar(
                df_conf, x="Label", y="Count",
                color="Label",
                color_discrete_map={k: color_map.get(k, "#6c757d") for k in label_counts},
            )
            fig2.update_layout(showlegend=False, margin=dict(t=20, b=20), height=320)
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No data yet.")

    # Ticket status breakdown
    st.markdown("### Ticket Status Overview")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Open", ticket_stats.get("open", 0))
    c2.metric("In Progress", ticket_stats.get("in_progress", 0))
    c3.metric("Resolved/Closed", ticket_stats.get("resolved", 0))
    c4.metric("Escalated", ticket_stats.get("escalated", 0))


# ════════════════════════════════════════════════════════════════════════════════
# TAB 2: ESCALATION QUEUE
# ════════════════════════════════════════════════════════════════════════════════
with tab_escalation:
    st.markdown("### 🚨 Active Escalation Queue")
    escalated_tickets = _ticket_api.list_tickets(escalated_only=True, limit=50)
    open_escalated = [t for t in escalated_tickets if t["status"] not in ("Resolved", "Closed")]

    if not open_escalated:
        st.success("✅ No active escalations — all clear!")
    else:
        # Priority-aware summary banner
        crit_count = sum(1 for t in open_escalated if t["priority"] == "Critical")
        high_count = sum(1 for t in open_escalated if t["priority"] == "High")
        st.warning(
            f"⚠️ **{len(open_escalated)} escalated conversations** require human attention "
            f"&nbsp;·&nbsp; 🔴 {crit_count} Critical &nbsp;·&nbsp; 🟠 {high_count} High"
        )

        # Sort by priority (Critical → High → Medium → Low), then newest first
        _prio_rank = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
        open_escalated.sort(
            key=lambda t: (_prio_rank.get(t["priority"], 9), t.get("created_at", "")),
        )
        # Within each priority bucket, newest first
        open_escalated.sort(
            key=lambda t: t.get("created_at", ""), reverse=True,
        )
        open_escalated.sort(key=lambda t: _prio_rank.get(t["priority"], 9))

        for ticket in open_escalated:
            prio_class = ticket["priority"].lower()
            prio_emoji = {"Critical": "🔴", "High": "🟠", "Medium": "🟡", "Low": "🟢"}.get(
                ticket["priority"], "⚪"
            )
            with st.expander(
                f"{prio_emoji}  {ticket['ticket_id']}  |  {ticket['priority']}  |  "
                f"{ticket['customer_name']}  —  {ticket['subject'][:70]}",
                expanded=ticket["priority"] in ("Critical", "High"),
            ):
                st.markdown(
                    f"<div class='escalation-card {prio_class}'>"
                    f"<div class='meta'>"
                    f"🎫 <strong>{ticket['ticket_id']}</strong> &nbsp;·&nbsp; "
                    f"<span class='priority-{prio_class}'>{ticket['priority']} priority</span> &nbsp;·&nbsp; "
                    f"{ticket['category']} &nbsp;·&nbsp; "
                    f"Created {ticket['created_at'][:19].replace('T', ' ')} UTC"
                    f"</div>"
                    f"<div class='subject'>{ticket['subject']}</div>"
                    f"<div class='meta'>👤 <strong>{ticket['customer_name']}</strong> "
                    f"(<code>{ticket['customer_id']}</code>) &nbsp;·&nbsp; "
                    f"Session <code>{ticket.get('session_id', 'N/A')[:8]}…</code></div>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

                col_info, col_actions = st.columns([3, 2])
                with col_info:
                    st.markdown("**📝 Description**")
                    desc = ticket.get("description", "")[:1200]
                    st.markdown(
                        f"<div class='escalation-card {prio_class}'><pre>{desc}</pre></div>",
                        unsafe_allow_html=True,
                    )

                    if ticket.get("notes"):
                        st.markdown("**🗒️ Agent Notes**")
                        for note in ticket["notes"]:
                            st.info(f"**{note['timestamp'][:16].replace('T', ' ')}** — {note['text']}")

                with col_actions:
                    st.markdown("**⚙️ Actions**")
                    new_note = st.text_area(
                        "Add internal note",
                        key=f"note_{ticket['ticket_id']}",
                        height=90,
                        placeholder="e.g. Called customer, awaiting callback…",
                    )
                    if st.button("💾 Save Note", key=f"add_note_{ticket['ticket_id']}", use_container_width=True):
                        if new_note:
                            _ticket_api.update_ticket(ticket["ticket_id"], note=new_note)
                            st.success("Note added!")
                            st.rerun()

                    status_options = ["Open", "In Progress", "Pending Customer", "Resolved", "Closed"]
                    new_status = st.selectbox(
                        "Update Status",
                        status_options,
                        index=status_options.index(ticket["status"]) if ticket["status"] in status_options else 0,
                        key=f"status_{ticket['ticket_id']}",
                    )
                    if st.button("✅ Update Status", key=f"upd_{ticket['ticket_id']}", use_container_width=True):
                        _ticket_api.update_ticket(ticket["ticket_id"], status=new_status)
                        st.success(f"Status updated to {new_status}")
                        st.rerun()


# ════════════════════════════════════════════════════════════════════════════════
# TAB 3: TICKETS
# ════════════════════════════════════════════════════════════════════════════════
with tab_tickets:
    st.markdown("### 🎫 All Support Tickets")
    all_tickets = load_tickets()

    if not all_tickets:
        st.info("No tickets yet. Tickets are created automatically when conversations are escalated.")
    else:
        # Filter controls
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        with filter_col1:
            status_filter = st.multiselect(
                "Status", ["Open", "In Progress", "Pending Customer", "Resolved", "Closed"],
                default=[]
            )
        with filter_col2:
            priority_filter = st.multiselect(
                "Priority", ["Low", "Medium", "High", "Critical"], default=[]
            )
        with filter_col3:
            esc_only = st.checkbox("Escalated only", value=False)

        filtered = all_tickets
        if status_filter:
            filtered = [t for t in filtered if t["status"] in status_filter]
        if priority_filter:
            filtered = [t for t in filtered if t["priority"] in priority_filter]
        if esc_only:
            filtered = [t for t in filtered if t.get("escalated")]

        if filtered:
            df_tickets = pd.DataFrame([{
                "Ticket ID": t["ticket_id"],
                "Customer": t["customer_name"],
                "Subject": t["subject"][:50] + "…" if len(t["subject"]) > 50 else t["subject"],
                "Priority": t["priority"],
                "Status": t["status"],
                "Category": t["category"],
                "Escalated": "🚨 Yes" if t.get("escalated") else "No",
                "Created": t["created_at"][:19].replace("T", " "),
            } for t in filtered])
            st.dataframe(df_tickets, use_container_width=True, hide_index=True)
        else:
            st.info("No tickets match the current filters.")


# ════════════════════════════════════════════════════════════════════════════════
# TAB 4: CONVERSATIONS
# ════════════════════════════════════════════════════════════════════════════════
with tab_conversations:
    st.markdown("### 💬 Conversation Summaries")
    conversations = load_conversations()

    if not conversations:
        st.info("No conversation summaries yet. Conversations are summarized after each session.")
    else:
        # Sort by timestamp descending
        conversations.sort(key=lambda c: c.get("timestamp", ""), reverse=True)

        search = st.text_input("🔍 Search conversations", placeholder="customer name, intent, session ID…")
        if search:
            q = search.lower()
            conversations = [
                c for c in conversations
                if q in c.get("customer_name", "").lower()
                or q in c.get("intent", "").lower()
                or q in c.get("session_id", "").lower()
            ]

        for convo in conversations[:20]:
            conf = convo.get("confidence_score", 0)
            label = convo.get("confidence_label", "medium")
            esc_icon = "🚨" if convo.get("escalated") else "✅"
            # Darker palette so the inline confidence text is readable on
            # the white card surface (matches the shared theme tokens).
            color_map = {
                "high":         "#065f46",
                "medium":       "#1e3a8a",
                "low":          "#78350f",
                "critical_low": "#7f1d1d",
            }
            color = color_map.get(label, "#475569")

            with st.expander(
                f"{esc_icon} {convo.get('customer_name', 'Unknown')} | {convo.get('intent', 'unknown')} | "
                f"Confidence: {conf:.0%} | {convo.get('timestamp', '')[:16].replace('T', ' ')} UTC"
            ):
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.markdown(f"**Session ID:** `{convo.get('session_id', 'N/A')}`")
                    st.markdown(f"**Customer:** {convo.get('customer_name', 'N/A')} (`{convo.get('customer_id', 'N/A')}`)")
                    st.markdown(f"**Intent:** `{convo.get('intent', 'N/A')}`")
                    st.markdown(f"**Turns:** {convo.get('turn_count', 0)}")
                with col2:
                    st.markdown(
                        f"**Confidence:** "
                        f"<span style='color:{color};font-weight:700'>{conf:.0%} ({label})</span>",
                        unsafe_allow_html=True,
                    )
                    st.markdown(f"**Escalated:** {'Yes 🚨' if convo.get('escalated') else 'No ✅'}")
                    if tid := convo.get("ticket_id"):
                        st.markdown(f"**Ticket:** `{tid}`")

                st.markdown("**AI Summary:**")
                st.markdown(convo.get("summary", "No summary available."))

                if convo.get("needs_review", False):
                    st.warning("⚠️ This conversation was flagged for human review (low confidence).")


# ════════════════════════════════════════════════════════════════════════════════
# TAB 5: AUDIT LOGS
# ════════════════════════════════════════════════════════════════════════════════
with tab_audit:
    st.markdown("### 📋 Audit Log Viewer")

    # Filters
    filter_row = st.columns([2, 2, 2, 1])
    with filter_row[0]:
        session_filter = st.text_input("Filter by Session ID", placeholder="partial match OK")
    with filter_row[1]:
        event_types = [
            "All", "message_received", "intent_classified", "docs_retrieved",
            "api_called", "response_generated", "escalation_triggered",
            "ticket_created", "guardrail_triggered",
        ]
        evt_filter = st.selectbox("Event Type", event_types)
    with filter_row[2]:
        log_limit = st.slider("Max logs to show", 20, 500, 100)
    with filter_row[3]:
        st.markdown("<br>", unsafe_allow_html=True)
        export_btn = st.button("⬇️ Export")

    logs = _audit.read_logs(
        session_id=session_filter if session_filter else None,
        event_type=evt_filter if evt_filter != "All" else None,
        limit=log_limit,
    )

    if not logs:
        st.info("No audit logs yet. Logs are created as customers chat.")
    else:
        st.caption(f"Showing {len(logs)} log entries (newest first)")

        # Reverse for newest-first display
        logs_display = list(reversed(logs))

        df_logs = pd.DataFrame([{
            "Timestamp": log.get("timestamp", "")[:19].replace("T", " "),
            "Event": log.get("event_type", ""),
            "Session": log.get("session_id", "")[:8] + "…",
            "Intent": log.get("intent", "") or "—",
            "Confidence": f"{log.get('confidence', 0):.0%}" if log.get("confidence") else "—",
            "Customer": log.get("customer_id", "") or "—",
        } for log in logs_display])

        st.dataframe(df_logs, use_container_width=True, hide_index=True)

        if export_btn:
            csv = df_logs.to_csv(index=False)
            st.download_button(
                "Download CSV", csv, "audit_logs.csv", "text/csv"
            )

        # Detail view for individual log
        st.markdown("---")
        st.markdown("**Log Entry Detail**")
        selected_idx = st.number_input("Select log entry index (0 = newest)", 0, len(logs_display) - 1, 0)
        if logs_display:
            selected = logs_display[int(selected_idx)]
            st.json(selected)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 6: GOVERNANCE
# ════════════════════════════════════════════════════════════════════════════════
with tab_governance:
    st.markdown("### 🛡️ Governance & Safety Controls")

    col_g1, col_g2 = st.columns(2)

    with col_g1:
        st.markdown("#### Confidence Thresholds")
        from config import CONFIDENCE_THRESHOLD, ESCALATION_THRESHOLD
        st.info(f"""
| Threshold | Value | Action |
|---|---|---|
| High confidence | ≥ 0.80 | Auto-serve, no review |
| Medium confidence | {ESCALATION_THRESHOLD:.0%} – {CONFIDENCE_THRESHOLD:.0%} | Serve, flag for review |
| Low confidence | < {CONFIDENCE_THRESHOLD:.0%} | Serve, queue for review |
| Critical low | < {ESCALATION_THRESHOLD:.0%} | Auto-escalate to human |
        """)

        st.markdown("#### Data Masking Rules")
        st.success("""
- ✅ Email addresses → [EMAIL]
- ✅ Phone numbers → [PHONE]
- ✅ Credit card numbers → [CARD-NUMBER]
- ✅ SSN patterns → [SSN]
- ✅ ZIP codes → [ZIP]
- ✅ API keys (long hex) → [REDACTED-KEY]
- ✅ Passwords in text → [REDACTED]
        """)

        st.markdown("#### Blocked Topics")
        from config import BLOCKED_TOPICS
        for topic in BLOCKED_TOPICS:
            st.markdown(f"🚫 `{topic}`")

    with col_g2:
        st.markdown("#### Guardrail Rules")
        st.warning("""
**Response guardrails applied to every AI reply:**
1. **Length cap** — Max 1200 characters per response
2. **Human impersonation** — Bot cannot claim to be human
3. **Topic blocking** — Blocked topics redacted from output
4. **Legal/financial advice** — Disclaimer added automatically
5. **URL validation** — Non-TechNova URLs removed
6. **Competitor endorsement** — Flagged for review

**Input guardrails:**
1. **Prompt injection** — Detected and blocked
2. **Jailbreak attempts** — Session flagged and logged
        """)

        st.markdown("#### Guardrail Statistics")
        gr_stats = _metrics.get_guardrail_metrics()
        st.metric("Total Guardrail Triggers", gr_stats.get("total_guardrail_triggers", 0))
        if vtypes := gr_stats.get("violation_types"):
            df_vt = pd.DataFrame([
                {"Violation Type": k, "Count": v}
                for k, v in vtypes.items()
            ])
            st.dataframe(df_vt, use_container_width=True, hide_index=True)

        st.markdown("#### Human-in-the-Loop")
        st.info("""
**Review Queue triggers:**
- Confidence score < 65%
- Guardrail violations ≥ 3
- Customer explicitly requests human
- Critical priority tickets
- Safety issues (battery swelling, server outages)
        """)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 7: EVALUATION
# ════════════════════════════════════════════════════════════════════════════════
with tab_eval:
    st.markdown("### 📈 Evaluation Metrics & Sample Scenarios")

    col_m1, col_m2 = st.columns(2)

    with col_m1:
        st.markdown("#### Response Quality Metrics")
        rq = _metrics.get_response_quality_metrics()
        if "error" not in rq:
            m1, m2, m3 = st.columns(3)
            m1.metric("Total Convos", rq.get("total_conversations", 0))
            m2.metric("Avg Confidence", f"{rq.get('avg_confidence_score', 0):.0%}")
            m3.metric("High Conf Rate", f"{rq.get('high_confidence_rate', 0):.0%}")

            conf_dist = rq.get("confidence_distribution", {})
            if conf_dist:
                fig = px.bar(
                    x=list(conf_dist.keys()),
                    y=list(conf_dist.values()),
                    color=list(conf_dist.keys()),
                    color_discrete_map={
                        "high": "#28a745", "medium": "#007bff",
                        "low": "#fd7e14", "critical_low": "#dc3545"
                    },
                    labels={"x": "Confidence Level", "y": "Count"},
                    title="Confidence Distribution",
                )
                fig.update_layout(showlegend=False, height=250, margin=dict(t=30, b=10))
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Run some conversations first to see quality metrics.")

        st.markdown("#### Retrieval Quality")
        rq2 = _metrics.get_retrieval_quality()
        if "error" not in rq2:
            r1, r2, r3 = st.columns(3)
            r1.metric("Total Retrievals", rq2.get("total_retrievals", 0))
            r2.metric("Avg Top Score", f"{rq2.get('avg_top_score', 0):.3f}")
            r3.metric("Avg Docs/Query", rq2.get("avg_docs_retrieved", 0))
        else:
            st.info(rq2.get("error", "No data."))

    with col_m2:
        st.markdown("#### Resolution Metrics")
        res = _metrics.get_resolution_metrics()
        if "error" not in res:
            r1, r2, r3 = st.columns(3)
            r1.metric("FCR Rate", f"{res.get('first_contact_resolution_rate', 0):.0%}")
            r2.metric("Escalation Rate", f"{res.get('escalation_rate', 0):.0%}")
            r3.metric("Ticket Resolution", f"{res.get('ticket_resolution_rate', 0):.0%}")

            # Gauge chart for FCR
            fcr = res.get("first_contact_resolution_rate", 0)
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=fcr * 100,
                title={"text": "First Contact Resolution %"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "#28a745" if fcr >= 0.7 else "#fd7e14"},
                    "steps": [
                        {"range": [0, 50], "color": "#f8d7da"},
                        {"range": [50, 70], "color": "#fff3cd"},
                        {"range": [70, 100], "color": "#d4edda"},
                    ],
                },
            ))
            fig_gauge.update_layout(height=250, margin=dict(t=30, b=10))
            st.plotly_chart(fig_gauge, use_container_width=True)
        else:
            st.info("No resolution data yet.")

    # Sample Scenarios
    st.markdown("---")
    st.markdown("#### 📋 Sample Support Scenarios")
    st.caption("These predefined scenarios demonstrate the system's capabilities across different intents.")

    try:
        scenarios_path = __import__("pathlib").Path(__file__).parent / "evaluation" / "scenarios.json"
        scenarios = json.loads(scenarios_path.read_text())
    except Exception:
        scenarios = []

    if scenarios:
        for scenario in scenarios:
            icon = "🚨" if scenario.get("is_safety_issue") or scenario.get("is_critical") else "▶️"
            with st.expander(f"{icon} {scenario['id']} — {scenario['name']}"):
                c1, c2 = st.columns([2, 1])
                with c1:
                    st.markdown(f"**Description:** {scenario['description']}")
                    st.markdown(f"**Sample query:**")
                    st.info(scenario["user_message"])
                with c2:
                    st.markdown(f"**Expected Intent:** `{scenario['expected_intent']}`")
                    st.markdown(f"**Expected Resolution:** `{scenario['expected_resolution']}`")
                    if scenario.get("requires_api"):
                        st.markdown(f"**APIs Used:** {', '.join(scenario['requires_api'])}")
                    if scenario.get("is_safety_issue"):
                        st.error("⚠️ Safety issue — immediate escalation required")
                    if scenario.get("is_critical"):
                        st.error("🔴 Critical priority — enterprise SLA applies")
    else:
        st.info("No scenarios found.")

    # Full metrics report download
    st.markdown("---")
    if st.button("📊 Generate Full Metrics Report"):
        report = _metrics.get_full_report()
        st.json(report)
        report_json = json.dumps(report, indent=2)
        st.download_button(
            "⬇️ Download Report (JSON)",
            report_json,
            "technova_metrics_report.json",
            "application/json",
        )
