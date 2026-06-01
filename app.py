"""
TechNova Customer Support Chat — Enterprise AI assistant UI (Streamlit).

Run with:
    streamlit run app.py

Design goals
------------
* Polished, AI-native hero + sticky chat input
* Suggested-prompt cards as the empty state
* Categorised quick actions + persistent conversation history in the sidebar
* All visual tokens shared with ``admin.py`` via ``ui_theme.apply_theme``
* WCAG-AA contrast everywhere (no light text on light backgrounds)
* Streamlit-only (no React / Tailwind / custom JS frameworks)
"""
from __future__ import annotations

from datetime import datetime
from typing import Iterable

import streamlit as st

from config import APP_TITLE, COMPANY_NAME, SUPPORT_EMAIL, SUPPORT_PHONE
from agents.orchestrator import SupportOrchestrator
from ui_theme import apply_theme

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get help": f"mailto:{SUPPORT_EMAIL}",
        "About": f"{COMPANY_NAME} AI Support Assistant",
    },
)

# Shared design tokens (typography, colours, base components, contrast rules)
apply_theme("customer")


# ── Page-specific polish CSS (extends the shared theme) ──────────────────────
st.markdown(
    """
<style>
/* ─── Centre the chat surface for readable line length ─────────────── */
.main .block-container {
    max-width: 880px;
    padding-top: 1.2rem;
    padding-bottom: 7rem;   /* leave room for the sticky chat input */
}

/* ─── Welcome state ────────────────────────────────────────────────── */
.welcome-hero { text-align: center; padding: 1.4rem 0.5rem 0.3rem; }
.welcome-hero .greet {
    font-size: 1.6rem; font-weight: 700; color: #0f172a;
    margin: 0 0 0.35rem;
}
.welcome-hero .sub {
    color: #475569; font-size: 1rem; line-height: 1.55;
    margin: 0 auto; max-width: 540px;
}
.prompt-section-title {
    color: #475569; font-size: 0.74rem; font-weight: 800;
    text-transform: uppercase; letter-spacing: 0.9px;
    margin: 1.4rem 0 0.6rem; text-align: center;
}

/* Suggested-prompt cards — only inside the prompt grid we mark with
   .prompt-card-title (uses the next-sibling combinator so it does NOT
   affect any other st.columns block in the app). */
.prompt-section-title + div[data-testid="stHorizontalBlock"] .stButton button {
    height: auto !important;
    min-height: 78px !important;
    padding: 0.95rem 1rem !important;
    text-align: left !important;
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 14px !important;
    color: #0f172a !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    line-height: 1.45 !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    transition: transform 0.18s ease, box-shadow 0.18s ease,
                border-color 0.18s ease;
    white-space: normal !important;
}
.prompt-section-title + div[data-testid="stHorizontalBlock"] .stButton button:hover {
    border-color: #6366f1 !important;
    box-shadow: 0 8px 20px rgba(99, 102, 241, 0.18);
    transform: translateY(-2px);
    color: #1e1b4b !important;
    background: #f8fafc !important;
}

/* ─── Meta row (confidence + sources) below each assistant reply ──── */
.meta-row {
    display: flex; flex-wrap: wrap; align-items: center; gap: 0.45rem;
    margin-top: 0.75rem; padding-top: 0.65rem;
    border-top: 1px dashed #e2e8f0;
    font-size: 0.86rem;
}
.meta-row .meta-label {
    color: #475569; font-weight: 600; margin-right: 0.2rem;
}

/* ─── Persistent action chip above the chat input ─────────────────── */
.escalate-bar {
    margin: 0.4rem 0 0.6rem;
    display: flex; justify-content: flex-end;
}
.escalate-bar .stButton button {
    background: #fff1f2 !important;
    color: #9f1239 !important;
    border: 1px solid #fecdd3 !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 0.35rem 0.85rem !important;
}
.escalate-bar .stButton button:hover {
    background: #ffe4e6 !important;
    border-color: #fda4af !important;
    color: #881337 !important;
}

/* ─── Sidebar polish ───────────────────────────────────────────────── */
section[data-testid="stSidebar"] .sb-brand {
    display: flex; align-items: center; gap: 0.55rem;
    font-size: 1.02rem; font-weight: 800; color: #0f172a;
    margin: 0 0 0.85rem;
}
section[data-testid="stSidebar"] .sb-brand .logo {
    width: 28px; height: 28px; border-radius: 8px;
    display: inline-flex; align-items: center; justify-content: center;
    background: linear-gradient(135deg, #6366f1, #ec4899);
    color: #ffffff; font-weight: 800; font-size: 0.85rem;
    box-shadow: 0 2px 6px rgba(99, 102, 241, 0.3);
}
section[data-testid="stSidebar"] .sb-section-title {
    text-transform: uppercase; font-size: 0.72rem; letter-spacing: 0.9px;
    color: #64748b; font-weight: 800;
    margin: 1.05rem 0 0.45rem;
}
section[data-testid="stSidebar"] .sb-empty {
    color: #64748b; font-size: 0.85rem; padding: 0.3rem 0.1rem;
}
section[data-testid="stSidebar"] .sb-footer {
    font-size: 0.82rem; color: #475569; line-height: 1.75;
}
section[data-testid="stSidebar"] .sb-footer a {
    color: #1e3a8a; text-decoration: none; font-weight: 600;
}
section[data-testid="stSidebar"] .sb-footer a:hover {
    text-decoration: underline;
}
section[data-testid="stSidebar"] .stButton button:focus-visible {
    outline: 2px solid #6366f1 !important;
    outline-offset: 2px;
}

</style>
""",
    unsafe_allow_html=True,
)


