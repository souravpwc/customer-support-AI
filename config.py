"""Central configuration for TechNova Support Assistant."""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
KB_DIR = BASE_DIR / "knowledge_base"
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# ── OpenAI ────────────────────────────────────────────────────────────────────
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
LLM_MODEL = "gpt-4o-mini"
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSIONS = 1536

# ── Agent Thresholds ──────────────────────────────────────────────────────────
MAX_RETRIEVED_DOCS = 5
CONFIDENCE_THRESHOLD = 0.65       # below → flag for review
ESCALATION_THRESHOLD = 0.40       # below → auto-escalate
MAX_CONVERSATION_TURNS = 20

# ── Intent Labels ─────────────────────────────────────────────────────────────
INTENTS = [
    "order_status",
    "warranty_check",
    "troubleshooting",
    "return_refund",
    "product_info",
    "escalation_request",
    "general_faq",
]

INTENT_DESCRIPTIONS = {
    "order_status":       "Checking order status, tracking, delivery, shipping info",
    "warranty_check":     "Warranty validity, coverage, claims, service tags",
    "troubleshooting":    "Device not working, errors, bugs, hardware/software issues",
    "return_refund":      "Returns, refunds, exchanges, cancellations",
    "product_info":       "Product specs, features, comparisons, manuals",
    "escalation_request": "Customer explicitly requesting human agent or escalation",
    "general_faq":        "General questions, policies, contact info, account help",
}

# ── Branding ──────────────────────────────────────────────────────────────────
COMPANY_NAME = "TechNova"
APP_TITLE = "TechNova Support Assistant"
ADMIN_TITLE = "TechNova Support Dashboard"
SUPPORT_EMAIL = "support@technova.com"
SUPPORT_PHONE = "1-800-TECHNOVA"

# ── Governance ────────────────────────────────────────────────────────────────
AUDIT_LOG_FILE = DATA_DIR / "audit_logs.jsonl"
TICKETS_FILE = DATA_DIR / "tickets.json"
CONVERSATIONS_FILE = DATA_DIR / "conversations.json"
EMBEDDINGS_CACHE = DATA_DIR / "embeddings_cache.pkl"

# ── Response Guardrails ───────────────────────────────────────────────────────
BLOCKED_TOPICS = [
    "competitor pricing", "internal pricing tools", "employee data",
    "legal advice", "medical advice",
]
MAX_RESPONSE_LENGTH = 1200  # characters

# ── Evaluation ────────────────────────────────────────────────────────────────
EVAL_SCENARIOS_FILE = BASE_DIR / "evaluation" / "scenarios.json"
