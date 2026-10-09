"""Count surface AI-writing markers in Mongolian (Cyrillic) text.

Usage:
    python mn_markers.py FILE
    python mn_markers.py < FILE

Prints a JSON report: hits per check, how many distinct pattern types were
found, and the suggested intervention level (light / selective / full).
This only catches mechanical markers. Calques and rhythm need a human or model
reading; treat the count as a floor, not a verdict.
"""

from __future__ import annotations

import json
import re
import sys
from collections.abc import Callable
from pathlib import Path

WORD = r"[А-Яа-яЁёӨөҮүA-Za-z]"

# Phrase families mirror references/ai-phrases.md (A*) and kantselyarit.md (K).
STOCK_PHRASES: dict[str, tuple[str, ...]] = {
    "A1_inflated_significance": (
        "чухал үүрэг гүйцэтгэдэг",
        "чухал үүрэг гүйцэтгэх",
        "онцгой ач холбогдолтой",
        "шийдвэрлэх ач холбогдолтой",
        "үнэлж баршгүй",
        "салшгүй хэсэг",
        "үндэс суурь",
        "түлхүүр болдог",
        "шинэ эрин үе",
    ),
    "A2_stock_opener": ("хурдацтай хөгжиж буй", "даяаршиж буй", "технологийн эрин"),
    "A3_transition_pile": ("мөн түүнчлэн", "үүний зэрэгцээ", "түүгээр ч зогсохгүй", "нэмж хэлэхэд"),
    "A4_empty_conclusion": ("дүгнэж хэлэхэд", "эцэст нь хэлэхэд", "ирээдүй гэрэлтэй", "гэрэлт зам"),
    "A7_negative_parallelism": ("зүгээр нэг",),
    "A8_vague_attribution": (
        "судлаачдын үзэж байгаагаар",
        "мэргэжилтнүүдийн хэлснээр",
        "судалгаагаар батлагдсан",
    ),
    "A10_chatbot_leftover": (
        "мэдээжийн хэрэг",
        "маш сайн асуулт",
        "тусалсандаа баяртай",
        "нэмэлт мэдээлэл хэрэгтэй бол",
    ),
    "K_kantselyarit": (
        "арга хэмжээ авах",
        "ажлыг хэрэгжүүлэх",
        "ажлыг хэрэгжүүлсэн",
        "зохион байгуулах ажлыг",
        "анхаарч ажиллана",
        "улам бүр",
        "байгаа болно",
    ),
}

CALQUE_PATTERNS: tuple[str, ...] = (
    r"тусламжтайгаар",
    r"{w}+х боломжтой",
    # "өөрсдийн мэдлэг, ур чадвараа": possessive pronoun doubling the reflexive suffix
    r"өөр(ийн|сдийн)\s[^.!?]{{0,40}}?{w}(аа|ээ|оо|өө)\b",
    r"(?<!{w})нэг (чухал|том|томоохон|гайхалтай|шинэ) ",
)

QUANTIFIERS = (
    "олон|бүх|зарим|ихэнх|хэд хэдэн|цөөн|цөөхөн|"
    "хоёр|гурван|дөрвөн|таван|зургаан|долоон|найман|есөн|арван"
)
PLURAL_SUFFIX = r"{w}+(ууд|үүд|нууд|нүүд|чууд|чүүд)\b|хүмүүс|{w}+ нар\b"

NI = re.compile(rf"(?<!{WORD})нь(?!{WORD})", re.IGNORECASE)
LONG_DASH = re.compile(r"(?<!\d)\s*[—–]\s*(?!\d)|\s--\s")
SENTENCE_END = re.compile(r"(?<=[.!?…])\s+")
HEADING = re.compile(r"^\s*#{1,6}\s+(.+)$", re.MULTILINE)
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿✅]")
BOLD_LABEL = re.compile(r"^\s*(?:[-*•]|\S{1,2})?\s*\*\*[^*]+:\*\*", re.MULTILINE)
BOLON_LIST = re.compile(rf"{WORD}+,\s+(болон|ба)\s+{WORD}+", re.IGNORECASE)


def _compile(pattern: str) -> re.Pattern[str]:
    return re.compile(pattern.format(w=WORD), re.IGNORECASE)


CALQUES = tuple(_compile(p) for p in CALQUE_PATTERNS)
QUANT_PLURAL = _compile(rf"(?<!{{w}})({QUANTIFIERS})\s+({PLURAL_SUFFIX})")


def split_sentences(text: str) -> list[str]:
    return [s.strip() for s in SENTENCE_END.split(text.strip()) if s.strip()]