# ── Content data ─────────────────────────────────────────────────────────────
SUGGESTED_PROMPTS = [
    {
        "title": "📦 Track an order",
        "body": "Where is my order? My order number is TN-100001.",
    },
    {
        "title": "🛠️ Laptop won't power on",
        "body": "My NovaBook XPS 15 won't turn on — no lights, no sound.",
    },
    {
        "title": "🔒 Check my warranty",
        "body": "Can you check my warranty status? My service tag is SVC-TAG-001.",
    },
    {
        "title": "🔋 Battery looks swollen",
        "body": "My laptop battery is bulging out — what should I do?",
    },
    {
        "title": "↩️ Start a return",
        "body": "I want to return my NovaBook Air 13 that I received yesterday.",
    },
    {
        "title": "📞 Talk to a human",
        "body": "Please escalate this to a human support agent.",
        "force_escalate": True,
    },
]

CATEGORY_QUICK_ACTIONS = {
    "📦 Orders & Shipping": [
        ("Track my order", "Where is my order TN-100001?", False),
        ("Start a return", "I want to return my NovaBook Air 13.", False),
        ("Update shipping address",
         "Can I change the shipping address on my latest order?", False),
    ],
    "🛠️ Device Help": [
        ("Won't turn on", "My NovaBook XPS 15 won't turn on at all.", False),
        ("Overheating", "My laptop is running very hot and the fan won't stop.", False),
        ("Display flickering", "My screen keeps flickering on the NovaBook Pro.", False),
        ("Wi-Fi problems", "My laptop can't stay connected to Wi-Fi.", False),
    ],
    "🔒 Warranty & Account": [
        ("Check warranty", "Check warranty for service tag SVC-TAG-001.", False),
        ("Extend warranty", "Can I extend the warranty on my NovaBook?", False),
        ("Product specs", "What are the specs of the NovaBook XPS 15?", False),
    ],
    "📞 Talk to a Human": [
        ("Escalate to agent", "Please escalate to a human support agent.", True),
    ],
}


