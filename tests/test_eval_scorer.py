"""Metric fixtures: the eval scorer must fail known-bad rewrites and pass good ones.

No API needed. The bad rewrites are deliberately broken versions of case
inputs; the good ones come from references/examples.md or minimal correct fixes.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "eval"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import check_outputs as co  # noqa: E402
from mn_text import split_framing  # noqa: E402

CASES = {c["id"]: c for c in co.load_cases(Path(__file__).resolve().parent / "eval" / "cases.jsonl")}


def reply(rewrite: str, notes: str = "") -> str:
    return f"**Дүгнэлт:** ...\n\n**Засварласан хувилбар:**\n\n{rewrite}\n\n" + (f"**Анхаарах:** {notes}\n" if notes else "")


def body(case_id: str) -> str:
    return split_framing(CASES[case_id]["input_text"])[1]


BAD = [
    # (case id, reply, checks that must fail)
    ("A01-formal-essay", reply("Боловсролгүй хүнд өнөөдөр амьдрал хэцүү."),
     {"leave_alone", "no_labels", "register_floor"}),
    ("D01-petition", reply("Захирал Б.Сарантуяа. Миний хүү Д.Тэмүүлэн 2025-2026 онд 9б ангид сурдаг. Бид 11 дүгээр сарын "
                           "3-наас 14 хүртэл хөдөө явна. Хүүг чөлөөлөөч. Хичээлээ нөхнө.\nД.Ганбат"),
     {"leave_alone", "register_floor", "keep:Хүндэтгэсэн"}),
    ("D02-essay-stance", reply("Хүүхдийг багаас нь ном уншиж сургах нь эцэг эхийн хамгийн чухал үүрэг. Ном уншдаг хүүхэд асуулт "
                               "их асуудаг, бодож сэтгэх чадвар нь эрт хөгждөг. Бүх гэр бүлд номын сан байхгүй. Өдөрт ганц "
                               "хуудас уншиж өгвөл хүүхдийн ирээдүйд том хөрөнгө оруулалт болно."),
     {"leave_alone", "register_floor", "keep:болов уу"}),
    ("E01-facts-quote", reply("2025 оны 9 дүгээр сарын 15-нд Улаанбаатар хотод болсон чуулга уулзалтад 23 улсын 150 гаруй төлөөлөгч "
                              "оролцов. Чуулга уулзалтаар уур амьсгалын өөрчлөлтийн асуудлыг хэлэлцсэн. \"Бид хамтран ажиллах "
                              "ёстой\" гэж НҮБ-ын төлөөлөгч Мария Гарсиа хэлсэн. Уулзалтын төгсгөлд хамтарсан мэдэгдэлд гарын "
                              "үсэг зурсан."),
     {"numbers_preserved", "quotes_preserved"}),
    ("A04-personal-note", reply("Өнгөрсөн зун аав ээжтэйгээ хөдөө явлаа. Нутгаа тойрлоо. Уул усаа үзлээ."),
     {"leave_alone", "shape"}),
    ("H01-ai-essay-connector-pile", reply(CASES["H01-ai-essay-connector-pile"]["input_text"]),
     {"connector_pile_reduced"}),
    ("H03-ai-news-ghost-experts", reply(
        body("H03-ai-news-ghost-experts").replace("[номын сангийн нэр]", "Төв").replace(
            "гэж мэргэжилтнүүд үзэж байна", "гэж судлаач Д.Батбаяр үзэж байна")),
     {"no_new_names", "placeholders_kept", "keep:[номын сангийн нэр]", "flag:мэргэжилт"}),
    ("B02-ai-post-preamble", reply(CASES["B02-ai-post-preamble"]["input_text"]),
     {"remove:Иймэрхүү пост болно"}),
]

GOOD = [
    ("C01-translated-report", reply(
        "Өчигдөр сургууль дээр эцэг эхчүүдтэй уулзалт болсон. Уулзалтаар хүүхдүүдийн сурлагын асуудлыг хөндөж, олон эцэг эх "
        "санал хэлсэн бөгөөд багш нар саналыг нь хүлээн авсан. Цаашид хамтын ажиллагааг сайжруулах болно.")),
    ("A01-formal-essay", "**Дүгнэлт:** эсээ, засвар шаардлагагүй.\n\n**Анхаарах:** \"олон судлаачдын\" гэсэн хэсэгт эх сурвалж алга."),
    ("C02-letter-double-passive", reply(
        "Танай байгууллагын үйл ажиллагааг сайжруулах чиглэлээр хамтран ажиллах асуудлыг судлан үзэх зорилгоор уулзалт зохион "
        "байгуулахаар төлөвлөж байна. Энэхүү уулзалт нь хоёр талын хамтын ажиллагааг цаашид өргөжүүлэн бэхжүүлэхэд онцгой ач "
        "холбогдолтой юм.")),
    ("E01-facts-quote", reply(
        "2025 оны 9 дүгээр сарын 15-нд Улаанбаатар хотод болсон чуулга уулзалтад 23 улсын 140 гаруй төлөөлөгч оролцов. Чуулга "
        "уулзалтаар уур амьсгалын өөрчлөлтийн асуудлыг хэлэлцсэн. \"Бид хамтдаа ажиллах ёстой\" гэж НҮБ-ын төлөөлөгч Мария "
        "Гарсиа хэлсэн. Уулзалтын төгсгөлд хамтарсан мэдэгдэлд гарын үсэг зурсан.")),
    ("H03-ai-news-ghost-experts", reply(
        body("H03-ai-news-ghost-experts"),
        "\"гэж мэргэжилтнүүд үзэж байна\": аль мэргэжилтэн болохыг нэрлэх эсвэл энэ өгүүлбэрийг хасах хэрэгтэй.")),
    ("H08-idempotence", "**Дүгнэлт:** мэдээ, аль хэдийн монгол найруулгатай; засвар шаардлагагүй."),
]


class FixtureTest(unittest.TestCase):
    def test_bad_rewrites_fail_the_expected_checks(self):
        for cid, rep, must_fail in BAD:
            with self.subTest(cid):
                r = co.score_case(CASES[cid], rep)
                failed = {k for k, v in r["checks"].items() if v is False}
                self.assertFalse(r["pass"])
                self.assertTrue(must_fail <= failed, f"{cid}: expected {must_fail - failed} to fail; failed={failed}")

    def test_good_rewrites_pass(self):
        for cid, rep in GOOD:
            with self.subTest(cid):
                r = co.score_case(CASES[cid], rep)
                failed = [k for k, v in r["checks"].items() if v is False]
                self.assertTrue(r["pass"], f"{cid} failed: {failed} {r['checks'].get('problems', '')}")

    def test_split_reply_reads_no_change_verdict(self):
        rewrite, _ = co.split_reply("**Дүгнэлт:** албан бичиг, засвар шаардлагагүй.")
        self.assertIsNone(rewrite)

    def test_split_reply_finds_free_form_rewrite(self):
        src = CASES["C01-translated-report"]["input_text"]
        free = "Энд зассан текст байна, тайлбаргүй.\n\n" + src.replace("хийгдсэн", "болсон") + "\n\nАмжилт хүсье!"
        rewrite, commentary = co.split_reply(free, src)
        self.assertIn("уулзалт болсон", rewrite)
        self.assertIn("Амжилт", commentary)


class CasesFileTest(unittest.TestCase):
    def test_public_cases_carry_no_third_party_human_text(self):
        for c in CASES.values():
            self.assertFalse(c["source"].startswith("research/corpora/human"), c["id"])

    def test_every_case_has_checks_and_prompt(self):
        for c in CASES.values():
            with self.subTest(c["id"]):
                self.assertTrue(c["checks"])
                self.assertTrue(c["prompt"].strip())
                if c["category"] != "trigger":
                    self.assertIn(c["input_text"], c["prompt"])

    def test_at_least_twenty_cases_and_leave_alone_cases(self):
        self.assertGreaterEqual(len(CASES), 20)
        self.assertGreaterEqual(sum(1 for c in CASES.values() if c["checks"].get("leave_alone")), 10)


if __name__ == "__main__":
    unittest.main()