def check_ni_overuse(text: str) -> list[str]:
    """Sentences with a doubled 'нь', or every 'нь' sentence when it is dense.

    Dense means 3+ in total and in at least half of the sentences.
    """
    sentences = split_sentences(text)
    counts = [len(NI.findall(s)) for s in sentences]
    doubled = [s for s, n in zip(sentences, counts) if n >= 2]
    with_ni = [s for s, n in zip(sentences, counts) if n]
    dense = sum(counts) >= 3 and len(with_ni) * 2 >= len(sentences)
    return with_ni if dense else doubled


def check_stock_phrases(text: str) -> list[str]:
    lowered = text.lower()
    return [p for phrases in STOCK_PHRASES.values() for p in phrases if p in lowered]


def stock_phrase_families(text: str) -> list[str]:
    lowered = text.lower()
    return [fam for fam, phrases in STOCK_PHRASES.items() if any(p in lowered for p in phrases)]


def check_calques(text: str) -> list[str]:
    return [m.group(0) for rx in CALQUES for m in rx.finditer(text)]


def check_quantifier_plural(text: str) -> list[str]:
    return [m.group(0) for m in QUANT_PLURAL.finditer(text)]


def check_dashes(text: str) -> list[str]:
    return [m.group(0) for m in LONG_DASH.finditer(text)]


def check_monotonous_endings(text: str) -> list[str]:
    """Endings repeated in 3+ consecutive sentences, or in 3+ sentences that
    make up at least 40% of the text."""
    last_words = [
        re.sub(r"[^\w]", "", s.split()[-1].lower()) for s in split_sentences(text) if s.split()
    ]
    found: list[str] = []
    streak = 1
    for prev, cur in zip(last_words, last_words[1:]):
        streak = streak + 1 if cur and cur == prev else 1
        if streak == 3:
            found.append(cur)
    for word in dict.fromkeys(last_words):
        n = last_words.count(word)
        if word and word not in found and n >= 3 and n * 5 >= len(last_words) * 2:
            found.append(word)
    return found


def check_title_case(text: str) -> list[str]:
    hits = []
    for heading in HEADING.findall(text):
        words = [w for w in re.findall(rf"{WORD}+", heading) if len(w) > 2]
        if len(words) >= 2 and all(w[0].isupper() for w in words):
            hits.append(heading.strip())
    return hits


def check_emoji(text: str) -> list[str]:
    return EMOJI.findall(text)


def check_bold_labels(text: str) -> list[str]:
    return BOLD_LABEL.findall(text)


def check_bolon_list(text: str) -> list[str]:
    return [m.group(0) for m in BOLON_LIST.finditer(text)]


def check_mash(text: str) -> list[str]:
    hits = re.findall(rf"(?<!{WORD})маш(?!{WORD})", text, re.IGNORECASE)
    return hits if len(hits) >= 3 else []


CHECKS: dict[str, Callable[[str], list[str]]] = {
    "ni_overuse": check_ni_overuse,
    "stock_phrases": check_stock_phrases,
    "calques": check_calques,
    "quantifier_plural": check_quantifier_plural,
    "dashes": check_dashes,
    "monotonous_endings": check_monotonous_endings,
    "title_case_headings": check_title_case,
    "emoji": check_emoji,
    "bold_label_lists": check_bold_labels,
    "bolon_in_lists": check_bolon_list,
    "mash_overuse": check_mash,
}


def level_for(types_found: int) -> str:
    if types_found <= 2:
        return "light"
    if types_found <= 5:
        return "selective"
    return "full"


def analyze(text: str) -> dict:
    hits = {name: check(text) for name, check in CHECKS.items()}
    # Each stock-phrase family counts as its own pattern type.
    families = stock_phrase_families(text)
    other_types = sum(1 for name, found in hits.items() if found and name != "stock_phrases")
    types_found = len(families) + other_types
    return {
        "types_found": types_found,
        "level": level_for(types_found),
        "phrase_families": families,
        "hits": {name: found for name, found in hits.items() if found},
    }


def main(argv: list[str]) -> int:
    try:
        if len(argv) > 1:
            text = Path(argv[1]).read_text(encoding="utf-8")
        else:
            sys.stdin.reconfigure(encoding="utf-8")
            text = sys.stdin.read()
    except (OSError, UnicodeDecodeError) as exc:
        sys.stderr.write(f"mn_markers: cannot read input: {exc}\n")
        return 1
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stdout.write(json.dumps(analyze(text), ensure_ascii=False, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
