"""
TechNova Customer Support Chat — Customer-facing Streamlit application.
Run with: streamlit run app.py
"""
import streamlit as st
import json
from datetime import datetime

from config import APP_TITLE, COMPANY_NAME, SUPPORT_EMAIL, SUPPORT_PHONE
from agents.orchestrator import SupportOrchestrator

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.main-header {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    padding: 1.5rem 2rem;
    border-radius: 12px;
    margin-bottom: 1rem;
    color: white;
}
.main-header h1 { color: #e94560; margin: 0; font-size: 1.8rem; }
.main-header p { color: #a8b2d8; margin: 0.2rem 0 0; font-size: 0.9rem; }

.confidence-badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 600;
}
.badge-high    { background: #d4edda; color: #155724; }
.badge-medium  { background: #cce5ff; color: #004085; }
.badge-low     { background: #fff3cd; color: #856404; }
.badge-critical_low { background: #f8d7da; color: #721c24; }

.ticket-banner {
    background: #f0f7ff;
    border-left: 4px solid #0d6efd;
    padding: 0.75rem 1rem;
    border-radius: 0 8px 8px 0;
    margin: 0.5rem 0;
}
.quick-action-btn {
    width: 100%;
    margin-bottom: 0.25rem;
}
.source-pill {
    display: inline-block;
    background: #f1f3f5;
    border: 1px solid #dee2e6;
    padding: 1px 8px;
    border-radius: 10px;
    font-size: 0.7rem;
    margin-right: 4px;
    color: #495057;
}
</style>
""", unsafe_allow_html=True)


# ── Session state init ─────────────────────────────────────────────────────────
def init_session():
    if "orchestrator" not in st.session_state:
        st.session_state.orchestrator = SupportOrchestrator()
    if "session_id" not in st.session_state:
        st.session_state.session_id = None
    if "messages" not in st.session_state:
        # messages = [{role, content, meta}]
        st.session_state.messages = []
    if "ticket_ids" not in st.session_state:
        st.session_state.ticket_ids = []
    if "customer_id" not in st.session_state:
        st.session_state.customer_id = ""
    if "customer_name" not in st.session_state:
        st.session_state.customer_name = ""
    if "last_state" not in st.session_state:
        st.session_state.last_state = None
    if "pending_message" not in st.session_state:
        st.session_state.pending_message = None


init_session()


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 👤 Your Profile")
    cust_id = st.text_input("Customer ID (optional)", value=st.session_state.customer_id,
                             placeholder="CUST-001", key="cust_id_input")
    cust_name = st.text_input("Your Name (optional)", value=st.session_state.customer_name,
                               placeholder="Alice Johnson", key="cust_name_input")
    if cust_id != st.session_state.customer_id or cust_name != st.session_state.customer_name:
        st.session_state.customer_id = cust_id
        st.session_state.customer_name = cust_name

    st.divider()
    st.markdown("## ⚡ Quick Actions")

    quick_actions = [
        ("📦 Track My Order", "Where is my order? My order number is TN-100001"),
        ("🔒 Check Warranty", "Can you check my warranty status? My service tag is SVC-TAG-001"),
        ("🛠️ Laptop Won't Turn On", "My NovaBook XPS 15 won't turn on at all. No lights, no sound."),
        ("🔋 Battery Problem", "My laptop battery looks swollen and is bulging out. What should I do?"),
        ("↩️ Return a Product", "I want to return my NovaBook Air 13 that I received yesterday."),
        ("📞 Talk to a Human", "Please escalate this to a human agent."),
    ]
    for label, message in quick_actions:
        if st.button(label, key=f"qa_{label}", use_container_width=True):
            st.session_state.pending_message = message

    st.divider()

    # Session info
    st.markdown("## ℹ️ Session Info")
    if st.session_state.session_id:
        st.code(f"Session: {st.session_state.session_id[:8]}…", language=None)
    if st.session_state.ticket_ids:
        st.markdown("**Open Tickets:**")
        for tid in st.session_state.ticket_ids:
            st.markdown(f"🎫 `{tid}`")

    # Last response meta
    if ls := st.session_state.last_state:
        st.divider()
        st.markdown("**Last Response Quality**")
        conf = ls.get("confidence_score", 0)
        label = ls.get("confidence_label", "medium")
        color_map = {"high": "green", "medium": "blue", "low": "orange", "critical_low": "red"}
        st.markdown(
            f"<span class='confidence-badge badge-{label}'>"
            f"Confidence: {conf:.0%} ({label})</span>",
            unsafe_allow_html=True,
        )
        if ls.get("intent"):
            st.caption(f"Intent: `{ls['intent']}`")

    st.divider()
    if st.button("🗑️ New Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.session_id = None
        st.session_state.ticket_ids = []
        st.session_state.last_state = None
        st.rerun()

    st.markdown("---")
    st.caption(f"📞 {SUPPORT_PHONE}")
    st.caption(f"✉️ {SUPPORT_EMAIL}")
    st.caption("[Admin Dashboard →](http://localhost:8502)", unsafe_allow_html=True)


# ── Main chat area ─────────────────────────────────────────────────────────────
st.markdown(
    f"""<div class="main-header">
    <h1>🖥️ {COMPANY_NAME} Support Assistant</h1>
    <p>AI-powered support · Available 24/7 · Backed by human agents when you need them</p>
    </div>""",
    unsafe_allow_html=True,
)

# Welcome message
if not st.session_state.messages:
    st.markdown("""
    👋 **Welcome to TechNova Support!**

    I can help you with:
    - 📦 **Order tracking** — Check status of any order
    - 🔒 **Warranty** — Verify coverage and file claims
    - 🛠️ **Troubleshooting** — Step-by-step device support
    - ↩️ **Returns & refunds** — Process returns easily
    - 📋 **Product info** — Specs, manuals, comparisons

    *Use the Quick Actions in the sidebar, or type your question below.*
    """)

# Display conversation history
for msg in st.session_state.messages:
    role = msg["role"]
    with st.chat_message(role, avatar="🧑" if role == "user" else "🤖"):
        st.markdown(msg["content"])

        # Show metadata for assistant messages
        if role == "assistant" and (meta := msg.get("meta")):
            cols = st.columns([3, 1])
            with cols[0]:
                # Source citations
                sources = meta.get("sources", [])
                if sources:
                    source_html = "".join(
                        f"<span class='source-pill'>📄 {s}</span>" for s in sources[:3]
                    )
                    st.markdown(f"<small>Sources: {source_html}</small>", unsafe_allow_html=True)
            with cols[1]:
                conf_label = meta.get("confidence_label", "medium")
                conf_score = meta.get("confidence_score", 0)
                st.markdown(
                    f"<span class='confidence-badge badge-{conf_label}'>"
                    f"{conf_score:.0%}</span>",
                    unsafe_allow_html=True,
                )

            # Ticket banner
            if tid := meta.get("ticket_id"):
                st.markdown(
                    f"<div class='ticket-banner'>🎫 <strong>Ticket Created:</strong> "
                    f"<code>{tid}</code> — A human agent will follow up shortly.</div>",
                    unsafe_allow_html=True,
                )


# ── Message processing ─────────────────────────────────────────────────────────
def process_message(user_input: str):
    """Run user input through the orchestrator and update session."""
    # Display user message immediately
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Init session if new
    if not st.session_state.session_id:
        st.session_state.session_id = st.session_state.orchestrator.start_session(
            customer_id=st.session_state.customer_id,
            customer_name=st.session_state.customer_name,
        )

    # Build conversation history for context
    history = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages[:-1]  # Exclude the current message
    ]

    # Run through agent pipeline
    with st.spinner("TechNova AI is thinking…"):
        state = st.session_state.orchestrator.process_message(
            user_message=user_input,
            session_id=st.session_state.session_id,
            customer_id=st.session_state.customer_id,
            customer_name=st.session_state.customer_name,
            conversation_history=history,
        )

    st.session_state.last_state = state
    response = state.get("final_response", "I'm sorry, I encountered an issue. Please try again.")

    # Gather sources from retrieved docs
    docs = state.get("retrieved_docs", [])
    sources = list({d.get("title", "KB") for d in docs[:3]})

    # Track ticket IDs
    if tid := state.get("ticket_id"):
        if tid not in st.session_state.ticket_ids:
            st.session_state.ticket_ids.append(tid)

    # Append assistant response
    meta = {
        "confidence_score": state.get("confidence_score", 0),
        "confidence_label": state.get("confidence_label", "medium"),
        "intent": state.get("intent", ""),
        "sources": sources,
        "ticket_id": state.get("ticket_id"),
        "needs_review": state.get("needs_review", False),
    }
    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "meta": meta,
    })


# ── Handle pending quick-action messages ──────────────────────────────────────
if st.session_state.pending_message:
    msg = st.session_state.pending_message
    st.session_state.pending_message = None
    process_message(msg)
    st.rerun()

# ── Chat input ─────────────────────────────────────────────────────────────────
user_input = st.chat_input("Type your question here… (e.g. 'Where is my order TN-100001?')")
if user_input:
    process_message(user_input)
    st.rerun()

# ── Escalation quick button ────────────────────────────────────────────────────
if st.session_state.messages:
    with st.expander("Need urgent help?", expanded=False):
        st.markdown(
            "If the AI hasn't resolved your issue, you can request immediate human assistance."
        )
        if st.button("🚨 Escalate to Human Agent", type="primary"):
            process_message("Please escalate this to a human support agent immediately.")
            st.rerun()
