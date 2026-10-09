"""Count mechanical translationese markers in Mongolian (Cyrillic) text.

Usage:
    python mn_markers.py FILE
    python mn_markers.py < FILE

Prints a JSON report: hits per check, how many distinct marker types were
found, and a suggested intervention level (light / selective / full).

The checks follow the evidence in references/: noun + хийх instead of a verb,
agentless passives, redundant plurals, runs of identical endings, piled-up
"нь", chatbot residue, unsourced attributions, and AI typography. They do NOT
flag formal formulas ("чухал үүрэг гүйцэтгэдэг", "Дүгнэж хэлэхэд"), topic
"нь", or connectives: those are native Mongolian. Treat the count as a floor,
not a verdict.
"""

from __future__ import annotations

import json
import re
import sys
from collections.abc import Callable
from pathlib import Path

WORD = r"[А-Яа-яЁёӨөҮүA-Za-z]"


def _compile(pattern: str) -> re.Pattern[str]:
    return re.compile(pattern.format(w=WORD), re.IGNORECASE)


# T1/T3: lexicalised noun (-лт, -лга) + a light verb where Mongolian uses the verb.
NOUN_VERB = _compile(
    r"(?<!{w})({w}+(?:лт|лага|лэг|лого|лөг|лга|лгэ))\s+"
    r"(хийгд{w}*|явагд{w}*|хий(?:в|лээ|сэн|нэ|х|ж|дэг|гээд)?)(?!{w})"
)
# Event nouns: "сургалт явагдана", "хэлэлцүүлэг явагдлаа" are native.
EVENT_NOUNS = ("сургалт", "уулзалт", "ярилцлага", "хэлэлцүүлэг", "үзэсгэлэн", "сонгон шалгаруулалт")
# Established collocations with хийх ("захиалга хийх") are everyday Mongolian.
ESTABLISHED_HIIH = ("захиалга",)

# T2: passive -гд- with a finite or participle ending.
PASSIVE = _compile(
    r"(?<!{w})({w}+гд(?:сан|сэн|сон|сөн|лаа|лээ|лоо|лөө|ана|энэ|оно|өнө|ах|эх|ох|өх"
    r"|жээ|чээ|ав|эв|ов|өв|аж|эж|ож|өж|даг|дэг|дог|дөг))(?!{w})"
)
# Native -гд- verbs: perception, spontaneous, or lexical (not translation passives).
NATIVE_GD_STEMS = (
    "харагд", "санагд", "бодогд", "сонсогд", "үзэгд", "мэдэгд", "мэдрэгд",
    "анзаарагд", "хамрагд", "дуулдагд", "тохиолдогд",
)
PASSIVE_MIN_HITS = 2

QUANTIFIERS = (
    "олон|бүх|зарим|ихэнх|хэд хэдэн|цөөн|цөөхөн|"
    "хоёр|гурван|дөрвөн|таван|зургаан|долоон|найман|есөн|арван|\\d+"
)
# Plural stems (-ууд/-үүд, -чид, -чд-, нар, хүмүүс) with an optional case ending.
# Case endings are listed explicitly so words like "буудал" do not match.
CASE = "ын|ийн|ад|эд|ыг|ийг|тай|тэй|аас|ээс|аар|ээр|аа|ээ"
PLURAL = (
    r"{w}+(?:ууд|үүд|чид)(?:" + CASE + r")?(?!{w})"
    r"|{w}+чд(?:ын|ад|эд|аас|ээс)(?!{w})"
    r"|хүмүүс{w}*"
    r"|{w}+ нар(?:ын|т|тай|аас)?(?!{w})"
)
QUANT_PLURAL = _compile(
    rf"(?<!{{w}})(?:{QUANTIFIERS})\s+(?!улсын)(?:{{w}}+\s+)?(?:{PLURAL})"
)

NI = _compile(r"(?<!{w})нь(?!{w})")
DOUBLED_POSSESSIVE = _compile(
    r"(?<!{w})(?:таны|миний|чиний|бидний)\s+(?:{w}+\s+){{1,4}}(?:тань|минь|чинь|маань)(?!{w})"
)
BOLON_LIST = _compile(r"{w}+,\s+(?:болон|ба)\s+{w}+")
MASH = _compile(r"(?<!{w})маш(?!{w})")
MASH_MIN_HITS = 3

SAN_ENDING = re.compile(r"(сан|сэн|сон|сөн)$")
RUN_LENGTH = 3

CHATBOT_PHRASES = (
    "мэдээжийн хэрэг",
    "маш сайн асуулт",
    "тусалсандаа баяртай",
    "тустай байх гэж найдаж",
    "нэмэлт мэдээлэл хэрэгтэй бол",
    "дэлгэрэнгүй авч үзье",
    "-ыг хүргэж байна",
)
ATTRIBUTION_PHRASES = (
    "судлаачдын үзэж байгаагаар",
    "судлаачийн үзэж байгаагаар",
    "мэргэжилтнүүдийн хэлснээр",
    "судалгаагаар батлагдсан",
    "эрдэмтэд үздэг",
)
CALQUED_IDIOMS = (
    "мэдрэмж төр",
    "мэдрэмж ав",
    "хонгилын үзүүрт",
    "нэг оронтой тоонд",
)

