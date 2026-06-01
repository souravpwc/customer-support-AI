"""
Shared UI theme for TechNova Support apps.

Both the customer chat (``app.py``) and the admin dashboard (``admin.py``)
call :func:`apply_theme` so the two surfaces stay visually identical and
every text element has accessible (WCAG-AA) contrast on its background.

Add new tokens / rules here — not in the individual apps — so the two
dashboards never drift apart again.
"""
from __future__ import annotations
import streamlit as st


# ── Design tokens (single source of truth) ────────────────────────────────────
APP_BG          = "#f5f7fb"
SURFACE         = "#ffffff"
SURFACE_ALT     = "#f8fafc"
TEXT_PRIMARY    = "#1f2937"   # body copy
TEXT_HEADING    = "#0f172a"   # headings / strong emphasis
TEXT_MUTED      = "#475569"   # captions, meta — darker than Streamlit default
BORDER          = "#e2e8f0"
BORDER_STRONG   = "#cbd5e1"

BRAND_GRADIENT  = "linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)"
BRAND_ACCENT    = "#ff8fa3"
BRAND_BLUE      = "#1d4ed8"

# Priority palette (used in both apps so chips look identical)
PRIO_CRIT   = "#dc2626"
PRIO_HIGH   = "#ea580c"
PRIO_MED    = "#b45309"
PRIO_LOW    = "#15803d"