# ── Session state ────────────────────────────────────────────────────────────
def init_session() -> None:
    defaults = {
        "orchestrator": None,
        "session_id": None,
        "messages": [],            # [{"role", "content", "meta"?}]
        "ticket_ids": [],
        "customer_id": "",
        "customer_name": "",
        "last_state": None,
        "pending_message": None,   # {"text", "force_escalate"} | None
        # Past sessions for the sidebar:
        # [{"session_id", "title", "started_at", "messages", "ticket_ids"}]
        "history_sessions": [],
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val
    if st.session_state.orchestrator is None:
        st.session_state.orchestrator = SupportOrchestrator()


init_session()


# ── Helpers ──────────────────────────────────────────────────────────────────
def _conversation_title(messages: Iterable[dict]) -> str:
    """Derive a short title from the first user message."""
    first = next((m["content"] for m in messages if m["role"] == "user"),
                 "New conversation")
    return first[:46] + ("…" if len(first) > 46 else "")


def _snapshot_current_to_history() -> None:
    """Save the current conversation into the sidebar history list."""
    if not st.session_state.messages or not st.session_state.session_id:
        return
    title = _conversation_title(st.session_state.messages)
    existing = next(
        (s for s in st.session_state.history_sessions
         if s["session_id"] == st.session_state.session_id),
        None,
    )
    snapshot = {
        "session_id": st.session_state.session_id,
        "title": title,
        "started_at": datetime.utcnow().isoformat(),
        "messages": list(st.session_state.messages),
        "ticket_ids": list(st.session_state.ticket_ids),
    }
    if existing:
        existing.update(snapshot)
    else:
        st.session_state.history_sessions.insert(0, snapshot)
    # Cap history at 12 most-recent sessions
    st.session_state.history_sessions = st.session_state.history_sessions[:12]


def start_new_conversation() -> None:
    """Snapshot then clear the active conversation."""
    _snapshot_current_to_history()
    st.session_state.messages = []
    st.session_state.session_id = None
    st.session_state.ticket_ids = []
    st.session_state.last_state = None


def load_history_session(session_id: str) -> None:
    """Switch the active chat to a previously-saved session."""
    _snapshot_current_to_history()
    for s in st.session_state.history_sessions:
        if s["session_id"] == session_id:
            st.session_state.session_id = s["session_id"]
            st.session_state.messages = list(s["messages"])
            st.session_state.ticket_ids = list(s.get("ticket_ids", []))
            st.session_state.last_state = None
            return


def process_message(user_input: str, force_escalate: bool = False) -> None:
    """Run a user message through the orchestrator and update state."""
    st.session_state.messages.append({"role": "user", "content": user_input})

    if not st.session_state.session_id:
        st.session_state.session_id = (
            st.session_state.orchestrator.start_session(
                customer_id=st.session_state.customer_id,
                customer_name=st.session_state.customer_name,
            )
        )

    history = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages[:-1]
    ]

    with st.spinner("TechNova AI is working on it…"):
        state = st.session_state.orchestrator.process_message(
            user_message=user_input,
            session_id=st.session_state.session_id,
            customer_id=st.session_state.customer_id,
            customer_name=st.session_state.customer_name,
            conversation_history=history,
            force_escalate=force_escalate,
        )

    st.session_state.last_state = state
    response = state.get(
        "final_response",
        "I'm sorry, I ran into an issue. Please try again.",
    )

    docs = state.get("retrieved_docs", [])
    sources = list({d.get("title", "Knowledge Base") for d in docs[:3]})

    if tid := state.get("ticket_id"):
        if tid not in st.session_state.ticket_ids:
            st.session_state.ticket_ids.append(tid)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "meta": {
            "confidence_score": state.get("confidence_score", 0),
            "confidence_label": state.get("confidence_label", "medium"),
            "intent": state.get("intent", ""),
            "sources": sources,
            "ticket_id": state.get("ticket_id"),
        },
    })
    _snapshot_current_to_history()


