"""Tests for scripts/mn_compare.py: a rewrite must not drop register, facts, or shape."""

import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import mn_compare as c  # noqa: E402
from test_mn_markers import FORMAL_ESSAY, TRANSLATED_REPORT  # noqa: E402

PETITION = (
    "Сургуулийн захирал Б.Сарантуяа танаа\n\n"
    "Миний хүү Д.Тэмүүлэн 2025-2026 оны хичээлийн жилд танай сургуулийн 9б ангид суралцаж байна. "
    "Гэр бүлийн шалтгаанаар бид 11 дүгээр сарын 3-наас 14-нийг хүртэл хөдөө орон нутагт явах болсон "
    "тул хүүг энэ хугацаанд хичээлээс чөлөөлж өгөхийг Танаас хүсье. Хоцорсон хичээлээ нөхөх талаар "
    "ангийн багштай нь тохиролцоно.\n\nХүндэтгэсэн,\nЭцэг Д.Ганбат"
)
STANCE = (
    "Миний бодлоор хүүхдийг багаас нь ном уншиж сургах нь эцэг эхийн хамгийн чухал үүрэг юм. "
    "Мэдээж бүх гэр бүлд номын сан байхгүй байж болох юм. Гэхдээ өдөрт ганц хуудас ч гэсэн "
    "хүүхэддээ уншиж өгвөл түүний ирээдүйд том хөрөнгө оруулалт болох болов уу гэж би боддог."
)
NEWS = (
    "2025 оны 9 дүгээр сарын 15-нд Улаанбаатар хотод болсон чуулга уулзалтад 23 улсын 140 гаруй "
    'төлөөлөгчид оролцсон. "Бид хамтдаа ажиллах ёстой" гэж НҮБ-ын төлөөлөгч Мария Гарсиа хэлсэн.'
)
NOTE = "Өнгөрсөн зун аав ээжтэйгээ хөдөө явж, нутгийнхаа уул усыг тойрч ирлээ."


class CompareTest(unittest.TestCase):
    def test_blunt_rewrite_fails(self):
        r = c.compare(FORMAL_ESSAY, "Боловсролгүй хүнд өнөөдөр амьдрал хэцүү.")
        self.assertFalse(r["ok"])
        kinds = {p.split(":")[0] for p in r["problems"]}
        self.assertTrue({"register_drop", "new_label", "much_shorter"} <= kinds, r["problems"])

    def test_light_fix_passes(self):
        r = c.compare(FORMAL_ESSAY, FORMAL_ESSAY.replace("олон судлаачдын", "олон судлаачийн"))
        self.assertTrue(r["ok"], r["problems"])
        self.assertGreater(r["metrics"]["chrf"], 95)

    def test_full_rewrite_of_translationese_passes(self):
        good = (
            "Өчигдөр сургууль дээр эцэг эхчүүдтэй уулзалт болсон. Уулзалтаар хүүхдүүдийн сурлагын "
            "асуудлыг хөндөж, олон эцэг эх санал хэлсэн бөгөөд багш нар саналыг нь хүлээн авсан. "
            "Цаашид хамтын ажиллагааг сайжруулах болно."
        )
        self.assertTrue(c.compare(TRANSLATED_REPORT, good)["ok"])

    def test_dropped_courtesy_fails(self):
        blunt = PETITION.replace("Танаас хүсье", "хүсч байна").replace("Хүндэтгэсэн,\n", "")
        r = c.compare(PETITION, blunt)
        self.assertIn("register_drop", " ".join(r["problems"]))

    def test_dropped_softeners_fail(self):
        flat = STANCE.replace(" юм.", ".").replace(" болох болов уу гэж би боддог", " болно")
        r = c.compare(STANCE, flat)
        self.assertFalse(r["ok"])
        self.assertIn("softener", " ".join(r["problems"]))

    def test_allow_register_drop(self):
        flat = STANCE.replace(" юм.", ".")
        self.assertTrue(c.compare(STANCE, flat, allow_register_drop=True)["ok"])

    def test_changed_number_fails(self):
        r = c.compare(NEWS, NEWS.replace("140", "150"))
        self.assertIn("numbers_changed", " ".join(r["problems"]))

    def test_changed_quote_fails(self):
        r = c.compare(NEWS, NEWS.replace("хамтдаа ажиллах", "хамтран ажиллах"))
        self.assertIn("quote_changed", " ".join(r["problems"]))

    def test_chopped_sentences_fail(self):
        chopped = "Өнгөрсөн зун аав ээжтэйгээ хөдөө явлаа. Нутгаа тойрлоо. Уул усаа үзлээ."
        r = c.compare(NOTE, chopped)
        self.assertIn("chopped", " ".join(r["problems"]))

    def test_allow_merge_split(self):
        chopped = "Өнгөрсөн зун аав ээжтэйгээ хөдөө явлаа. Нутгийнхаа уул усыг тойрч ирлээ."
        self.assertTrue(c.compare(NOTE, chopped, allow_merge_split=True)["ok"])

    def test_removing_chat_framing_is_not_shortening(self):
        original = "Мэдээж. Таны хүссэн пост доор байна:\n\n" + STANCE + "\n\nХэрэв өөр хувилбар хэрэгтэй бол хэлээрэй."
        self.assertTrue(c.compare(original, STANCE)["ok"])

    def test_lower_rung_word_fails(self):
        r = c.compare("Аав хоолоо идэв.", "Аав хоолоо гудрав.")
        self.assertIn("lower_rung", " ".join(r["problems"]))


class ChrfTest(unittest.TestCase):
    def test_identical_is_100(self):
        self.assertAlmostEqual(c.chrf(NOTE, NOTE), 100.0)

    def test_blunt_is_low(self):
        self.assertLess(c.chrf("Боловсролгүй хүнд өнөөдөр амьдрал хэцүү.", FORMAL_ESSAY), 40)


class CliTest(unittest.TestCase):
    def test_main_prints_json(self):
        with tempfile.TemporaryDirectory() as d:
            a, b = Path(d, "a.txt"), Path(d, "b.txt")
            a.write_text(FORMAL_ESSAY, encoding="utf-8")
            b.write_text("Боловсролгүй хүнд өнөөдөр амьдрал хэцүү.", encoding="utf-8")
            buf = io.StringIO()
            with redirect_stdout(buf):
                code = c.main(["mn_compare.py", str(a), str(b)])
        self.assertEqual(code, 0)
        self.assertIn('"ok": false', buf.getvalue())

    def test_main_reports_missing_file(self):
        self.assertEqual(c.main(["mn_compare.py", "missing-a.txt", "missing-b.txt"]), 1)


if __name__ == "__main__":
    unittest.main()