def _shared_css() -> str:
    """The base stylesheet applied to both apps."""
    return f"""
<style>
/* ─── App surface & base typography ──────────────────────────────────── */
.stApp, [data-testid="stAppViewContainer"] {{
    background-color: {APP_BG} !important;
    color: {TEXT_PRIMARY} !important;
}}
.main .block-container {{
    padding-top: 1.4rem;
    padding-bottom: 4rem;
    color: {TEXT_PRIMARY};
}}
.main, .main p, .main li, .main span, .main label, .main div {{
    color: {TEXT_PRIMARY};
}}
h1, h2, h3, h4, h5 {{ color: {TEXT_HEADING}; }}

/* ─── Kill Streamlit's dark top toolbar & dark bottom container ────── */
/* Top toolbar (where the hamburger menu / "Deploy" button live) */
[data-testid="stHeader"],
header[data-testid="stHeader"] {{
    background: transparent !important;
    background-color: transparent !important;
    box-shadow: none !important;
    border-bottom: none !important;
    height: 0 !important;
}}
[data-testid="stToolbar"] {{
    background: transparent !important;
}}
/* The light "running" status indicator */
[data-testid="stStatusWidget"] {{
    background: transparent !important;
}}

/* Bottom container that wraps st.chat_input — Streamlit fills it dark
   in some versions. Force the app surface colour so the input visually
   sits on the page instead of a dark slab. */
[data-testid="stBottom"],
[data-testid="stBottomBlockContainer"],
section[data-testid="stBottom"] {{
    background: {APP_BG} !important;
    background-color: {APP_BG} !important;
    border-top: none !important;
    box-shadow: none !important;
}}
[data-testid="stBottom"] > div,
section[data-testid="stBottom"] > div {{
    background: {APP_BG} !important;
    background-color: {APP_BG} !important;
}}

/* ─── Unified app header (used by both dashboards) ───────────────────── */
.app-header {{
    background: {BRAND_GRADIENT};
    padding: 1.6rem 2rem;
    border-radius: 14px;
    margin-bottom: 1.2rem;
    color: #ffffff;
    box-shadow: 0 4px 14px rgba(15, 52, 96, 0.18);
}}
.app-header h1 {{
    color: {BRAND_ACCENT};
    margin: 0;
    font-size: 1.95rem;
    letter-spacing: 0.2px;
}}
.app-header p {{
    color: #ffffff;
    margin: 0.35rem 0 0;
    font-size: 0.98rem;
    opacity: 0.92;
}}

/* ─── KPI cards (admin) ──────────────────────────────────────────────── */
.kpi-card {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 1.1rem 1.2rem;
    text-align: center;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}}
.kpi-card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}}
.kpi-card .kpi-value {{
    font-size: 2.1rem;
    font-weight: 800;
    color: {TEXT_HEADING};
    line-height: 1.1;
}}
.kpi-card .kpi-label {{
    font-size: 0.88rem;
    color: {TEXT_MUTED};
    margin-top: 0.35rem;
    font-weight: 600;
}}
.kpi-card .kpi-delta {{
    font-size: 0.82rem;
    margin-top: 0.3rem;
    color: {TEXT_MUTED};
    font-weight: 500;
}}

/* ─── Status / priority chips (shared) ───────────────────────────────── */
.escalation-badge, .resolved-badge, .open-badge, .confidence-badge {{
    display: inline-block;
    padding: 4px 12px;
    border-radius: 14px;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.2px;
    border: 1px solid transparent;
}}
.escalation-badge {{ background: #fee2e2; color: #7f1d1d; border-color: #fca5a5; }}
.resolved-badge   {{ background: #d1fae5; color: #065f46; border-color: #6ee7b7; }}
.open-badge       {{ background: #dbeafe; color: #1e3a8a; border-color: #93c5fd; }}
.badge-high          {{ background: #d1fae5; color: #065f46; border-color: #6ee7b7; }}
.badge-medium        {{ background: #dbeafe; color: #1e3a8a; border-color: #93c5fd; }}
.badge-low           {{ background: #fef3c7; color: #78350f; border-color: #fcd34d; }}
.badge-critical_low  {{ background: #fee2e2; color: #7f1d1d; border-color: #fca5a5; }}

.priority-critical {{ color: {PRIO_CRIT}; font-weight: 800; }}
.priority-high     {{ color: {PRIO_HIGH}; font-weight: 700; }}
.priority-medium   {{ color: {PRIO_MED};  font-weight: 700; }}
.priority-low      {{ color: {PRIO_LOW};  font-weight: 700; }}

/* ─── Source pills (customer chat) ───────────────────────────────────── */
.source-pill {{
    display: inline-block;
    background: {SURFACE};
    border: 1px solid {BORDER_STRONG};
    padding: 3px 11px;
    border-radius: 12px;
    font-size: 0.8rem;
    margin-right: 6px;
    margin-top: 2px;
    color: {TEXT_PRIMARY};
    font-weight: 500;
}}

/* ─── Welcome card (customer) ────────────────────────────────────────── */
.welcome-card {{
    background: {SURFACE};
    border: 1px solid {BORDER_STRONG};
    border-radius: 12px;
    padding: 1.3rem 1.5rem;
    margin: 0.4rem 0 1.2rem 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    color: {TEXT_PRIMARY};
}}
.welcome-card h3 {{
    margin: 0 0 0.7rem 0;
    font-size: 1.2rem;
    color: {TEXT_HEADING};
    font-weight: 700;
}}
.welcome-card p, .welcome-card li {{
    color: {TEXT_PRIMARY};
    font-size: 1rem;
    line-height: 1.7;
}}
.welcome-card strong {{ color: {TEXT_HEADING}; }}
.welcome-card ul {{ margin: 0.2rem 0 0.6rem 1.2rem; }}
.welcome-card .hint {{
    color: #334155;
    background: #eef2ff;
    border-left: 3px solid #4f46e5;
    padding: 0.55rem 0.8rem;
    border-radius: 0 8px 8px 0;
    font-size: 0.92rem;
    margin-top: 0.6rem;
}}
.welcome-card .hint strong {{ color: #1e1b4b; }}

/* ─── Ticket banner (customer) ───────────────────────────────────────── */
.ticket-banner {{
    background: #e0ecff;
    border-left: 5px solid {BRAND_BLUE};
    padding: 0.9rem 1.1rem;
    border-radius: 0 10px 10px 0;
    margin: 0.6rem 0;
    font-size: 1rem;
    color: {TEXT_HEADING};
}}
.ticket-banner strong {{ color: {TEXT_HEADING}; }}
.ticket-banner code {{
    background: {SURFACE};
    padding: 2px 10px;
    border-radius: 6px;
    color: {BRAND_BLUE};
    font-weight: 800;
    border: 1px solid #c7d8f5;
}}

/* ─── Escalation card (admin) — readable troubleshooting tips ────────── */
.escalation-card {{
    background: {SURFACE};
    border: 1px solid #f1c5c7;
    border-left: 6px solid {PRIO_CRIT};
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.6rem;
    box-shadow: 0 1px 4px rgba(220, 53, 69, 0.08);
    color: {TEXT_PRIMARY};
}}
.escalation-card.high     {{ border-left-color: {PRIO_HIGH}; border-color: #ffd7b3; }}
.escalation-card.medium   {{ border-left-color: {PRIO_MED};  border-color: #fde68a; }}
.escalation-card.low      {{ border-left-color: {PRIO_LOW};  border-color: #bbf7d0; }}

/* Every text node inside the card must be readable on white */
.escalation-card,
.escalation-card * {{
    color: {TEXT_PRIMARY};
}}
.escalation-card .meta {{
    color: {TEXT_MUTED};
    font-size: 0.9rem;
    line-height: 1.55;
}}
.escalation-card .meta code {{
    background: #eef2ff;
    color: #1e1b4b;
    padding: 1px 7px;
    border-radius: 5px;
    font-weight: 600;
    border: 1px solid #c7d2fe;
}}
.escalation-card .subject {{
    font-size: 1.05rem;
    font-weight: 700;
    color: {TEXT_HEADING};
    margin: 0.25rem 0 0.45rem 0;
}}
/* The troubleshooting / description text block — HIGH-contrast dark text */
.escalation-card pre {{
    background: #f1f5f9;
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 0.75rem 0.9rem;
    font-size: 0.92rem;
    line-height: 1.55;
    white-space: pre-wrap;
    word-wrap: break-word;
    color: {TEXT_HEADING} !important;
    font-weight: 500;
    font-family: 'Segoe UI', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}}
.escalation-card pre strong, .escalation-card pre b {{
    color: {TEXT_HEADING} !important;
    font-weight: 700;
}}

/* ─── Streamlit primitives: force readable contrast ──────────────────── */
/* Captions everywhere */
[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p,
.stCaption {{
    color: {TEXT_MUTED} !important;
    opacity: 1 !important;
    font-size: 0.9rem;
}}

/* Expander — clean light card with dark, readable header text */
[data-testid="stExpander"] {{
    background: {SURFACE} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 10px !important;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
    margin-bottom: 0.5rem;
}}
[data-testid="stExpander"] summary,
[data-testid="stExpander"] details summary,
.streamlit-expanderHeader {{
    background: {SURFACE} !important;
    color: {TEXT_HEADING} !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    border-radius: 10px !important;
    padding: 0.55rem 0.85rem !important;
}}
[data-testid="stExpander"] summary:hover {{
    background: #f1f5f9 !important;
}}
[data-testid="stExpander"] [data-testid="stExpanderDetails"] {{
    background: {SURFACE} !important;
    border-top: 1px solid {BORDER};
    padding: 0.55rem 0.85rem !important;
}}
[data-testid="stExpander"] p,
[data-testid="stExpander"] li,
[data-testid="stExpander"] span,
[data-testid="stExpander"] label {{
    color: {TEXT_PRIMARY} !important;
}}

/* Inputs / text areas / selects */
input, textarea, select,
.stTextInput input, .stTextArea textarea, .stSelectbox div[role="button"] {{
    background-color: {SURFACE} !important;
    color: {TEXT_HEADING} !important;
    border: 1px solid {BORDER_STRONG} !important;
}}
input::placeholder, textarea::placeholder {{
    color: #94a3b8 !important;
    opacity: 1;
}}

/* Buttons (primary surface) */
.stButton button {{
    color: {TEXT_PRIMARY} !important;
    background-color: {SURFACE} !important;
    border: 1px solid {BORDER_STRONG} !important;
    font-weight: 500;
}}
.stButton button:hover {{
    background-color: #eef2ff !important;
    border-color: #6366f1 !important;
    color: #1e1b4b !important;
}}
.stButton button[kind="primary"] {{
    background-color: {BRAND_BLUE} !important;
    color: #ffffff !important;
    border-color: {BRAND_BLUE} !important;
}}
.stButton button[kind="primary"]:hover {{
    background-color: #1e40af !important;
    border-color: #1e40af !important;
    color: #ffffff !important;
}}

/* Tabs */
[data-baseweb="tab-list"] {{ gap: 0.25rem; }}
[data-baseweb="tab"] {{
    color: {TEXT_MUTED} !important;
    font-weight: 600;
}}
[data-baseweb="tab"][aria-selected="true"] {{
    color: {TEXT_HEADING} !important;
}}

/* Sidebar */
section[data-testid="stSidebar"] {{
    background-color: {SURFACE_ALT} !important;
}}
section[data-testid="stSidebar"] * {{
    color: {TEXT_PRIMARY};
}}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {{
    color: {TEXT_HEADING} !important;
}}
section[data-testid="stSidebar"] .stButton button {{
    text-align: left;
    font-size: 0.93rem;
}}
section[data-testid="stSidebar"] [data-testid="stCodeBlock"],
section[data-testid="stSidebar"] code {{
    background: #e2e8f0 !important;
    color: {TEXT_HEADING} !important;
}}

/* ─── Chat messages (customer) ───────────────────────────────────────── */
[data-testid="stChatMessage"] {{
    background-color: {SURFACE} !important;
    color: {TEXT_PRIMARY} !important;
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 0.8rem 1rem !important;
    margin-bottom: 0.6rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}}
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] span,
[data-testid="stChatMessage"] strong,
[data-testid="stChatMessage"] em {{
    color: {TEXT_PRIMARY} !important;
    font-size: 1.02rem;
    line-height: 1.65;
}}
[data-testid="stChatMessage"] code {{
    background: #f1f5f9 !important;
    color: {TEXT_HEADING} !important;
    padding: 1px 6px;
    border-radius: 4px;
    font-size: 0.92em;
}}
[data-testid="stChatMessage"] small {{
    color: {TEXT_MUTED} !important;
    font-size: 0.85rem;
}}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {{
    background-color: #eef4ff !important;
    border-color: #c7d8f5;
}}

/* Chat input — clean light card that visually belongs to the page */
[data-testid="stChatInput"] {{
    background: {APP_BG} !important;
    background-color: {APP_BG} !important;
}}
[data-testid="stChatInput"] > div {{
    background: {SURFACE} !important;
    background-color: {SURFACE} !important;
    border: 1px solid {BORDER_STRONG} !important;
    border-radius: 14px !important;
    box-shadow: 0 2px 10px rgba(15, 23, 42, 0.06) !important;
}}
[data-testid="stChatInput"] textarea {{
    background-color: {SURFACE} !important;
    color: {TEXT_HEADING} !important;
    font-size: 1rem !important;
    border: none !important;
    box-shadow: none !important;
}}
[data-testid="stChatInput"] textarea:focus {{
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
}}
[data-testid="stChatInput"] textarea::placeholder {{
    color: #64748b !important;
    opacity: 1;
}}
/* Send button inside the chat input */
[data-testid="stChatInput"] button {{
    background: {BRAND_BLUE} !important;
    color: #ffffff !important;
    border: none !important;
}}
[data-testid="stChatInput"] button:hover {{
    background: #1e40af !important;
}}
[data-testid="stChatInput"] button:disabled {{
    background: #cbd5e1 !important;
    color: #ffffff !important;
}}
</style>
"""


def apply_theme(variant: str = "customer") -> None:
    """Inject the shared theme.

    Args:
        variant: "customer" or "admin". Kept as a hook for tiny per-app
                 tweaks in the future, but the visual language is identical.
    """
    st.markdown(_shared_css(), unsafe_allow_html=True)


def render_header(title: str, subtitle: str) -> None:
    """Render the unified app header used by both dashboards."""
    st.markdown(
        f"""<div class="app-header">
        <h1>{title}</h1>
        <p>{subtitle}</p>
        </div>""",
        unsafe_allow_html=True,
    )
