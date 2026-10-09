"""Tests for scripts/mn_markers.py. Run: python -m unittest discover -s tests"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import mn_markers as m  # noqa: E402

# Acceptable formal school essay. A native speaker judged it fine; the skill
# must not treat its formulas, connectives, or topic "нь" as problems.
FORMAL_ESSAY = (
    "Өнөөгийн хурдацтай хөгжиж буй технологийн эрин үед боловсрол нь хүний "
    "амьдралд маш чухал үүрэг гүйцэтгэдэг юм. Боловсрол нь зөвхөн мэдлэг олж "
    "авах хэрэгсэл биш, харин хувь хүний хөгжил, нийгмийн дэвшил, эдийн засгийн "
    "өсөлтийн үндэс суурь юм. Мөн түүнчлэн, олон судлаачдын үзэж байгаагаар "
    "чанартай боловсрол нь ирээдүйн амжилтын түлхүүр болдог. Түүгээр ч "
    "зогсохгүй, сурагчид өөрсдийн мэдлэг, ур чадвараа хөгжүүлэх боломжтой "
    "болдог. Дүгнэж хэлэхэд, боловсрол бол бидний ирээдүйн гэрэлт замын эхлэл юм."
)

# Translated report: noun + хийгдэх, agentless passive, redundant plurals,
# four -сан endings in a row.
TRANSLATED_REPORT = (
    "Өчигдөр сургууль дээр эцэг эхчүүдтэй уулзалт хийгдсэн. Уулзалтаар "
    "хүүхдүүдийн сурлагын асуудлууд хөндөгдсөн. Олон эцэг эхчүүд санал хэлсэн. "
    "Багш нар саналуудыг хүлээн авсан. Цаашид хамтын ажиллагааны сайжруулалт "
    "хийгдэх болно."
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


class NounVerbTest(unittest.TestCase):
    def test_noun_plus_hiih(self):
        hits = m.check_noun_verb("Сайд нартай ярилцлага хийв. Туршилт хийгдэнэ. Уулзалт хийлээ.")
        self.assertEqual(len(hits), 3)

    def test_noun_plus_yavagdah(self):
        self.assertEqual(len(m.check_noun_verb("Мал төллөлт явагдаж байна.")), 1)

    def test_event_noun_with_yavagdah_is_native(self):
        self.assertEqual(m.check_noun_verb("Сургалт 10 дугаар сарын 20-нд явагдана."), [])
        self.assertEqual(m.check_noun_verb("Сургалт явагдана."), [])

    def test_lexicalised_noun_without_hiih_is_fine(self):
        self.assertEqual(m.check_noun_verb("Уулзалт амжилттай болов. Сургалтад хамрагдсан."), [])


class PassiveTest(unittest.TestCase):
    def test_agentless_passives_flagged_when_repeated(self):
        hits = m.check_passive("Асуудлууд хөндөгджээ. Концерт тоглогдоно.")
        self.assertEqual(len(hits), 2)

    def test_single_passive_not_flagged(self):
        self.assertEqual(m.check_passive("Хурал зохион байгуулагдсан."), [])

    def test_perception_verbs_are_native(self):
        text = "Уул харагдав. Тэгж санагдлаа. Дуу сонсогдов. Ингэж бодогдсон."
        self.assertEqual(m.check_passive(text), [])

    def test_notify_verb_is_not_passive(self):
        self.assertEqual(m.check_passive("Бид мэдэгдсэн. Тэд мэдэгдлээ."), [])


class GrammarTest(unittest.TestCase):
    def test_double_ni_in_one_sentence(self):
        hits = m.check_ni_overuse("Хөтөлбөр нь сурагчид нь тусалдаг. Би ирлээ.")
        self.assertEqual(len(hits), 1)

    def test_one_ni_per_sentence_is_native(self):
        text = "Хууль нь батлагдсан. Шүүх нь шийдсэн. Иргэд нь баярласан."
        self.assertEqual(m.check_ni_overuse(text), [])

    def test_ni_inside_word_is_ignored(self):
        self.assertEqual(m.check_ni_overuse("Миний нийтлэл нийгэмд хүрсэн."), [])

    def test_doubled_possessive(self):
        self.assertEqual(len(m.check_doubled_possessive("Таны бие лагшин тань сайн уу?")), 1)

    def test_plural_after_quantifier(self):
        hits = m.check_quantifier_plural("Олон хүмүүс ирсэн. Бүх оюутнууд суусан. Гурван ном авлаа.")
        self.assertEqual(len(hits), 2)

    def test_group_plural_without_quantifier_is_native(self):
        self.assertEqual(m.check_quantifier_plural("Багш нар, эцэг эхчүүд ирэв."), [])

    def test_bolon_in_list(self):
        self.assertEqual(len(m.check_bolon_list("Дорж, Дондог, болон Бат ирэв.")), 1)


class RhythmTest(unittest.TestCase):
    def test_san_run(self):
        text = "Бид гарсан. Уул руу явсан. Хоол идсэн. Тэгээд харилаа."
        self.assertEqual(len(m.check_ending_runs(text)), 1)

    def test_identical_last_word_run(self):
        text = "Бид гарч байна. Бид явж байна. Бид идэж байна."
        self.assertEqual(len(m.check_ending_runs(text)), 1)

    def test_varied_endings(self):
        self.assertEqual(m.check_ending_runs(NATURAL_TEXT), [])


class ResidueTest(unittest.TestCase):
    def test_chatbot_leftover(self):
        self.assertEqual(len(m.check_chatbot("Мэдээжийн хэрэг! Энэ сайн.")), 1)

    def test_unsourced_attribution(self):
        self.assertEqual(len(m.check_attribution("Олон судлаачдын үзэж байгаагаар энэ зөв.")), 1)

    def test_calqued_idiom(self):
        self.assertEqual(len(m.check_calqued_idioms("Ийм мэдрэмж төрлөө.")), 1)

    def test_formal_formulas_are_not_flagged(self):
        text = "Боловсрол чухал үүрэг гүйцэтгэдэг. Дүгнэж хэлэхэд сайн. Мөн түүнчлэн ирлээ."
        report = m.analyze(text)
        self.assertEqual(report["types_found"], 0)


class TypographyTest(unittest.TestCase):
    def test_dashes(self):
        self.assertEqual(len(m.check_dashes("Хууль — эцэст нь — батлагдлаа. 2020–2024")), 2)

    def test_range_dash_is_ignored(self):
        self.assertEqual(m.check_dashes("2020–2024 онд"), [])

    def test_title_case_heading(self):
        self.assertEqual(len(m.check_title_case("## Бидний Шинэ Үйлчилгээ\nТекст")), 1)
        self.assertEqual(m.check_title_case("## Бидний шинэ үйлчилгээ"), [])


class ReportTest(unittest.TestCase):
    def test_formal_essay_is_light(self):
        report = m.analyze(FORMAL_ESSAY)
        self.assertEqual(report["level"], "light")

    def test_translated_report_is_not_light(self):
        report = m.analyze(TRANSLATED_REPORT)
        self.assertGreaterEqual(report["types_found"], 4)
        self.assertNotEqual(report["level"], "light")

    def test_natural_text_is_clean(self):
        self.assertEqual(m.analyze(NATURAL_TEXT)["types_found"], 0)

    def test_level_thresholds(self):
        self.assertEqual(m.level_for(0), "light")
        self.assertEqual(m.level_for(2), "light")
        self.assertEqual(m.level_for(3), "selective")
        self.assertEqual(m.level_for(5), "selective")
        self.assertEqual(m.level_for(6), "full")

    def test_empty_text(self):
        self.assertEqual(m.analyze("")["types_found"], 0)


if __name__ == "__main__":
    unittest.main()
