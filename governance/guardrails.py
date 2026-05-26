"""Response guardrails — topic blocking, length enforcement, tone checks."""
from __future__ import annotations
import re
from dataclasses import dataclass, field
from typing import List

from config import BLOCKED_TOPICS, MAX_RESPONSE_LENGTH, COMPANY_NAME


@dataclass
class GuardrailResult:
    passed: bool
    violations: List[str] = field(default_factory=list)
    sanitized_response: str = ""
    action: str = "allow"  # allow | warn | block


# Phrases that suggest the bot is claiming to be human
_HUMAN_CLAIM_RE = re.compile(
    r"\b(I am a human|I'm a human|I am not an AI|I'm not an AI|as a person)\b",
    re.IGNORECASE,
)

# Competitor names — should not be endorsed/compared
_COMPETITOR_RE = re.compile(
    r"\b(Apple|Dell|HP|Lenovo|Microsoft Surface|Asus|Acer|Samsung Laptop)\b",
    re.IGNORECASE,
)

# Legal/financial disclaimers that the bot should not give
_LEGAL_FINANCE_RE = re.compile(
    r"\b(legal advice|financial advice|medical advice|you should sue|file a lawsuit)\b",
    re.IGNORECASE,
)

# Hallucination guard: any made-up phone numbers or URLs not from TechNova
_FAKE_URL_RE = re.compile(
    r"https?://(?!(?:support\.technova\.com|technova\.com|www\.technova\.com))\S+",
    re.IGNORECASE,
)


class Guardrails:
    """Validates AI-generated responses before delivery."""

    def check(self, response: str, intent: str = "") -> GuardrailResult:
        violations: List[str] = []
        sanitized = response

        # 1. Length cap
        if len(response) > MAX_RESPONSE_LENGTH:
            sanitized = response[:MAX_RESPONSE_LENGTH].rsplit(" ", 1)[0] + "…"
            violations.append(f"response_too_long ({len(response)} chars)")

        # 2. Human impersonation
        if _HUMAN_CLAIM_RE.search(sanitized):
            sanitized = _HUMAN_CLAIM_RE.sub(f"I am the {COMPANY_NAME} AI Support Assistant", sanitized)
            violations.append("human_impersonation")

        # 3. Blocked topics
        for topic in BLOCKED_TOPICS:
            if topic.lower() in sanitized.lower():
                violations.append(f"blocked_topic:{topic}")
                sanitized = re.sub(
                    re.escape(topic), "[information not available]", sanitized, flags=re.IGNORECASE
                )

        # 4. Legal / financial advice
        if _LEGAL_FINANCE_RE.search(sanitized):
            violations.append("legal_financial_advice")
            sanitized = (
                sanitized
                + "\n\n*Note: For legal or financial matters, please consult a qualified professional.*"
            )

        # 5. Fabricated URLs
        fake_urls = _FAKE_URL_RE.findall(sanitized)
        if fake_urls:
            for url in fake_urls:
                sanitized = sanitized.replace(url, "[URL removed]")
            violations.append(f"fabricated_urls:{fake_urls}")

        # 6. Competitor brand endorsement
        if _COMPETITOR_RE.search(sanitized):
            violations.append("competitor_mention")

        passed = len([v for v in violations if "response_too_long" not in v and "competitor_mention" not in v]) == 0
        action = "allow" if passed else ("warn" if len(violations) <= 2 else "block")

        return GuardrailResult(
            passed=passed,
            violations=violations,
            sanitized_response=sanitized,
            action=action,
        )

    def check_input(self, user_message: str) -> GuardrailResult:
        """Check user input for policy violations."""
        violations: List[str] = []

        # Prompt injection attempts
        injection_patterns = [
            r"ignore (previous|all|prior) instructions",
            r"you are now",
            r"pretend (you are|to be)",
            r"act as (a|an) (?!support)",
            r"DAN mode",
            r"jailbreak",
        ]
        for pat in injection_patterns:
            if re.search(pat, user_message, re.IGNORECASE):
                violations.append(f"prompt_injection:{pat}")

        passed = len(violations) == 0
        return GuardrailResult(
            passed=passed,
            violations=violations,
            sanitized_response=user_message if passed else "[Input blocked by safety filter]",
            action="allow" if passed else "block",
        )


_GUARDRAILS: Guardrails | None = None


def get_guardrails() -> Guardrails:
    global _GUARDRAILS
    if _GUARDRAILS is None:
        _GUARDRAILS = Guardrails()
    return _GUARDRAILS
