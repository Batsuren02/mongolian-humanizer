"""Write the `claude plugin eval` suite (evals/) from tests/eval/cases.jsonl.

Usage: python tests/eval/build_plugin_evals.py

Each non-trigger case gets an `llm` grader whose rubric embeds the original
text and the case's checks as PASS/FAIL conditions (regex graders cannot tell
the rewrite from the explanation, which quotes the original), plus a
`tool_used` indicator that the skill fired. Trigger cases get `tool_used`
graders scored in both arms; run them with `--tag trigger --ablation none`.
The deterministic scorer (check_outputs.py) stays the precise instrument;
this suite measures the same cases through the official runner.
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
EVALS = REPO / "evals"
SKILL_FIRED = '"skill"\\s*:\\s*"(?:[\\w-]+:)?mongolian-humanizer"'
MAX_TURNS = 25

ALWAYS = [
    "Every number, name, date and quotation of the original is unchanged, and nothing is added that the original "
    "does not say (no new fact, source, example, opinion or person).",
    "The text is not made blunter, colder or lower in register: Та-forms, courtesy formulas, softeners "
    "(болов уу, гэж үзэж байна), particles (юм, билээ, шүү, даа) and honorifics of the original survive.",
    "Paired words, balanced clauses and fixed formal phrases are not cut as 'redundant'.",
]


def _q(text: str) -> str:
    return json.dumps(text, ensure_ascii=False)


def conditions(case: dict) -> list[str]:
    chk = case["checks"]
    out = []
    if chk.get("leave_alone"):
        out.append("The reply says the text needs no change, or changes at most a few words "
                   f"(about {chk.get('max_changed_words', 0)}), each a clear error, not a style preference.")
    for ph in chk.get("must_keep", []):
        out.append(f"The final text still contains {_q(ph)}.")
    for ph in chk.get("must_remove", []):
        out.append(f"The final text (not the explanation) no longer contains {_q(ph)}.")
    for ph in chk.get("must_flag", []):
        out.append(f"The reply points out {_q(ph)} to the author (for example in an Анхаарах note).")
    if chk.get("flag_any"):
        out.append("The reply tells the author the voice is generic and suggests where their own example or view "
                   "would go, without writing that example for them.")
    if chk.get("connector_pile_reduced"):
        out.append("Fewer sentences start with a stacked connector (Мөн, Иймд, Юуны өмнө, Түүнчлэн...); "
                   "the sentences are joined or varied instead.")
    if chk.get("placeholders_kept"):
        out.append("Every [placeholder] of the original is kept, not filled with invented details.")
    if chk.get("min_len_ratio"):
        out.append(f"The final text keeps at least about {int(chk['min_len_ratio'] * 100)}% of the original's length "
                   "(chat lines addressed to the requester do not count).")
    if chk.get("allow_register_drop"):
        out.append("The user asked for a casual style, so a lower register is correct here.")
    if chk.get("explanation_language") == "en":
        out.append("Explanations are in English; the rewritten text is in Mongolian Cyrillic.")
    if case["id"].startswith("F01"):
        out.append("The reply is only the final Mongolian text: no headings, labels or explanations.")
    if case["id"].startswith("D05"):
        out.append("The Latin-script text is not converted to Cyrillic.")
    return out


def rubric(case: dict) -> str:
    conds = conditions(case)
    if not case["checks"].get("allow_register_drop"):
        conds += ALWAYS
    lines = [
        "You are grading an editor's reply to a request to make Mongolian text read naturally.",
        "",
        "Original text:",
        "<<<",
        case["input_text"],
        ">>>",
        "",
        f"Expected behaviour: {case['expected']}",
        "",
        "PASS only if all of these hold:",
        *[f"- {c}" for c in conds],
        "",
        "FAIL if any of them is violated. Judge the final rewritten text, not phrases the reply quotes from the "
        "original while explaining its changes.",
    ]
    return "\n".join(lines)


def frontmatter(fields: dict) -> str:
    body = "\n".join(f"{k}: {v}" for k, v in fields.items())
    return f"---\n{body}\n---\n"


def write_case(case: dict) -> None:
    d = EVALS / case["id"]
    (d / "graders").mkdir(parents=True, exist_ok=True)
    tags = [case["category"]] + (["trigger"] if case["category"] == "trigger" else [])
    (d / "prompt.md").write_text(
        frontmatter({
            "description": _q(case["expected"]),
            "tags": json.dumps(sorted(set(tags))),
            "max_turns": MAX_TURNS,
            "allowed_tools": "[Read, Glob, Grep, Skill]",
        }) + "\n" + case["prompt"].strip() + "\n",
        encoding="utf-8", newline="\n",
    )
    if case["category"] == "trigger":
        should = case["checks"]["should_trigger"]
        fields = {"type": "tool_used", "tool": "Skill", "input_match": f"'{SKILL_FIRED}'", "arm": "both"}
        if not should:
            fields.update({"min": 0, "max": 0})
        (d / "graders" / "skill-trigger.md").write_text(frontmatter(fields), encoding="utf-8", newline="\n")
        return
    (d / "graders" / "behaviour.md").write_text(
        frontmatter({"type": "llm"}) + "\n" + rubric(case) + "\n", encoding="utf-8", newline="\n")
    (d / "graders" / "skill-fired.md").write_text(
        frontmatter({"type": "tool_used", "tool": "Skill", "input_match": f"'{SKILL_FIRED}'"}),
        encoding="utf-8", newline="\n")


def main() -> int:
    cases = [json.loads(ln) for ln in (HERE / "cases.jsonl").read_text(encoding="utf-8").splitlines() if ln.strip()]
    for old in EVALS.iterdir() if EVALS.exists() else []:
        if old.is_dir() and (old / "prompt.md").exists():
            shutil.rmtree(old)
    for case in cases:
        write_case(case)
    sys.stdout.write(f"wrote {len(cases)} cases to {EVALS}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
