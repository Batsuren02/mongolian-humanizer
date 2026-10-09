"""The skill's own examples must not invent facts: every number and name in an
"after" text must already be in its "before" text.

Several humanizers found their worked examples inventing details (blader/humanizer
#187, #306); examples teach more than rules, so they are checked mechanically.
"""

import re
import unittest
from pathlib import Path

REFS = Path(__file__).resolve().parent.parent / "references"
CAPITALIZED = re.compile(r"(?<![А-ЯӨҮЁа-яөүё])([А-ЯӨҮЁ][А-ЯӨҮЁа-яөүё]{2,})")
SENTENCE_START = re.compile(r"(?:^|[.!?…:]\s+|\n)\s*[«\"“(]?$")


def quote_block(text: str, start: int) -> str:
    """Join the ">"-quoted lines that begin at or after `start`."""
    lines, seen = [], False
    for line in text[start:].splitlines():
        if line.startswith(">"):
            seen = True
            lines.append(line.lstrip("> ").strip())
        elif seen and line.strip():
            break
    return " ".join(x for x in lines if x)


def pairs() -> list[tuple[str, str, str]]:
    """(label, before, after) from Before/After quotes and from examples.md sections."""
    out = []
    for path in sorted(REFS.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        for m in re.finditer(r"> \*\*Before:\*\*(.*?)\n> \*\*After:\*\*(.*?)(?:\n\n|\Z)", text, re.S):
            before = re.sub(r"\n>\s?", " ", m.group(1))
            after = re.sub(r"\n>\s?", " ", m.group(2))
            out.append((f"{path.name}:{text[:m.start()].count(chr(10)) + 1}", before, after))
    examples = (REFS / "examples.md").read_text(encoding="utf-8")
    for sec in re.split(r"\n(?=## \d)", examples)[1:]:
        i, r = sec.find("**Input"), sec.find("**Засварласан хувилбар:**")
        if i >= 0 and r >= 0:
            out.append((f"examples.md {sec.splitlines()[0]}", quote_block(sec, i), quote_block(sec, r)))
    return out


def names(text: str) -> set[str]:
    """Capitalized words that do not start a sentence: names, places, abbreviations."""
    found = set()
    for m in CAPITALIZED.finditer(text):
        if not SENTENCE_START.search(text[: m.start()]):
            found.add(m.group(1).lower())
    return found


class ExamplesDoNotInventTest(unittest.TestCase):
    def test_pairs_were_found(self):
        self.assertGreaterEqual(len(pairs()), 15)

    def test_no_new_numbers(self):
        for label, before, after in pairs():
            with self.subTest(label):
                new = set(re.findall(r"\d+", after)) - set(re.findall(r"\d+", before))
                self.assertFalse(new, f"{label}: numbers not in the input: {new}")

    def test_no_new_names(self):
        for label, before, after in pairs():
            with self.subTest(label):
                known = names(before) | {w.lower() for w in CAPITALIZED.findall(before)}
                new = {n for n in names(after) if not any(k[:4] == n[:4] for k in known)}
                self.assertFalse(new, f"{label}: names not in the input: {new}")


if __name__ == "__main__":
    unittest.main()
