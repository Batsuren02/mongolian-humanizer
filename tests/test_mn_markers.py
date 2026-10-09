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

# Constructed in the shape of current LLM essays (references/ai-output.md):
# sentence-initial connectors and generic -даг / modal endings.
AI_ESSAY = (
    "Боловсрол бол хүний хөгжлийн үндэс юм. Юуны өмнө, боловсрол хүнд мэдлэг "
    "олгодог. Мөн боловсрол хүний ертөнцийг үзэх үзлийг тэлдэг. Мөн сургууль "
    "нийгэмших ур чадварыг хөгжүүлдэг. Иймд боловсролд анхаарах хэрэгтэй. "
    "Иймд залуус суралцахад хичээх шаардлагатай."
)

# A chat reply: preamble and closing offer addressed to the requester.
CHAT_REPLY = (
    "Мэдээж. Таны хүссэн пост доор байна:\n\n"
    "Өнөөдөр манай кофе шоп нээгдлээ! Та бүхнийг урьж байна.\n\n"
    "Хэрэв өөр хувилбар хэрэгтэй бол хэлээрэй."
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

    def test_established_terms_not_flagged(self):
        self.assertEqual(m.check_noun_verb("Татварын хөнгөлөлт үзүүлнэ. Захиалга хийх боломжтой."), [])

    def test_established_collocations_from_human_text_not_flagged(self):
        text = (
            "Цагдаа шалгалт хийлээ. Эрдэмтэд нээлт хийсэн. Тэр сонголт хийнэ. "
            "Бид хэмжилт хийж, танилцуулга хийв. Компани хөрөнгө оруулалт хийх юм."
        )
        self.assertEqual(m.check_noun_verb(text), [])

    def test_lexicalised_noun_without_hiih_is_fine(self):
        self.assertEqual(m.check_noun_verb("Уулзалт амжилттай болов. Сургалтад хамрагдсан."), [])


class PassiveTest(unittest.TestCase):
    def test_stacked_passive_is_flagged(self):
        text = "Уулзалт зохион байгуулагдахаар төлөвлөгдөж байна."
        self.assertEqual(len(m.check_passive(text)), 1)

    def test_single_agentless_passives_are_left_to_judgement(self):
        self.assertEqual(m.check_passive("Хурал зохион байгуулагдсан."), [])
        self.assertEqual(m.check_passive("Асуудлууд хөндөгджээ. Концерт тоглогдоно."), [])

    def test_united_nations_is_not_a_passive(self):
        self.assertEqual(m.check_passive("Нэгдсэн Үндэстний Байгууллага санал нэгдсэн."), [])

    def test_native_formulas_are_not_flagged(self):
        text = "Энэ мэдээ хуулиар хамгаалагдсан. Журам тогтоолоор батлагдсан."
        self.assertEqual(m.check_passive(text), [])

    def test_perception_verbs_are_native(self):
        text = "Уул харагдав. Тэгж санагдлаа. Дуу сонсогдов. Ингэж бодогдсон."
        self.assertEqual(m.check_passive(text), [])


class NiTest(unittest.TestCase):
    def test_two_ni_in_one_clause_is_native(self):
        # Human text uses "нь" about 5x more than AI text (references/false-positives.md).
        self.assertEqual(m.check_ni_overuse("Энэ сургууль нь багш нь чадвартай. Би ирлээ."), [])

    def test_stacked_ni_in_one_clause(self):
        self.assertEqual(len(m.check_ni_overuse("Энэ хөтөлбөр нь сурагчдын мэдлэг нь дээшлэхэд нь тусалдаг.")), 1)

    def test_parallel_contrastive_ni_is_native(self):
        text = "Үг нь зөв, дүрэм нь алдаагүй мөртлөө өгүүлбэр нь монгол биш."
        self.assertEqual(m.check_ni_overuse(text), [])

    def test_ni_inside_quotes_is_ignored(self):
        text = 'Тэр "Үг нь монгол, өгүүлбэр нь орос" гэж хэлсэн нь зөв.'
        self.assertEqual(m.check_ni_overuse(text), [])

    def test_possessive_ni_after_case_ending_is_native(self):
        self.assertEqual(m.check_ni_overuse("Аав нь гарыг нь бариад инээлээ."), [])

    def test_fixed_expressions_with_ni_are_native(self):
        self.assertEqual(m.check_ni_overuse("Ер нь төр нь ч сайн."), [])
        self.assertEqual(m.check_ni_overuse("Жишээ нь хүүхэд нь өвдсөн."), [])

    def test_converb_starts_a_new_clause(self):
        self.assertEqual(m.check_ni_overuse("Цэцгийн дэлбээ нь хийсэж үндэс нь үлддэг."), [])

    def test_one_ni_per_sentence_is_native(self):
        text = "Хууль нь батлагдсан. Шүүх нь шийдсэн. Иргэд нь баярласан."
        self.assertEqual(m.check_ni_overuse(text), [])

    def test_ni_inside_word_is_ignored(self):
        self.assertEqual(m.check_ni_overuse("Миний нийтлэл нийгэмд хүрсэн."), [])


class GrammarTest(unittest.TestCase):
    def test_doubled_possessive(self):
        self.assertEqual(len(m.check_doubled_possessive("Таны бие лагшин тань сайн уу?")), 1)

    def test_plural_after_quantifier(self):
        hits = m.check_quantifier_plural("Олон хүмүүс ирсэн. Бүх оюутнууд суусан. Гурван ном авлаа.")
        self.assertEqual(len(hits), 2)

    def test_plural_forms_with_case_endings(self):
        text = "Олон судлаачдын үзэж байгаагаар. 23 ажилчид ирэв. Зарим оюутнуудын санал. 120 багш нар суув."
        self.assertEqual(len(m.check_quantifier_plural(text)), 4)

    def test_words_containing_plural_letters_are_not_plurals(self):
        self.assertEqual(m.check_quantifier_plural("Олон буудал байна. Хоёр хуудас бичлээ."), [])
        self.assertEqual(m.check_quantifier_plural("Олон шууд нэвтрүүлэг гарсан."), [])

    def test_agent_noun_in_dative_is_not_a_plural(self):
        # "үйлчлүүлэгчид" after "Эхний 100" reads as dative singular ("to the first 100 customers").
        self.assertEqual(m.check_quantifier_plural("Эхний 100 үйлчлүүлэгчид бэлэг өгнө."), [])

    def test_agent_noun_plural_after_numeral_is_flagged(self):
        text = "Чуулганд 23 улсын 140 гаруй төлөөлөгчид оролцсон."
        self.assertEqual(len(m.check_quantifier_plural(text)), 1)

    def test_group_plural_without_quantifier_is_native(self):
        self.assertEqual(m.check_quantifier_plural("Багш нар, эцэг эхчүүд ирэв."), [])

    def test_bolon_in_list(self):
        self.assertEqual(len(m.check_bolon_list("Дорж, Дондог, болон Бат ирэв.")), 1)


class RhythmTest(unittest.TestCase):
    def test_san_run(self):
        text = "Бид гарсан. Уул руу явсан. Хоол идсэн. Тэгээд харилаа."
        self.assertEqual(len(m.check_ending_runs(text)), 1)

    def test_identical_lexical_verb_run(self):
        text = "Дорж ном уншина. Бат ном уншина. Сараа ном уншина."
        self.assertEqual(len(m.check_ending_runs(text)), 1)

    def test_auxiliary_and_particle_runs_are_native(self):
        self.assertEqual(m.check_ending_runs("Бид гарч байна. Бид явж байна. Бид идэж байна."), [])
        self.assertEqual(m.check_ending_runs("Тийм юм. Ийм юм. Ингэдэг юм."), [])

    def test_varied_endings(self):
        self.assertEqual(m.check_ending_runs(NATURAL_TEXT), [])


class AiOutputTest(unittest.TestCase):
    def test_connector_pile(self):
        self.assertGreaterEqual(len(m.check_connector_pile(AI_ESSAY)), 3)

    def test_a_few_connectors_are_fine(self):
        self.assertEqual(m.check_connector_pile(FORMAL_ESSAY), [])

    def test_ordinals_and_essay_formulas_are_not_counted(self):
        # Not measured as AI-heavy: they number points or frame an essay.
        text = (
            "Нэгдүгээрт, ном мэдлэг өгдөг. Хоёрдугаарт, ном сэтгэлгээг тэлдэг. "
            "Гуравдугаарт, ном амраадаг. Эцэст нь, ном найз болдог. Дүгнэж хэлэхэд, ном чухал."
        )
        self.assertEqual(m.check_connector_pile(text), [])

    def test_assistant_offer_after_divider_is_framing(self):
        reply = (
            "Хэд хэдэн хувилбар бичлээ.\n\nӨнөөдөр Тэрэлж явлаа.\n\n---\n\n"
            "Хэрэв та тодорхой мөчүүдээ хэлбэл би постыг илүү хувийн болгож өгнө."
        )
        self.assertEqual(len(m.check_chat_framing(reply)), 2)

    def test_official_formula_iimd_is_muted_in_official_register(self):
        letter = "Хүү маань өвчтэй байна. Иймд чөлөө олгохыг хүсье. Мөн хичээлээ нөхнө. Мөн гэрээсээ давтана."
        self.assertEqual(m.analyze(letter, register="official")["hits"].get("connector_pile", []), [])

    def test_generic_voice(self):
        self.assertGreaterEqual(len(m.check_generic_voice(AI_ESSAY)), 3)

    def test_daг_yum_stance_is_not_generic_voice(self):
        self.assertEqual(m.check_generic_voice(FORMAL_ESSAY), [])

    def test_chat_framing(self):
        hits = m.check_chat_framing(CHAT_REPLY)
        self.assertEqual(len(hits), 2)

    def test_letter_greeting_is_not_framing(self):
        letter = "Эрхэм хүндэт захирал танаа,\n\nХүүгээ чөлөөлөхийг хүсье.\n\nХүндэтгэсэн, Д.Ганбат"
        self.assertEqual(m.check_chat_framing(letter), [])

    def test_placeholders(self):
        self.assertEqual(len(m.check_placeholders("Огноо: [өдөр, сар]. Гарын үсэг: ________")), 2)

    def test_unnamed_experts(self):
        hits = m.check_attribution("Энэ нь чухал алхам болно гэж мэргэжилтнүүд үзэж байна.")
        self.assertEqual(len(hits), 1)

    def test_bolomjtoi_filler_needs_repetition(self):
        one = "Та манай аппаар захиалга өгөх боломжтой."
        many = one + " Та ирж үзэх боломжтой. Та бүртгүүлэх боломжтой."
        self.assertEqual(m.check_bolomjtoi(one), [])
        self.assertEqual(len(m.check_bolomjtoi(many)), 3)


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

    def test_mash_is_not_counted(self):
        text = "Маш сайн. Маш гоё. Маш их баярлалаа."
        self.assertEqual(m.analyze(text)["types_found"], 0)


class TypographyTest(unittest.TestCase):
    def test_dashes(self):
        self.assertEqual(len(m.check_dashes("Хууль — эцэст нь — батлагдлаа. 2020–2024")), 2)

    def test_range_dash_is_ignored(self):
        self.assertEqual(m.check_dashes("2020–2024 онд"), [])

    def test_title_case_heading(self):
        self.assertEqual(len(m.check_title_case("## Бидний Шинэ Үйлчилгээ\nТекст")), 1)
        self.assertEqual(m.check_title_case("## Бидний шинэ үйлчилгээ"), [])

    def test_emoji_muted_in_posts(self):
        report = m.analyze("Өнөөдөр нээгдлээ! 🎉 Ирээрэй.", register="post")
        self.assertNotIn("emoji", report["flags"])


class ReportTest(unittest.TestCase):
    def test_formal_essay_is_light(self):
        self.assertEqual(m.analyze(FORMAL_ESSAY)["level"], "light")

    def test_translated_report_is_full(self):
        report = m.analyze(TRANSLATED_REPORT)
        self.assertGreaterEqual(report["types_found"], 3)
        self.assertEqual(report["level"], "full")

    def test_ai_essay_is_not_light(self):
        report = m.analyze(AI_ESSAY)
        self.assertNotEqual(report["level"], "light")
        self.assertIn("generic_voice", report["flags"])

    def test_natural_text_is_clean(self):
        report = m.analyze(NATURAL_TEXT)
        self.assertEqual(report["types_found"], 0)
        self.assertEqual(report["level"], "light")

    def test_chat_framing_does_not_raise_the_level(self):
        report = m.analyze(CHAT_REPLY)
        self.assertIn("chat_framing", report["flags"])
        self.assertEqual(report["level"], "light")

    def test_legal_register_is_never_rewritten(self):
        report = m.analyze(TRANSLATED_REPORT, register="legal")
        self.assertEqual(report["level"], "light")

    def test_level_thresholds(self):
        self.assertEqual(m.level_for(0, 9), "light")
        self.assertEqual(m.level_for(3, 9), "light")
        self.assertEqual(m.level_for(4, 9), "selective")
        self.assertEqual(m.level_for(4, 8), "selective")
        self.assertEqual(m.level_for(5, 9), "full")
        self.assertEqual(m.level_for(1, 2), "selective")

    def test_unknown_register_is_rejected(self):
        with self.assertRaises(ValueError):
            m.analyze("Текст.", register="poem")

    def test_empty_text(self):
        report = m.analyze("")
        self.assertEqual(report["types_found"], 0)
        self.assertEqual(report["level"], "light")


class CliTest(unittest.TestCase):
    def test_main_reads_file_and_register(self):
        import io
        import tempfile
        from contextlib import redirect_stdout

        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as fh:
            fh.write(TRANSLATED_REPORT)
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = m.main(["mn_markers.py", fh.name, "--register", "news"])
        Path(fh.name).unlink()
        self.assertEqual(code, 0)
        self.assertIn('"level": "full"', buf.getvalue())

    def test_main_reports_missing_file(self):
        self.assertEqual(m.main(["mn_markers.py", "no-such-file.txt"]), 1)

    def test_scripts_run_in_isolated_mode(self):
        # `python -I` drops the script's folder from sys.path; the sibling import must still work.
        import subprocess

        scripts = Path(__file__).resolve().parent.parent / "scripts"
        for script in ("mn_markers.py", "mn_compare.py"):
            with self.subTest(script):
                proc = subprocess.run(
                    [sys.executable, "-I", str(scripts / script), "--help"],
                    capture_output=True, text=True, encoding="utf-8",
                )
                self.assertEqual(proc.returncode, 0, proc.stderr)


if __name__ == "__main__":
    unittest.main()
