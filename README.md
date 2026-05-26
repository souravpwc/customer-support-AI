# TechNova Customer Support Assistant

A fully-agentic, multi-layer AI support system built with LangGraph, OpenAI, and Streamlit.

---

## Architecture

```
Customer Chat (app.py)
        │
        ▼
 SupportOrchestrator  ←── LangGraph StateGraph
        │
   ┌────┴────────────────────────────────────────────┐
   │                   Agent Pipeline                │
   │                                                 │
   │  classify → retrieve → integrate → generate      │
   │       ↘          ↓                    ↓         │
   │      (order)  troubleshoot        escalate       │
   │                                    ↓            │
   │                               summarize → END   │
   └─────────────────────────────────────────────────┘
        │                    │
   Knowledge Base        Mock APIs
   (407 doc chunks)   order/warranty/ticket/CRM/repair
        │
   Hybrid Retriever
   (Vector + TF-IDF)
        │
   Governance Layer
   audit / masker / guardrails / confidence
        │
   Admin Dashboard (admin.py)
```

---

## Components

| Layer | Module | Description |
|---|---|---|
| **Agents** | `agents/orchestrator.py` | LangGraph workflow — routes all 8 agent nodes |
| | `agents/classifier.py` | Intent classification (7 intents) |
| | `agents/retriever.py` | Hybrid KB retrieval |
| | `agents/integrator.py` | Mock API orchestration |
| | `agents/troubleshooter.py` | Structured diagnostic steps |
| | `agents/response_generator.py` | GPT-4o-mini response + guardrails |
| | `agents/summarizer.py` | Conversation summarization |
| | `agents/escalation.py` | Ticket creation + human handoff |
| **Retrieval** | `retrieval/vector_store.py` | OpenAI embeddings + cosine similarity |
| | `retrieval/keyword_search.py` | TF-IDF keyword search |
| | `retrieval/hybrid_retriever.py` | RRF fusion of vector + keyword |
| **Integrations** | `integrations/order_api.py` | Mock order management |
| | `integrations/warranty_api.py` | Mock warranty lookup |
| | `integrations/ticket_api.py` | Help-desk ticket creation |
| | `integrations/crm_api.py` | Customer profile / tier lookup |
| | `integrations/repair_api.py` | Repair appointment scheduling |
| **Governance** | `governance/audit_logger.py` | Append-only JSONL audit log |
| | `governance/data_masker.py` | PII regex masking (email, phone, SSN, CC) |
| | `governance/guardrails.py` | Response safety checks |
| | `governance/confidence_scorer.py` | 0-1 quality scoring |
| **Evaluation** | `evaluation/metrics.py` | FCR, escalation rate, confidence dist. |
| | `evaluation/scenarios.json` | 10 sample workflow scenarios |
| **UI** | `app.py` | Customer Streamlit chat |
| | `admin.py` | Admin dashboard (port 8502) |

---

## Quick Start

### 1. Environment Setup
```bash
# .env is already populated with OPENAI_API_KEY
# Activate virtual environment
.venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch Customer Chat
```bash
streamlit run app.py
# Opens at http://localhost:8501
```

### 4. Launch Admin Dashboard (separate terminal)
```bash
streamlit run admin.py --server.port 8502
# Opens at http://localhost:8502
```

---

## Sample Workflows

| Scenario | Steps |
|---|---|
| **Order Tracking** | Type "Where is order TN-100001?" → integrate_order → response with shipping info |
| **Warranty Check** | Type "Check warranty SVC-TAG-001" → integrate_warranty → active/expired status |
| **Laptop Troubleshooting** | "My NovaBook won't turn on" → classify → retrieve KB → troubleshoot → steps |
| **Battery Safety** | "Battery is swollen" → safety escalation → ticket created → human handoff |
| **Expired Warranty** | "SVC-TAG-003" (expired) → warranty API → out-of-warranty repair options |
| **Escalation** | "Talk to a human" → escalate → ticket TKT-XXXXX created → response |

---

## Knowledge Base
- **407 document chunks** across 5 categories
- `knowledge_base/manuals/` — 19 product manuals
- `knowledge_base/troubleshooting/` — 8 diagnostic guides
- `knowledge_base/warranty/` — warranty policy
- `knowledge_base/returns/` — return policy
- `knowledge_base/faqs/` — general FAQs

## Governance Features
- **Audit Logs**: Every event logged to `data/audit_logs.jsonl`
- **PII Masking**: Email, phone, SSN, credit cards auto-masked
- **Confidence Scoring**: 4-level (high/medium/low/critical_low)
- **Guardrails**: Length cap, human impersonation, topic blocking, URL validation
- **Human-in-the-loop**: Auto-escalation when confidence < 40%

## Evaluation Metrics
- First Contact Resolution (FCR) Rate
- Escalation Rate
- Average Confidence Score
- Retrieval Quality (top score, docs per query)
- Guardrail trigger counts
- Intent distribution
