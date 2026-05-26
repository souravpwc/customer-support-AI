"""PII / sensitive-data masker using regex patterns."""
from __future__ import annotations
import re
from typing import List, Tuple

# (pattern, replacement, label)
_RULES: List[Tuple[re.Pattern, str, str]] = [
    (re.compile(r"\b[A-Z0-9]{16}\b"), "[CARD-NUMBER]", "credit_card"),
    (re.compile(r"\b(?:\d[ -]*?){13,16}\b"), "[CARD-NUMBER]", "credit_card_digits"),
    (re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), "[SSN]", "ssn"),
    (re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b"), "[EMAIL]", "email"),
    (re.compile(r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b"), "[PHONE]", "phone"),
    (re.compile(r"\b\d{5}(?:-\d{4})?\b"), "[ZIP]", "zip_code"),
    # API/secret keys (long hex or base64-looking strings)
    (re.compile(r"\b[A-Za-z0-9+/]{32,}={0,2}\b"), "[REDACTED-KEY]", "api_key"),
    # Password patterns
    (re.compile(r"(?i)password\s*[=:]\s*\S+"), "password=[REDACTED]", "password"),
]


class DataMasker:
    """Masks PII from text before logging or displaying."""

    def mask(self, text: str) -> Tuple[str, List[str]]:
        """
        Returns (masked_text, list_of_detected_types).
        Text is safe to log; original is NOT stored.
        """
        detected: List[str] = []
        result = text
        for pattern, replacement, label in _RULES:
            new = pattern.sub(replacement, result)
            if new != result:
                detected.append(label)
                result = new
        return result, detected

    def mask_dict(self, data: dict) -> dict:
        """Recursively mask string values in a dict."""
        masked = {}
        for k, v in data.items():
            if isinstance(v, str):
                masked[k], _ = self.mask(v)
            elif isinstance(v, dict):
                masked[k] = self.mask_dict(v)
            elif isinstance(v, list):
                masked[k] = [
                    self.mask(i)[0] if isinstance(i, str)
                    else self.mask_dict(i) if isinstance(i, dict)
                    else i
                    for i in v
                ]
            else:
                masked[k] = v
        return masked

    def contains_pii(self, text: str) -> bool:
        _, detected = self.mask(text)
        return len(detected) > 0


_MASKER: DataMasker | None = None


def get_masker() -> DataMasker:
    global _MASKER
    if _MASKER is None:
        _MASKER = DataMasker()
    return _MASKER