SENTENCE_END = re.compile(r"(?<=[.!?…])\s+")
LONG_DASH = re.compile(r"(?<!\d)\s*[—–]\s*(?!\d)|\s--\s")
HEADING = re.compile(r"^\s*#{1,6}\s+(.+)$", re.MULTILINE)
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿✅]")
BOLD_LABEL = re.compile(r"^\s*(?:[-*•]|\S{1,2})?\s*\*\*[^*]+:\*\*", re.MULTILINE)


def split_sentences(text: str) -> list[str]:
    return [s.strip() for s in SENTENCE_END.split(text.strip()) if s.strip()]


def _find_phrases(text: str, phrases: tuple[str, ...]) -> list[str]:
    lowered = text.lower()
    return [p for p in phrases if p in lowered]


def check_noun_verb(text: str) -> list[str]:
    return [
        m.group(0)
        for m in NOUN_VERB.finditer(text)
        if not _is_native_collocation(m.group(1).lower(), m.group(2).lower())
    ]


def _is_native_collocation(noun: str, verb: str) -> bool:
    if verb.startswith("явагд"):
        return noun in EVENT_NOUNS
    return verb.startswith("хий") and not verb.startswith("хийгд") and noun in ESTABLISHED_HIIH


def check_passive(text: str) -> list[str]:
    hits = [
        m.group(1)
        for m in PASSIVE.finditer(text)
        if not m.group(1).lower().startswith(NATIVE_GD_STEMS)
    ]
    return hits if len(hits) >= PASSIVE_MIN_HITS else []


def check_quantifier_plural(text: str) -> list[str]:
    return [m.group(0) for m in QUANT_PLURAL.finditer(text)]


QUOTED = re.compile(r'"[^"]*"|«[^»]*»|“[^”]*”')
CLAUSE_BREAK = re.compile(r",|;|\s(?:мөртлөө|харин|боловч|гэвч)\s")


def check_ni_overuse(text: str) -> list[str]:
    """Sentences where one clause stacks two or more standalone "нь".

    Parallel contrastive "нь" across balanced clauses ("Үг нь монгол,
    өгүүлбэр нь орос") is native, and quoted text is left alone.
    """
    hits = []
    for sentence in split_sentences(text):
        clauses = CLAUSE_BREAK.split(QUOTED.sub(" ", sentence))
        if any(len(NI.findall(c)) >= 2 for c in clauses):
            hits.append(sentence)
    return hits


def check_doubled_possessive(text: str) -> list[str]:
    return [m.group(0) for m in DOUBLED_POSSESSIVE.finditer(text)]


def check_bolon_list(text: str) -> list[str]:
    return [m.group(0) for m in BOLON_LIST.finditer(text)]


def check_mash(text: str) -> list[str]:
    hits = MASH.findall(text)
    return hits if len(hits) >= MASH_MIN_HITS else []


def _last_words(text: str) -> list[str]:
    return [
        re.sub(r"[^\w]", "", s.split()[-1].lower())
        for s in split_sentences(text)
        if s.split()
    ]


def check_ending_runs(text: str) -> list[str]:
    """Runs of 3+ consecutive sentences ending in the same word, or all in -сан."""
    words = _last_words(text)
    runs: list[str] = []
    same = san = 1
    for prev, cur in zip(words, words[1:]):
        same = same + 1 if cur and cur == prev else 1
        san = san + 1 if SAN_ENDING.search(cur) and SAN_ENDING.search(prev) else 1
        if same == RUN_LENGTH:
            runs.append(f"…{cur} ×{RUN_LENGTH}")
        elif san == RUN_LENGTH and same < RUN_LENGTH:
            runs.append(f"…-сан ×{RUN_LENGTH}")
    return runs


def check_chatbot(text: str) -> list[str]:
    return _find_phrases(text, CHATBOT_PHRASES)


def check_attribution(text: str) -> list[str]:
    return _find_phrases(text, ATTRIBUTION_PHRASES)


def check_calqued_idioms(text: str) -> list[str]:
    return _find_phrases(text, CALQUED_IDIOMS)


def check_dashes(text: str) -> list[str]:
    return [m.group(0) for m in LONG_DASH.finditer(text)]


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


CHECKS: dict[str, Callable[[str], list[str]]] = {
    "noun_plus_light_verb": check_noun_verb,
    "agentless_passive": check_passive,
    "redundant_plural": check_quantifier_plural,
    "ending_runs": check_ending_runs,
    "ni_pileup": check_ni_overuse,
    "doubled_possessive": check_doubled_possessive,
    "calqued_idioms": check_calqued_idioms,
    "bolon_in_lists": check_bolon_list,
    "mash_overuse": check_mash,
    "chatbot_leftovers": check_chatbot,
    "unsourced_attribution": check_attribution,
    "dashes": check_dashes,
    "title_case_headings": check_title_case,
    "emoji": check_emoji,
    "bold_label_lists": check_bold_labels,
}


def level_for(types_found: int) -> str:
    if types_found <= 2:
        return "light"
    if types_found <= 5:
        return "selective"
    return "full"


def analyze(text: str) -> dict:
    hits = {name: check(text) for name, check in CHECKS.items()}
    found = {name: items for name, items in hits.items() if items}
    return {
        "types_found": len(found),
        "level": level_for(len(found)),
        "hits": found,
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
