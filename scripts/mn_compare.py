"""Compare an original Mongolian text with its rewrite: did the rewrite do harm?

Usage:
    python mn_compare.py ORIGINAL REWRITE [--allow-register-drop] [--allow-merge-split]

Prints JSON: "ok", a list of "problems", and metrics. A problem is any of:
    register_drop   fewer politeness or stance markers (Та, юм, билээ, шүү/даа,
                    softeners, courtesy formulas, honorifics) than the original
    new_label       a group label ("боловсролгүй хүн") the original did not have
    lower_rung      a derogatory-rung word ("гудрах") the original did not have
    numbers_changed a digit group added, dropped or changed
    quote_changed   a quoted span no longer appears verbatim
    much_shorter    under 70% of the original's words (blunt shortening)
    chopped         more and much shorter sentences (curt splitting)

Chat framing in the original (a preamble or closing offer to the requester) is
set aside first: removing it is expected. Use --allow-register-drop only when
the user asked for a more casual text, --allow-merge-split when sentence shape
was meant to change. This is the audit's mechanical half; it cannot judge
meaning or naturalness.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # sibling import under python -I

from mn_text import CYR, split_framing, split_sentences  # noqa: E402

WORDS = re.compile(rf"[{CYR}A-Za-z0-9]+")
NUMBERS = re.compile(r"\d+")
QUOTE = re.compile(r'"([^"\n]{3,})"|«([^»\n]{3,})»|“([^”\n]{3,})”')
B = rf"(?<![{CYR}])"
E = rf"(?![{CYR}])"

# Politeness and stance markers whose loss signals a register drop (SKILL.md
# principles 6 and 7, the tone guard).
REGISTER_MARKERS: dict[str, re.Pattern[str]] = {
    "Та-address": re.compile(
        rf"{B}(?:Та|Танд|Таны|Танаа|танаа|Таныг|Танаас|Танай|танай|тань|[Тт]а бүх[{CYR}]*){E}"
    ),
    "юм": re.compile(rf"{B}юм{E}"),
    "билээ": re.compile(rf"{B}билээ{E}"),
    "шүү/даа": re.compile(rf"{B}(?:шүү|даа|дээ|доо|дөө){E}"),
    "softener": re.compile(r"болов уу|гэж үзэж байна|гэж бодож байна|гэж боддог|байж болох|магадгүй"),
    "courtesy": re.compile(r"Хүндэтгэсэн|хүсье|Эрхэм|хүндэт|баярлалаа|талархал"),
    "honorific": re.compile(rf"{B}(?:морил|айлтга|бараалх|зоогло|айлда|дээдл)[{CYR}]*"),
}
LABEL = re.compile(
    rf"{B}(?:боловсролгүй|мэдлэггүй|ухаангүй|соёлгүй|хүмүүжилгүй|хариуцлагагүй|залхуу|хойрго|хоцрогдсон)"
    rf"\s+(?:хүн|хүмүүс|иргэд|ажилчид|залуус)[{CYR}]*",
    re.I,
)
LOWER_RUNG = re.compile(rf"{B}(?:гудра|чалчи|сажла|ховдоглон)[{CYR}]*", re.I)

MIN_LENGTH_RATIO = 0.7
MAX_SENTENCE_RATIO = 1.2
MIN_WORDS_PER_SENTENCE_RATIO = 0.8


def words(text: str) -> list[str]:
    return WORDS.findall(text)


def sentences(text: str) -> list[str]:
    return [s for s in split_sentences(text) if words(s)]


def chrf(hyp: str, ref: str, n_max: int = 6, beta: float = 2.0) -> float:
    """Character n-gram F-score (chrF, Popović 2015), whitespace ignored, 0-100."""
    h, r = re.sub(r"\s+", "", hyp), re.sub(r"\s+", "", ref)
    precisions, recalls = [], []
    for n in range(1, n_max + 1):
        hc = Counter(h[i:i + n] for i in range(len(h) - n + 1))
        rc = Counter(r[i:i + n] for i in range(len(r) - n + 1))
        if not hc or not rc:
            continue
        overlap = sum((hc & rc).values())
        precisions.append(overlap / sum(hc.values()))
        recalls.append(overlap / sum(rc.values()))
    if not precisions:
        return 0.0
    p, rr = sum(precisions) / len(precisions), sum(recalls) / len(recalls)
    return 0.0 if p + rr == 0 else 100 * (1 + beta**2) * p * rr / (beta**2 * p + rr)


def changed_words(a: str, b: str) -> int:
    sm = difflib.SequenceMatcher(a=words(a), b=words(b), autojunk=False)
    return sum(max(i2 - i1, j2 - j1) for op, i1, i2, j1, j2 in sm.get_opcodes() if op != "equal")


def marker_counts(text: str) -> Counter:
    return Counter({k: len(rx.findall(text)) for k, rx in REGISTER_MARKERS.items()})


def quoted_spans(text: str) -> list[str]:
    return [next(x for x in groups if x) for groups in QUOTE.findall(text)]


def _register_problems(body: str, rewrite: str) -> list[str]:
    before, after = marker_counts(body), marker_counts(rewrite)
    return [f"register_drop: {k} {before[k]}→{after[k]}" for k in REGISTER_MARKERS if after[k] < before[k]]


def _new_matches(rx: re.Pattern[str], body: str, rewrite: str) -> list[str]:
    old = {m.lower() for m in rx.findall(body)}
    return [m for m in rx.findall(rewrite) if m.lower() not in old]


def compare(
    original: str,
    rewrite: str,
    allow_register_drop: bool = False,
    allow_merge_split: bool = False,
    min_length_ratio: float = MIN_LENGTH_RATIO,
) -> dict:
    body = split_framing(original)[1] or original.strip()
    s_in, s_out = sentences(body), sentences(rewrite)
    n_in, n_out = len(words(body)), len(words(rewrite))
    length_ratio = n_out / max(n_in, 1)
    wps_ratio = (n_out / max(len(s_out), 1)) / max(n_in / max(len(s_in), 1), 1e-9)
    sentence_ratio = len(s_out) / max(len(s_in), 1)
    problems: list[str] = []
    if not allow_register_drop:
        problems += _register_problems(body, rewrite)
    problems += [f"new_label: {x}" for x in _new_matches(LABEL, body, rewrite)]
    problems += [f"lower_rung: {x}" for x in _new_matches(LOWER_RUNG, body, rewrite)]
    if Counter(NUMBERS.findall(body)) != Counter(NUMBERS.findall(rewrite)):
        problems.append("numbers_changed")
    problems += [f"quote_changed: {q[:40]}" for q in quoted_spans(body) if q not in rewrite]
    if length_ratio < min_length_ratio:
        problems.append(f"much_shorter: {length_ratio:.2f} of the original's words")
    if not allow_merge_split and sentence_ratio > MAX_SENTENCE_RATIO and wps_ratio < MIN_WORDS_PER_SENTENCE_RATIO:
        problems.append(f"chopped: {len(s_in)}→{len(s_out)} sentences")
    return {
        "ok": not problems,
        "problems": problems,
        "metrics": {
            "length_ratio": round(length_ratio, 2),
            "chrf": round(min(chrf(rewrite, body), chrf(body, rewrite)), 1),
            "changed_words": changed_words(body, rewrite),
            "sentences": [len(s_in), len(s_out)],
            "words_per_sentence_ratio": round(wps_ratio, 2),
        },
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="mn_compare.py", description=__doc__.split("\n")[0])
    parser.add_argument("original")
    parser.add_argument("rewrite")
    parser.add_argument("--allow-register-drop", action="store_true")
    parser.add_argument("--allow-merge-split", action="store_true")
    args = parser.parse_args(argv[1:])
    try:
        original = Path(args.original).read_text(encoding="utf-8")
        rewrite = Path(args.rewrite).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        sys.stderr.write(f"mn_compare: cannot read input: {exc}\n")
        return 1
    report = compare(original, rewrite, args.allow_register_drop, args.allow_merge_split)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.stdout.write(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
