"""Count mechanical markers in Mongolian (Cyrillic) text: translationese and AI-output tells.

Usage:
    python mn_markers.py FILE [--register REGISTER]
    python mn_markers.py [--register REGISTER] < FILE

REGISTER is one of: auto (default), essay, official, legal, academic, news,
literary, post. It mutes checks that are native in that register.

Prints a JSON report with three groups:
    hits          sentence-level style problems; they set the level
    flags         things to remove, flag for the author, or fix lightly
                  (chat framing, placeholders, unsourced claims, generic
                  voice, typography); they do not set the level
    observations  absences worth noticing but never "fixing" by invention

"level" (light / selective / full) is the share of sentences with a style
problem: at most one in three is light, up to half is selective, more is full,
as defined in SKILL.md. Every check was measured on pre-2021 human Mongolian
and current LLM output (references/ai-output.md); checks that fired on most human
texts were removed or narrowed. Treat the report as a floor, not a verdict.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Callable
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # sibling import under python -I

from mn_text import (  # noqa: E402
    CYR,
    WORD,
    AUXILIARY_ENDINGS,
    CYR_WORD,
    is_generic_ending,
    last_word,
    prose_sentences,
    prose_units,
    split_framing,
    split_sentences,
)

REGISTERS = ("auto", "essay", "official", "legal", "academic", "news", "literary", "post")


def _compile(pattern: str) -> re.Pattern[str]:
    return re.compile(pattern.format(w=WORD), re.IGNORECASE)


# T1/T3: lexicalised noun (-лт, -лга) + a light verb where Mongolian uses the verb.
NOUN_VERB = _compile(
    r"(?<!{w})({w}+(?:лт|лага|лэг|лого|лөг|лга|лгэ))\s+"
    r"(хийгд{w}*|явагд{w}*|хий(?:в|лээ|сэн|нэ|х|ж|дэг|гээд)?)(?!{w})"
)
# Event nouns: "сургалт явагдана", "хэлэлцүүлэг явагдлаа" are native.
EVENT_NOUNS = ("сургалт", "уулзалт", "ярилцлага", "хэлэлцүүлэг", "үзэсгэлэн", "сонгон шалгаруулалт")
# Established collocations with хийх, the most frequent in human news and reports.
ESTABLISHED_HIIH = (
    "захиалга", "шалгалт", "нээлт", "дүгнэлт", "сонголт", "хэмжилт", "оруулалт", "танилцуулга",
    "бичлэг", "нэвтрүүлэг", "сурвалжлага", "үзлэг", "ажиглалт", "оролдлого", "тоглолт",
    "дадлага", "эвлүүлэг", "золголт", "хатгалга", "тохижилт", "тээвэрлэлт", "байгуулалт",
)

# T2: a passive purposive governed by another passive ("зохион байгуулагдахаар
# төлөвлөгдөж"). Single agentless passives are left to judgement: in human news
# and reports they are as frequent as in AI text, and most are lexical
# (нэгдсэн, нэмэгдэх) or fixed formulas (хуулиар хамгаалагдсан).
STACKED_PASSIVE = _compile(r"(?<!{w}){w}+гд(?:ахаар|эхээр|охоор|өхөөр)\s+{w}+гд{w}*")

QUANTIFIERS = (
    "олон|бүх|зарим|ихэнх|хэд хэдэн|цөөн|цөөхөн|"
    "хоёр|гурван|дөрвөн|таван|зургаан|долоон|найман|есөн|арван|\\d+"
)
CASE = "ын|ийн|ад|эд|ыг|ийг|тай|тэй|аас|ээс|аар|ээр|аа|ээ"
# Plural stems with an optional case ending. Two or more stem letters, so
# "шууд", "бууд", "зүүд" are not plurals.
PLURAL = (
    r"{w}{{2,}}(?:ууд|үүд|чид)(?:" + CASE + r")?(?!{w})"
    r"|{w}+чд(?:ын|ад|эд|аас|ээс)(?!{w})"
    r"|хүмүүс{w}*"
    r"|{w}+ нар(?:ын|т|тай|аас)?(?!{w})"
)
QUANT_PLURAL = _compile(rf"(?<!{{w}})(?:{QUANTIFIERS})\s+(?!улсын)(?:{{w}}+\s+)?(?:{PLURAL})")
# "-гчид", "-аачид" after "эхний/сүүлийн N" is usually a dative singular
# ("Эхний 100 үйлчлүүлэгчид бэлэг өгнө"); elsewhere it is the plural.
AMBIGUOUS_PLURAL = re.compile(r"(?:гчид|аачид|ээчид|оочид|өөчид)$", re.I)
ORDINAL_CONTEXT = ("эхний", "сүүлийн")
NOT_PLURAL = ("илүүд", "хариуд", "зориуд")

NI = _compile(r"(?<!{w})нь(?!{w})")
NI_FIXED = _compile(r"(?<!{w})(?:ер|учир|уг|жишээ|эцэст|дараа|гол|ихэнх|зарим)\s+нь(?!{w})")
NI_MAX_PER_CLAUSE = 2
QUOTED = re.compile(r'"[^"]*"|«[^»]*»|“[^”]*”')
# Clause boundaries: punctuation, conjunctions, and the space after a converb.
CONVERB_ENDINGS = ("ж", "аад", "ээд", "оод", "өөд", "вал", "вэл", "вол", "вөл", "бал", "бэл", "тал", "тэл", "тол", "төл")
CLAUSE_BREAK = re.compile(
    r",|;|:|\s(?:мөртлөө|харин|боловч|гэвч|бөгөөд|ба)\s|"
    + "|".join(rf"(?<=[{CYR}]{{2}}{e})\s" for e in CONVERB_ENDINGS),
    re.IGNORECASE,
)
DOUBLED_POSSESSIVE = _compile(
    r"(?<!{w})(?:таны|миний|чиний|бидний)\s+(?:{w}+\s+){{1,4}}(?:тань|минь|чинь|маань)(?!{w})"
)
BOLON_LIST = _compile(r"{w}+,\s+(?:болон|ба)\s+{w}+")

SAN_ENDING = re.compile(r"(сан|сэн|сон|сөн)$")
RUN_LENGTH = 3

# Sentence-initial additive and consequence connectors that current LLMs stack
# (Мөн 4.5x, Иймд 7x, Юуны өмнө 9.5x the human rate). Ordinals (Нэгдүгээрт,
# Хоёрдугаарт) and essay formulas (Нэг талаас, Дүгнэж хэлэхэд) were not
# AI-heavy and are not counted. "Иймд" is also the official request formula.
CONNECTORS = (
    "мөн түүнчлэн", "мөн", "иймд", "иймээс", "тиймээс", "юуны өмнө", "түүнчлэн",
    "үүний зэрэгцээ", "түүнээс гадна", "үүнээс гадна", "нэмж хэлэхэд",
)
CONNECTOR_START = _compile(r"^(" + "|".join(CONNECTORS) + r")(?!{w})")
OFFICIAL_FORMULA_CONNECTORS = ("иймд",)
CONNECTOR_MIN, CONNECTOR_MIN_SHARE, CONNECTOR_ALLOWED_PER = 3, 0.2, 5

GENERIC_MIN, GENERIC_MIN_SHARE = 3, 0.45
BOLOMJTOI = _compile(r"(?<!{w}){w}+х\s+боломжтой(?!{w})")
BOLOMJTOI_MIN = 3

CHATBOT_PHRASES = (
    "мэдээжийн хэрэг",
    "маш сайн асуулт",
    "тусалсандаа баяртай",
    "тустай байх гэж найдаж",
    "нэмэлт мэдээлэл хэрэгтэй бол",
    "дэлгэрэнгүй авч үзье",
    "-ыг хүргэж байна",
)
ATTRIBUTION = _compile(
    r"гэж\s+(?:салбарын\s+)?(?:мэргэжилтнүүд|судлаачид|эрдэмтэд|шинжээчид)"
    r"|(?<!{w})(?:судлаач|мэргэжилтн|эрдэмт|шинжээч){w}*\s+(?:{w}+\s+){{0,2}}?"
    r"(?:үзэж|үздэг|хэлснээр|хэлж|анхааруул|тэмдэглэ|онцол|сануул){w}*"
    r"|судалгаагаар батлагдсан"
)
CALQUED_IDIOMS = (
    "мэдрэмж төр",
    "мэдрэмж ав",
    "хонгилын үзүүрт",
    "нэг оронтой тоонд",
)
PLACEHOLDER = re.compile(r"\[[^\]\n]{1,60}\](?!\()|_{4,}|\.{5,}")

LONG_DASH = re.compile(r"(?<!\d)\s*[—–]\s*(?!\d)|\s--\s")
HEADING = re.compile(r"^\s*#{1,6}\s+(.+)$", re.MULTILINE)
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿✅]")
BOLD_LABEL = re.compile(r"^\s*(?:[-*•]|\S{1,2})?\s*\*\*[^*]+:\*\*", re.MULTILINE)
PARTICLES = re.compile(rf"(?<![{CYR}])(?:л|даа|дээ|доо|дөө|биз|билээ|шүү)(?![{CYR}])", re.I)
LONG_SENTENCE_WORDS = 25
OBSERVE_MIN_SENTENCES = 8
FORMAL_REGISTERS = ("official", "legal", "academic", "news")

MUTED: dict[str, frozenset[str]] = {
    "academic": frozenset({"generic_voice"}),
    "literary": frozenset({"dashes", "emoji"}),
    "post": frozenset({"emoji"}),
}


def _find_phrases(text: str, phrases: tuple[str, ...]) -> list[str]:
    lowered = text.lower()
    return [p for p in phrases if p in lowered]


# ------------------------------------------------------------- style checks
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
    return [m.group(0) for m in STACKED_PASSIVE.finditer(text)]


def check_quantifier_plural(text: str) -> list[str]:
    hits = []
    for m in QUANT_PLURAL.finditer(text):
        plural = m.group(0).split()[-1].lower()
        before = CYR_WORD.findall(text[: m.start()].lower())
        if plural in NOT_PLURAL:
            continue
        if AMBIGUOUS_PLURAL.search(plural) and before and before[-1] in ORDINAL_CONTEXT:
            continue  # "Эхний 100 үйлчлүүлэгчид" reads as a dative singular
        if m.group(0).lower().startswith("олон") and before and before[-1].endswith("чин"):
            continue  # "наадамчин олон" is a noun: "the crowd"
        hits.append(m.group(0))
    return hits


def check_ni_overuse(text: str) -> list[str]:
    """Sentences where one clause stacks three or more "нь".

    Two in a clause ("Аав нь гарыг нь бариад") is ordinary Mongolian, and so
    are parallel "нь" across balanced clauses, fixed phrases ("ер нь", "учир
    нь"), and quoted text.
    """
    hits = []
    for sentence in split_sentences(text):
        bare = NI_FIXED.sub(" ", QUOTED.sub(" ", sentence))
        if any(len(NI.findall(c)) > NI_MAX_PER_CLAUSE for c in CLAUSE_BREAK.split(bare)):
            hits.append(sentence)
    return hits


def check_doubled_possessive(text: str) -> list[str]:
    return [m.group(0) for m in DOUBLED_POSSESSIVE.finditer(text)]


def check_bolon_list(text: str) -> list[str]:
    return [m.group(0) for m in BOLON_LIST.finditer(text)]


def check_calqued_idioms(text: str) -> list[str]:
    return _find_phrases(text, CALQUED_IDIOMS)


def _run_indices(sentences: list[str], lines: list[int] | None = None) -> list[list[int]]:
    """Runs of 3+ sentences in one paragraph ending in the same lexical word, or all in -сан.

    Auxiliaries and particles (байна, юм, билээ, даа...) are excluded: a run of
    them is native. A run never crosses a line break, so one-line list items
    ("2-р сард ... зохион байгуулсан.") are not a run.
    """
    lines = lines if lines is not None else [0] * len(sentences)
    words = [last_word(s) for s in sentences]
    lexical = [w if w and w not in AUXILIARY_ENDINGS else "" for w in words]
    runs: list[list[int]] = []
    start = 0
    for i in range(1, len(lexical) + 1):
        if (
            i < len(lexical)
            and lines[i] == lines[i - 1]
            and lexical[i]
            and _same_ending(lexical[i - 1], lexical[i])
        ):
            continue
        if i - start >= RUN_LENGTH:
            runs.append(list(range(start, i)))
        start = i
    return runs


def _same_ending(prev: str, cur: str) -> bool:
    return bool(prev) and (prev == cur or bool(SAN_ENDING.search(prev) and SAN_ENDING.search(cur)))


def check_ending_runs(text: str) -> list[str]:
    units = prose_units(text)
    sentences, lines = [s for _, s in units], [n for n, _ in units]
    return [f"…{last_word(sentences[r[-1]])} ×{len(r)}" for r in _run_indices(sentences, lines)]


def _connector_indices(sentences: list[str], muted: tuple[str, ...] = ()) -> list[int]:
    """Sentence-initial connectors beyond about one per five sentences, when piled."""
    found = []
    for i, s in enumerate(sentences):
        m = CONNECTOR_START.match(s)
        if m and m.group(1).lower() not in muted:
            found.append(i)
    if len(found) < CONNECTOR_MIN or len(found) < CONNECTOR_MIN_SHARE * len(sentences):
        return []
    allowed = max(1, len(sentences) // CONNECTOR_ALLOWED_PER)
    return found[allowed:]


def check_connector_pile(text: str, muted: tuple[str, ...] = ()) -> list[str]:
    sentences = prose_sentences(text)
    return [CONNECTOR_START.match(sentences[i]).group(1) for i in _connector_indices(sentences, muted)]


# ------------------------------------------------------- flags (no level)
def check_generic_voice(text: str) -> list[str]:
    """General-truth -даг and prescriptive endings, when they dominate the text."""
    sentences = prose_sentences(text)
    generic = [s for s in sentences if is_generic_ending(s)]
    if len(generic) < GENERIC_MIN or len(generic) < GENERIC_MIN_SHARE * len(sentences):
        return []
    return [s[-60:] for s in generic]


def check_bolomjtoi(text: str) -> list[str]:
    hits = [m.group(0) for m in BOLOMJTOI.finditer(text)]
    return hits if len(hits) >= BOLOMJTOI_MIN else []


def check_chat_framing(text: str) -> list[str]:
    pre, _, out = split_framing(text)
    return [x for x in (pre, out) if x]


def check_placeholders(text: str) -> list[str]:
    return PLACEHOLDER.findall(text)


def check_chatbot(text: str) -> list[str]:
    return _find_phrases(text, CHATBOT_PHRASES)


def check_attribution(text: str) -> list[str]:
    return [m.group(0) for m in ATTRIBUTION.finditer(text)]


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


# Local checks run per sentence, so each hit maps to the sentences it touches.
SENTENCE_CHECKS: dict[str, Callable[[str], list[str]]] = {
    "noun_plus_light_verb": check_noun_verb,
    "stacked_passive": check_passive,
    "redundant_plural": check_quantifier_plural,
    "ni_pileup": check_ni_overuse,
    "doubled_possessive": check_doubled_possessive,
    "calqued_idioms": check_calqued_idioms,
    "bolon_in_lists": check_bolon_list,
}
FLAG_CHECKS: dict[str, Callable[[str], list[str]]] = {
    "placeholders": check_placeholders,
    "chatbot_leftovers": check_chatbot,
    "unsourced_attribution": check_attribution,
    "generic_voice": check_generic_voice,
    "bolomjtoi_filler": check_bolomjtoi,
    "dashes": check_dashes,
    "title_case_headings": check_title_case,
    "emoji": check_emoji,
    "bold_label_lists": check_bold_labels,
}


def level_for(problem_sentences: int, sentences: int) -> str:
    """light: at most 1 in 3 sentences; selective: up to half; full: more."""
    if problem_sentences <= 0 or sentences <= 0:
        return "light"
    if sentences < 3:
        return "selective"
    share = problem_sentences / sentences
    if share <= 1 / 3:
        return "light"
    return "selective" if share <= 0.5 else "full"


def _style_hits(sentences: list[str], lines: list[int], register: str) -> tuple[dict[str, list[str]], set[int]]:
    hits: dict[str, list[str]] = {}
    touched: set[int] = set()
    for name, check in SENTENCE_CHECKS.items():
        for i, s in enumerate(sentences):
            found = check(s)
            if found:
                hits.setdefault(name, []).extend(found)
                touched.add(i)
    for run in _run_indices(sentences, lines):
        hits.setdefault("ending_runs", []).append(f"…{last_word(sentences[run[-1]])} ×{len(run)}")
        touched.update(run)
    muted = OFFICIAL_FORMULA_CONNECTORS if register in ("official", "legal") else ()
    idx = _connector_indices(sentences, muted)
    if idx:
        hits["connector_pile"] = [CONNECTOR_START.match(sentences[i]).group(1) for i in idx]
        touched.update(idx)
    return hits, touched


def _observations(sentences: list[str], body: str, register: str) -> list[str]:
    if len(sentences) < OBSERVE_MIN_SENTENCES:
        return []
    notes = []
    if not any(len(CYR_WORD.findall(s)) >= LONG_SENTENCE_WORDS for s in sentences):
        notes.append("no_long_sentences: no sentence of 25+ words (human prose has about 7x more)")
    if register not in FORMAL_REGISTERS and not PARTICLES.search(body):
        notes.append("no_particles: no л, даа, биз, билээ or шүү (observe only; never add them by default)")
    return notes


def analyze(text: str, register: str = "auto") -> dict:
    if register not in REGISTERS:
        raise ValueError(f"unknown register {register!r}; choose one of {', '.join(REGISTERS)}")
    pre, body, out = split_framing(text)
    units = prose_units(body)
    sentences, lines = [s for _, s in units], [n for n, _ in units]
    hits, touched = _style_hits(sentences, lines, register)
    muted = MUTED.get(register, frozenset())
    flags = {name: found for name, check in FLAG_CHECKS.items() if name not in muted and (found := check(body))}
    framing = [x for x in (pre, out) if x]
    if framing:
        flags = {"chat_framing": framing, **flags}
    level = "light" if register == "legal" else level_for(len(touched), len(sentences))
    report = {
        "register": register,
        "sentences": len(sentences),
        "problem_sentences": len(touched),
        "level": level,
        "types_found": len(hits) + len(flags),
        "hits": hits,
        "flags": flags,
        "observations": _observations(sentences, body, register),
    }
    if register == "legal":
        report["note"] = "Legal text: do not restyle. Remove chatbot leftovers; flag calques for the author."
    return report


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="mn_markers.py", description=__doc__.split("\n")[0])
    parser.add_argument("file", nargs="?", help="UTF-8 text file; reads stdin when omitted")
    parser.add_argument("--register", default="auto", choices=REGISTERS)
    args = parser.parse_args(argv[1:])
    try:
        if args.file:
            text = Path(args.file).read_text(encoding="utf-8")
        else:
            sys.stdin.reconfigure(encoding="utf-8")
            text = sys.stdin.read()
    except (OSError, UnicodeDecodeError) as exc:
        sys.stderr.write(f"mn_markers: cannot read input: {exc}\n")
        return 1
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.stdout.write(json.dumps(analyze(text, args.register), ensure_ascii=False, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
