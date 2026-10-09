"""Packaging checks that `claude plugin validate` skips for a root SKILL.md:
frontmatter limits, version sync, reference links, and the eval suite's sync.
"""

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
LINK = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")


def frontmatter(text: str) -> dict[str, str]:
    """Top-level keys of a simple YAML frontmatter (block scalars joined)."""
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        raise ValueError("no frontmatter")
    fields: dict[str, str] = {}
    key = None
    for line in m.group(1).splitlines():
        top = re.match(r"([A-Za-z_]+):\s*(.*)$", line)
        if top and not line.startswith(" "):
            key = top.group(1)
            fields[key] = top.group(2).strip().strip('"|')
        elif key:
            fields[key] = (fields[key] + " " + line.strip()).strip()
    return fields


class SkillFrontmatterTest(unittest.TestCase):
    def test_name_matches_plugin(self):
        self.assertEqual(frontmatter(SKILL)["name"], "mongolian-humanizer")

    def test_description_within_limits(self):
        desc = frontmatter(SKILL)["description"]
        self.assertLessEqual(len(desc), 1024)
        self.assertNotRegex(desc, r"[<>]")
        for verb in ("найруулах", "засах", "proofread", "humanize"):
            self.assertIn(verb, desc)

    def test_body_is_short(self):
        self.assertLess(len(SKILL.splitlines()), 500)


class VersionSyncTest(unittest.TestCase):
    def test_versions_agree(self):
        skill_version = re.search(r'version:\s*"([^"]+)"', SKILL).group(1)
        plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(plugin["version"], skill_version)
        self.assertIn(f"**{skill_version}**", (ROOT / "README.md").read_text(encoding="utf-8"))


class ReferenceLinksTest(unittest.TestCase):
    def test_every_reference_is_linked_from_skill(self):
        for ref in sorted((ROOT / "references").glob("*.md")):
            with self.subTest(ref.name):
                self.assertIn(f"references/{ref.name}", SKILL)

    def test_relative_links_resolve(self):
        for doc in [ROOT / "SKILL.md", ROOT / "README.md", *sorted((ROOT / "references").glob("*.md"))]:
            for target in LINK.findall(doc.read_text(encoding="utf-8")):
                if target.startswith(("http://", "https://", "mailto:")):
                    continue
                with self.subTest(f"{doc.name} -> {target}"):
                    self.assertTrue((doc.parent / target).exists())

    def test_scripts_named_in_skill_exist(self):
        for script in re.findall(r"scripts/(\w+\.py)", SKILL):
            with self.subTest(script):
                self.assertTrue((ROOT / "scripts" / script).exists())


class EvalSuiteSyncTest(unittest.TestCase):
    def test_every_case_has_a_plugin_eval_directory(self):
        cases = [json.loads(x) for x in (ROOT / "tests" / "eval" / "cases.jsonl").read_text(encoding="utf-8").splitlines() if x]
        for c in cases:
            with self.subTest(c["id"]):
                d = ROOT / "evals" / c["id"]
                self.assertTrue((d / "prompt.md").exists(), "run tests/eval/build_plugin_evals.py")
                self.assertTrue(any((d / "graders").glob("*.md")))


if __name__ == "__main__":
    unittest.main()
