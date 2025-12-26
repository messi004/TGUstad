import re
from .constants import EXPLICIT_KEYWORDS, SEVERE_KEYWORDS

LINK_PATTERN = re.compile(r"http[s]?://")
MENTION_PATTERN = re.compile(r"@\w+")

def has_link_or_mention(text: str) -> bool:
    return bool(LINK_PATTERN.search(text) or MENTION_PATTERN.search(text))


def keyword_or_pattern_match(text: str) -> bool:
    text_l = text.lower()

    # Severe keywords (instant strike)
    for kw in SEVERE_KEYWORDS:
        if kw in text_l:
            return True

    # Language keywords
    for lang in ("english", "hindi", "tamil"):
        for kw in EXPLICIT_KEYWORDS.get(lang, []):
            if kw in text_l:
                return True

    # Regex patterns
    for pattern in EXPLICIT_KEYWORDS["patterns"]:
        if pattern.search(text):
            return True

    return False