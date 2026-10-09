"""Deterministic scorer for mongolian-humanizer eval outputs.

Usage:
    python tests/eval/check_outputs.py OUTPUT_DIR [--cases tests/eval/cases.jsonl]

OUTPUT_DIR holds one file per case, named <case id>.txt, with the model's full
reply (any runner: a subagent, the API, a pasted chat). Trigger cases
(category "trigger") are scored by `claude plugin eval` (evals/), not here.

Checks, each only when the case sets it:
    leave_alone          reply says "засвар шаардлагагүй" or changes <= max_changed_words
    must_keep / must_remove   phrases that must survive / disappear in the rewrite
    must_flag            phrase mentioned outside the rewrite (Анхаарах etc.)
    flag_any             at least one of these words outside the rewrite
    min_len_ratio / max_len_ratio   rewrite words / input words (blunt cuts, padding)
    numbers_preserved    same digit groups in input and rewrite
    placeholders_kept    every [placeholder] of the input survives
    no_new_names         no new "Д.Батбаяр"-style name
    connector_pile_reduced   fewer piled sentence-initial connectors than the input
    mn_markers_must_decrease fewer style hits than the input
    explanation_language "en": commentary in English
Always on for a rewrite: quotes verbatim, no register drop (unless
allow_register_drop), no curt splitting (unless allow_merge_split), no new
group labels or lower-rung words, Cyrillic output for Cyrillic input.

Thresholds are seeds from four worked example pairs (references/examples.md);
re-fit them on the first batch of approved outputs.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
import mn_compare  # noqa: E402
import mn_markers  # noqa: E402
from mn_text import CYR, split_framing  # noqa: E402

NO_CHANGE = re.compile(r"засвар\s+шаардлагагүй|no changes? (?:are )?needed", re.I)
REWRITE_HEAD = re.compile(r"Засварласан хувилбар|Rewritten version|Revised (?:version|text)", re.I)
AFTER_REWRITE_HEAD = re.compile(r"^\s*(?:\*\*|#+\s*|\d+\.\s*)*(?:Анхаарах|Notes?|Caveats?)\b", re.I | re.M)
PARAGRAPH = re.compile(r"\n\s*\n")
NAME = re.compile(r"(?<![А-ЯӨҮа-яөүё])[А-ЯӨҮ]\.\s?[А-ЯӨҮ][а-яөүё]+")
PLACEHOLDER = re.compile(r"\[[^\]\n]{1,60}\]")


def split_reply(reply: str, src: str = "") -> tuple[str | None, str]:
    """Return (rewrite, commentary); rewrite is None when the reply declines to change.

    An explicit rewrite heading wins; then a "no changes needed" verdict;
    otherwise (free-form replies, as from a no-skill baseline) the run of
    paragraphs most similar to the input by chrF is taken as the rewrite.
    """
    m = REWRITE_HEAD.search(reply)
    if m:
        rest = re.sub(r"^[\s:*#)\]]+", "", reply[m.end():])
        end = AFTER_REWRITE_HEAD.search(rest)
        rewrite = rest[: end.start()] if end else rest
        commentary = reply[: m.start()] + (rest[end.start():] if end else "")
        return _strip_quote_marks(rewrite), commentary
    if NO_CHANGE.search(reply):
        return None, reply
    if not src:
        return _strip_quote_marks(reply), ""
    return best_span(reply, src)


def best_span(reply: str, src: str) -> tuple[str, str]:
    paras = [p for p in PARAGRAPH.split(reply.strip()) if p.strip()]
    n_src = len([p for p in PARAGRAPH.split(src.strip()) if p.strip()])
    best, best_score = (0, len(paras)), -1.0
    for i in range(len(paras)):
        for j in range(i + 1, min(len(paras), i + n_src + 3) + 1):
            score = mn_compare.chrf(_strip_quote_marks("\n\n".join(paras[i:j])), src)
            if score > best_score:
                best, best_score = (i, j), score
    i, j = best
    return _strip_quote_marks("\n\n".join(paras[i:j])), "\n\n".join(paras[:i] + paras[j:])


def _strip_quote_marks(text: str) -> str:
    return "\n".join(re.sub(r"^\s*>\s?", "", ln) for ln in text.strip().splitlines()).strip()


def _style_hit_total(text: str) -> int:
    return sum(len(v) for v in mn_markers.analyze(text)["hits"].values())


def _content_checks(chk: dict, src: str, body: str, rewrite: str | None, effective: str, commentary: str) -> dict:
    results: dict[str, bool | str] = {}
    for ph in chk.get("must_keep", []):
        results[f"keep:{ph}"] = ph in effective
    for ph in chk.get("must_remove", []):
        results[f"remove:{ph}"] = ph not in effective
    for ph in chk.get("must_flag", []):
        results[f"flag:{ph}"] = ph.lower() in commentary.lower()
    if chk.get("flag_any"):
        results["flag_any"] = any(w.lower() in commentary.lower() for w in chk["flag_any"])
    if rewrite is not None:
        ratio = len(mn_compare.words(rewrite)) / max(len(mn_compare.words(body)), 1)
        results["len_ratio_value"] = f"{ratio:.2f}"
        if "min_len_ratio" in chk:
            results["min_len_ratio"] = ratio >= chk["min_len_ratio"]
        if "max_len_ratio" in chk:
            results["max_len_ratio"] = ratio <= chk["max_len_ratio"]
    if chk.get("numbers_preserved"):
        results["numbers_preserved"] = Counter(re.findall(r"\d+", body)) == Counter(re.findall(r"\d+", effective))
    if chk.get("placeholders_kept"):
        results["placeholders_kept"] = all(p in effective for p in PLACEHOLDER.findall(body))
    if chk.get("no_new_names"):
        results["no_new_names"] = not (set(NAME.findall(effective)) - set(NAME.findall(src)))
    if chk.get("connector_pile_reduced"):
        before, after = mn_markers.check_connector_pile(body), mn_markers.check_connector_pile(effective)
        results["connector_pile_reduced"] = not after or len(after) < len(before)
    if chk.get("mn_markers_must_decrease"):
        results["mn_markers_decrease"] = _style_hit_total(effective) < _style_hit_total(src)
    if chk.get("explanation_language") == "en":
        results["explains_in_english"] = len(re.findall(r"[A-Za-z]{3,}", commentary)) >= 10
    return results


def _harm_checks(chk: dict, src: str, body: str, rewrite: str) -> dict:
    """Register, facts and shape: mn_compare plus a Cyrillic-output check."""
    report = mn_compare.compare(
        body, rewrite,
        allow_register_drop=chk.get("allow_register_drop", False),
        allow_merge_split=chk.get("allow_merge_split", False),
        min_length_ratio=0.0,  # length is judged per case above
    )
    kinds = {p.split(":")[0] for p in report["problems"]}
    results: dict[str, bool | str] = {
        "register_floor": "register_drop" not in kinds,
        "no_labels": not kinds & {"new_label", "lower_rung"},
        "quotes_preserved": "quote_changed" not in kinds,
        "shape": "chopped" not in kinds,
        "chrf_value": str(report["metrics"]["chrf"]),
    }
    if report["problems"]:
        results["problems"] = "; ".join(report["problems"])
    latin_in = len(re.findall(r"[A-Za-z]", src)) > len(re.findall(rf"[{CYR}]", src))
    if not latin_in:
        cyr, lat = len(re.findall(rf"[{CYR}]", rewrite)), len(re.findall(r"[A-Za-z]", rewrite))
        results["cyrillic"] = lat - len(re.findall(r"[A-Za-z]", src)) <= 0.05 * max(cyr + lat, 1)
    return results


def score_case(case: dict, reply: str) -> dict:
    chk, src = case["checks"], case["input_text"]
    rewrite, commentary = split_reply(reply, src)
    effective = src if rewrite is None else rewrite
    # Chat framing addressed to the requester is expected to go, so length,
    # register and placeholders are compared against the body only.
    body = split_framing(src)[1] or src
    results: dict[str, bool | str] = {}
    if chk.get("leave_alone"):
        n = 0 if rewrite is None else mn_compare.changed_words(src, rewrite)
        results["leave_alone"] = rewrite is None or n <= chk.get("max_changed_words", 0)
        results["changed_words"] = str(n)
    results.update(_content_checks(chk, src, body, rewrite, effective, commentary))
    if rewrite is not None:
        results.update(_harm_checks(chk, src, body, rewrite))
    bools = [v for v in results.values() if isinstance(v, bool)]
    return {"id": case["id"], "category": case["category"], "pass": all(bools),
            "score": sum(bools) / len(bools) if bools else 1.0, "checks": results}


def load_cases(path: Path) -> list[dict]:
    return [json.loads(ln) for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]


def main() -> int:
    ap = argparse.ArgumentParser(description="Score saved replies against tests/eval/cases.jsonl")
    ap.add_argument("outputs", help="directory of <case id>.txt replies")
    ap.add_argument("--cases", default=str(HERE / "cases.jsonl"))
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    out_dir = Path(args.outputs)
    if not out_dir.is_dir():
        sys.stderr.write(f"check_outputs: not a directory: {out_dir}\n")
        return 1
    rows = []
    for c in load_cases(Path(args.cases)):
        if c["category"] == "trigger":
            continue
        f = out_dir / f"{c['id']}.txt"
        if not f.exists():
            print(f"  {c['id']:32s} MISSING")
            continue
        r = score_case(c, f.read_text(encoding="utf-8"))
        rows.append(r)
        failed = [k for k, v in r["checks"].items() if v is False]
        print(f"  {r['id']:32s} {'PASS' if r['pass'] else 'FAIL'} {r['score']:.2f} {' '.join(failed)}")
    if not rows:
        return 1
    by_cat = Counter(r["category"] for r in rows)
    passed = Counter(r["category"] for r in rows if r["pass"])
    print("\nBy category: " + ", ".join(f"{k} {passed[k]}/{n}" for k, n in sorted(by_cat.items())))
    print(f"Overall: {sum(r['pass'] for r in rows)}/{len(rows)} cases pass; "
          f"mean score {sum(r['score'] for r in rows) / len(rows):.2f}")
    (out_dir / "_scores.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
