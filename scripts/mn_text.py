"""Shared text helpers for the mongolian-humanizer scripts (stdlib only).

Sentence splitting, sentence-final word classes, and detection of chat framing
(a preamble or closing offer addressed to the person who asked a chatbot,
rather than to the text's real reader).
"""

from __future__ import annotations

import re

CYR = "А-Яа-яЁёӨөҮү"
WORD = rf"[{CYR}A-Za-z]"
CYR_WORD = re.compile(rf"[{CYR}]+")
SENTENCE_BREAK = re.compile(r"(?<=[.!?…])\s+|\s*\n\s*")
PARAGRAPH_BREAK = re.compile(r"\n\s*\n")
HORIZONTAL_RULE = re.compile(r"^\s*(?:---+|\*\*\*+|___+)\s*$", re.M)
LEADING_MARKUP = re.compile(r"^(?:\s*(?:[>#•*\-–—]+|\d{1,2}[.)](?=\s)))*\s*")
HARD_WRAP = re.compile(r"(?<=[а-яөүёa-z,])[ \t]*\n[ \t]*(?=[а-яөүёa-z])")

# Sentence-final words that are auxiliaries or particles: a run of them is native.
AUXILIARY_ENDINGS = frozenset((
    "байна", "байсан", "байлаа", "байв", "байжээ", "байдаг", "байх", "болно", "юм",
    "билээ", "бэ", "вэ", "уу", "үү", "юу", "даа", "дээ", "доо", "дөө", "л", "шүү",
    "биз", "минь", "шиг", "мэт", "чадна",
))
HABITUAL = re.compile(r"(?:даг|дэг|дог|дөг)$")
MODAL_PREDICATES = frozenset(("хэрэгтэй", "шаардлагатай", "боломжтой", "чухал", "зайлшгүй"))

# Cues measured on 83 AI replies and 139 human texts (references/ai-output.md, A1).
PREAMBLE_CUES = re.compile(
    r"доор|энд\b|танд|таны хүссэн|бичлээ|бичиж өгье|бэлтгэлээ|бэлтгэж өгье|"
    r"санал болгож байна|жишээ болгон|загвар(?:ыг)?\s|хувилбар(?:ыг)?\s|мэдээж|^за[,!.]?\s",
    re.I,
)
OUTRO_CUES = re.compile(
    r"хэрэгтэй бол|тохируулж|өөрчилж|нэмж оруулж|засварлаж|хэлээрэй|мэдэгдээрэй|"
    r"бичээрэй|хүсвэл|оруулаарай|солиорой|бөглөөрэй|туслах(?:ад)? бэлэн|тустай байх|"
    r"(?:болгож|бичиж|засаж) өг(?:нө|ье)",
    re.I,
)
LETTER_OPENINGS = ("хүндэт", "эрхэм", "хаана", "хэнд", "хэнээс", "сайн байна уу")


def _unwrap(text: str) -> str:
    """Join hard-wrapped lines: a line ending mid-sentence before a lowercase word."""
    return HARD_WRAP.sub(" ", text.strip())


def split_sentences(text: str) -> list[str]:
    """Split on terminal punctuation and on line breaks (headings, list items)."""
    return [s.strip() for s in SENTENCE_BREAK.split(_unwrap(text)) if s.strip()]


def prose_units(text: str, min_words: int = 2) -> list[tuple[int, str]]:
    """(line number, sentence) for sentences of at least min_words Cyrillic words.

    List and heading markup is removed. The line number lets callers keep
    checks such as ending runs inside one paragraph: a column of one-line
    items ("2-р сард ... зохион байгуулсан.") is a list, not a run.
    """
    units = []
    lines = [ln for ln in _unwrap(text).splitlines() if ln.strip()]
    for n, line in enumerate(lines):
        for s in SENTENCE_BREAK.split(line.strip()):
            bare = LEADING_MARKUP.sub("", s).replace("**", "").strip()
            if len(CYR_WORD.findall(bare)) >= min_words:
                units.append((n, bare))
    return units


def prose_sentences(text: str, min_words: int = 2) -> list[str]:
    return [s for _, s in prose_units(text, min_words)]


def last_word(sentence: str) -> str:
    words = CYR_WORD.findall(sentence.lower())
    return words[-1] if words else ""


def is_generic_ending(sentence: str) -> bool:
    """A general-truth (-даг) or prescriptive (хэрэгтэй, шаардлагатай...) ending.

    "-даг юм" ends in "юм" and is a deliberate stance, so it does not count.
    """
    w = last_word(sentence)
    return bool(HABITUAL.search(w)) or w in MODAL_PREDICATES


def split_framing(text: str) -> tuple[str, str, str]:
    """Return (preamble, body, outro): chat lines addressed to the requester.

    A preamble is a short first paragraph ending in ":" or using a cue such as
    "доор", "таны хүссэн", "хувилбар". An outro is a short last paragraph
    offering further help ("хэрэгтэй бол хэлээрэй"). Letter salutations are
    never a preamble. Needs three or more paragraphs.
    """
    paras = [p for p in PARAGRAPH_BREAK.split(text.strip()) if p.strip()]
    pre = out = ""
    if len(paras) >= 3:
        first = paras[0].strip()
        if (
            len(first.split()) <= 40
            and not first.startswith("#")
            and not first.lower().startswith(LETTER_OPENINGS)
            and (first.endswith(":") or PREAMBLE_CUES.search(first))
        ):
            pre = paras.pop(0)
    while len(paras) >= 2:
        last = paras[-1].strip()
        if HORIZONTAL_RULE.fullmatch(last):
            paras.pop()
            continue
        if OUTRO_CUES.search(last) and len(last.split()) <= 80:
            out = last + ("\n\n" + out if out else "")
            paras.pop()
            continue
        break
    return pre.strip(), "\n\n".join(paras).strip(), out.strip()