def queue_message(text: str, force_escalate: bool = False) -> None:
    """Defer a message until after the next rerun (used by buttons)."""
    st.session_state.pending_message = {
        "text": text,
        "force_escalate": force_escalate,
    }


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        f"<div class='sb-brand'>"
        f"<span class='logo'>{COMPANY_NAME[0]}</span>{COMPANY_NAME} Support"
        f"</div>",
        unsafe_allow_html=True,
    )

    if st.button("✚ New conversation",
                 use_container_width=True,
                 type="primary",
                 key="sb_new_chat"):
        start_new_conversation()
        st.rerun()

    # ── Profile (collapsed by default) ───────────────────────────────────
    with st.expander("👤 Your profile", expanded=False):
        cust_id = st.text_input(
            "Customer ID",
            value=st.session_state.customer_id,
            placeholder="CUST-001",
            key="cust_id_input",
        )
        cust_name = st.text_input(
            "Your name",
            value=st.session_state.customer_name,
            placeholder="Alice Johnson",
            key="cust_name_input",
        )
        if (cust_id != st.session_state.customer_id
                or cust_name != st.session_state.customer_name):
            st.session_state.customer_id = cust_id
            st.session_state.customer_name = cust_name

    # ── Help topics (grouped quick actions) ──────────────────────────────
    st.markdown("<div class='sb-section-title'>Help topics</div>",
                unsafe_allow_html=True)
    for cat, actions in CATEGORY_QUICK_ACTIONS.items():
        with st.expander(cat, expanded=cat.startswith("📦")):
            for label, message, force_esc in actions:
                if st.button(label,
                             key=f"qa_{cat}_{label}",
                             use_container_width=True):
                    queue_message(message, force_escalate=force_esc)
                    st.rerun()

    # ── Recent conversations ─────────────────────────────────────────────
    st.markdown(
        "<div class='sb-section-title'>Recent conversations</div>",
        unsafe_allow_html=True,
    )
    if not st.session_state.history_sessions and not st.session_state.messages:
        st.markdown(
            "<div class='sb-empty'>Your past chats will appear here.</div>",
            unsafe_allow_html=True,
        )
    else:
        # Make sure the active chat is in the list so it appears at the top
        _snapshot_current_to_history()
        active_id = st.session_state.session_id
        for s in st.session_state.history_sessions:
            is_active = s["session_id"] == active_id
            label = f"{'● ' if is_active else ''}{s['title']}"
            if st.button(label,
                         key=f"hist_{s['session_id']}",
                         use_container_width=True,
                         disabled=is_active):
                load_history_session(s["session_id"])
                st.rerun()

    # ── Footer ───────────────────────────────────────────────────────────
    st.divider()
    st.markdown(
        f"<div class='sb-footer'>"
        f"<div>📞 <strong>{SUPPORT_PHONE}</strong></div>"
        f"<div>✉️ <a href='mailto:{SUPPORT_EMAIL}'>{SUPPORT_EMAIL}</a></div>"
        f"<div><a href='http://localhost:8502' target='_blank'>"
        f"Open admin dashboard ↗</a></div>"
        f"</div>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# MAIN AREA
# ─────────────────────────────────────────────────────────────────────────────

# Process any quick-action prompt queued from the sidebar / prompt cards
# (must happen BEFORE we render the conversation so the new turn shows up).
if st.session_state.pending_message:
    pending = st.session_state.pending_message
    st.session_state.pending_message = None
    if isinstance(pending, dict):
        process_message(
            pending["text"],
            force_escalate=pending.get("force_escalate", False),
        )
    else:
        process_message(pending)
    st.rerun()


# ── Empty state: welcome + suggested prompts ────────────────────────────────
if not st.session_state.messages:
    cust_first = (st.session_state.customer_name.split(" ")[0]
                  if st.session_state.customer_name else "there")
    st.markdown(
        f"""
        <div class="welcome-hero">
          <div class="greet">Hi {cust_first} 👋 — how can I help today?</div>
          <div class="sub">
            Ask me about orders, devices, warranty, or returns.
            I can also connect you with a human agent.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='prompt-section-title'>Suggested prompts</div>",
        unsafe_allow_html=True,
    )

    # 3-column grid of suggestion cards (2 rows × 3 cols = 6 prompts)
    for row_start in (0, 3):
        cols = st.columns(3, gap="small")
        for offset, col in enumerate(cols):
            idx = row_start + offset
            if idx >= len(SUGGESTED_PROMPTS):
                continue
            p = SUGGESTED_PROMPTS[idx]
            with col:
                if st.button(
                    p["title"],
                    key=f"sp_{idx}",
                    use_container_width=True,
                    help=p["body"],
                ):
                    queue_message(p["body"],
                                  force_escalate=p.get("force_escalate", False))
                    st.rerun()

# ── Active conversation ────────────────────────────────────────────────────
else:
    for msg in st.session_state.messages:
        role = msg["role"]
        with st.chat_message(role, avatar="🧑" if role == "user" else "🤖"):
            st.markdown(msg["content"])

            if role != "assistant":
                continue

            meta = msg.get("meta") or {}
            conf = meta.get("confidence_score", 0)
            label = meta.get("confidence_label", "medium")
            sources = meta.get("sources") or []
            tid = meta.get("ticket_id")

            # Single, scannable meta row: confidence chip + source pills
            meta_html = (
                "<div class='meta-row'>"
                f"<span class='confidence-badge badge-{label}'>"
                f"Confidence {conf:.0%}</span>"
            )
            if sources:
                pills = "".join(
                    f"<span class='source-pill'>📄 {s}</span>"
                    for s in sources[:3]
                )
                meta_html += (
                    f"<span class='meta-label'>Sources:</span>{pills}"
                )
            meta_html += "</div>"
            st.markdown(meta_html, unsafe_allow_html=True)

            if tid:
                st.markdown(
                    f"<div class='ticket-banner'>🎫 "
                    f"<strong>Ticket created:</strong> <code>{tid}</code> — "
                    f"a human agent will follow up shortly.</div>",
                    unsafe_allow_html=True,
                )

    # Persistent escalation chip above the (sticky) chat input
    st.markdown("<div class='escalate-bar'>", unsafe_allow_html=True)
    if st.button("🚨 Talk to a human", key="inline_escalate"):
        process_message(
            "Please escalate this to a human support agent immediately.",
            force_escalate=True,
        )
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


# ── Chat input (auto-pinned by Streamlit, styled by our CSS) ────────────────
user_input = st.chat_input(
    "Ask about an order, device, warranty… "
    "(e.g. 'Where is order TN-100001?')",
)
if user_input:
    process_message(user_input)
    st.rerun()
