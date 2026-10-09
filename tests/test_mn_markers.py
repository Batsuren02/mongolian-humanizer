"""Tests for scripts/mn_markers.py. Run: python -m unittest discover -s tests"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import mn_markers as m  # noqa: E402

ROBOTIC_ESSAY = (
    "Өнөөгийн хурдацтай хөгжиж буй технологийн эрин үед боловсрол нь хүний "
    "амьдралд маш чухал үүрэг гүйцэтгэдэг юм. Боловсрол нь зөвхөн мэдлэг олж "
    "авах хэрэгсэл биш, харин хувь хүний хөгжил, нийгмийн дэвшил, эдийн засгийн "
    "өсөлтийн үндэс суурь юм. Мөн түүнчлэн, олон судлаачдын үзэж байгаагаар "
    "чанартай боловсрол нь ирээдүйн амжилтын түлхүүр болдог. Түүгээр ч "
    "зогсохгүй, сурагчид өөрсдийн мэдлэг, ур чадвараа хөгжүүлэх боломжтой "
    "болдог. Дүгнэж хэлэхэд, боловсрол бол бидний ирээдүйн гэрэлт замын эхлэл юм."
)

NATURAL_TEXT = (
    "Өчигдөр ажлаасаа эрт гараад ээжийнхээ гэрт очлоо. "
    "Ээж бууз хийчихсэн хүлээж байсан. Хоёулаа цай уунгаа удаан ярилцав."
)


class SplitSentencesTest(unittest.TestCase):
    def test_splits_on_terminal_punctuation(self):
        self.assertEqual(
            m.split_sentences("Нэг. Хоёр! Гурав? Дөрөв"),
            ["Нэг.", "Хоёр!", "Гурав?", "Дөрөв"],
        )


class CheckTest(unittest.TestCase):
    def test_double_ni_in_one_sentence(self):
        hits = m.check_ni_overuse("Хөтөлбөр нь сурагчид нь тусалдаг. Би ирлээ.")
        self.assertEqual(len(hits), 1)

    def test_ni_inside_word_is_ignored(self):
        self.assertEqual(m.check_ni_overuse("Миний нийтлэл нийгэмд хүрсэн."), [])

    def test_stock_phrase_found_case_insensitive(self):
        hits = m.check_stock_phrases("Дүгнэж хэлэхэд бүх зүйл сайн.")
        self.assertIn("дүгнэж хэлэхэд", [h.lower() for h in hits])

    def test_plural_after_quantifier(self):
        hits = m.check_quantifier_plural("Олон хүмүүс ирсэн. Бүх оюутнууд суусан. Гурван ном авлаа.")
        self.assertEqual(len(hits), 2)

    def test_dashes(self):
        self.assertEqual(len(m.check_dashes("Хууль — эцэст нь — батлагдлаа. 2020–2024")), 2)

    def test_range_dash_is_ignored(self):
        self.assertEqual(m.check_dashes("2020–2024 онд"), [])

    def test_monotonous_endings(self):
        text = "Бид гарсан байна. Бид явсан байна. Бид идсэн байна."
        self.assertEqual(len(m.check_monotonous_endings(text)), 1)

    def test_title_case_heading(self):
        self.assertEqual(len(m.check_title_case("## Бидний Шинэ Үйлчилгээ\nТекст")), 1)
        self.assertEqual(m.check_title_case("## Бидний шинэ үйлчилгээ"), [])

    def test_dense_ni_across_sentences(self):
        text = "Хууль нь батлагдсан. Шүүх нь шийдсэн. Иргэд нь баярласан. Бид ирлээ."
        self.assertEqual(len(m.check_ni_overuse(text)), 3)

    def test_frequent_ending_not_consecutive(self):
        text = "Нэг юм. Хоёр байна. Гурав юм. Дөрөв гэв. Тав юм."
        self.assertEqual(m.check_monotonous_endings(text), ["юм"])

    def test_reflexive_doubling_across_comma(self):
        self.assertEqual(len(m.check_calques("Сурагчид өөрсдийн мэдлэг, ур чадвараа хөгжүүлнэ.")), 1)

    def test_phrase_families_counted_separately(self):
        fams = m.stock_phrase_families("Мөн түүнчлэн энэ чухал үүрэг гүйцэтгэдэг. Дүгнэж хэлэхэд сайн.")
        self.assertEqual(len(fams), 3)

    def test_bolon_in_list(self):
        self.assertEqual(len(m.check_bolon_list("Дорж, Дондог, болон Бат ирэв.")), 1)


class ReportTest(unittest.TestCase):
    def test_robotic_essay_needs_full_rewrite(self):
        report = m.analyze(ROBOTIC_ESSAY)
        self.assertGreaterEqual(report["types_found"], 6)
        self.assertEqual(report["level"], "full")

    def test_natural_text_is_light(self):
        report = m.analyze(NATURAL_TEXT)
        self.assertLessEqual(report["types_found"], 2)
        self.assertEqual(report["level"], "light")

    def test_level_thresholds(self):
        self.assertEqual(m.level_for(0), "light")
        self.assertEqual(m.level_for(2), "light")
        self.assertEqual(m.level_for(3), "selective")
        self.assertEqual(m.level_for(5), "selective")
        self.assertEqual(m.level_for(6), "full")

    def test_empty_text(self):
        report = m.analyze("")
        self.assertEqual(report["types_found"], 0)


if __name__ == "__main__":
    unittest.main()
