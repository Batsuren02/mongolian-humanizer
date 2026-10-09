# Mongolian Humanizer

Хиймэл оюуны бичсэн, эсвэл гадаад хэлнээс орчуулсан монгол текстийг уншихад нэг л эвгүй санагддаг. Үг нь зөв мөртлөө өгүүлбэр нь монгол биш. Ринчен гуайн хэлсэнчлэн "Үг нь монгол, өгүүлбэр нь орос байна." Энэ skill ийм текстийг монгол найруулга зүйн ёсоор засварлана. Claude Code, Codex, Cursor зэрэг SKILL.md уншдаг хэрэгсэлд ажиллана.

*English below.*

## Жишээ

Чатботын хариулт:

> **Өмнө:** Мэдээж. Иймэрхүү пост болно:
>
> Амралтын өдрөөр найзуудтайгаа Тэрэлж яваад, хотын завгүй хэмнэлээс түр ч гэсэн холдож сайхан амарлаа.
>
> **Дараа:** Амралтын өдрөөр найзуудтайгаа Тэрэлж яваад, хотын завгүй хэмнэлээс түр ч гэсэн холдож сайхан амарлаа.

Орчуулгын хэллэг:

> **Өмнө:** ...уулзалт зохион байгуулагдахаар төлөвлөгдөж байна.
>
> **Дараа:** ...уулзалт зохион байгуулахаар төлөвлөж байна.

Аль хэдийн сайн бичигдсэн текстэд гар хүрэхгүй, "засвар шаардлагагүй" гээд орхино.

## Зарчим

- Монгол найруулга зүйг баримтална, англи хэлний "богино, энгийн бич" зөвлөгөөг биш.
- Үйл үгийг сэргээнэ: "уулзалт хийлээ" биш, "уулзлаа".
- Чатботын хүсэлт гаргагчид хандсан мөр ("Мэдээж. Иймэрхүү пост болно:"), олон давтагдсан "Мөн", "Иймд"-ийг цэгцэлнэ.
- Хос үг, тогтсон хэллэг, "юм", "шүү", "билээ" зэрэг сул үгийг хамгаална.
- Текстийг бүдүүлэг, хүйтэн болгохгүй. Баримт, тоо, эх сурвалж, үзэл бодол нэмэхгүй.

## Суулгах

```bash
npx skills add Batsuren02/mongolian-humanizer --global
```

Claude Code plugin хэлбэрээр:

```
/plugin marketplace add Batsuren02/mongolian-humanizer
/plugin install mongolian-humanizer@mongolian-humanizer
```

## Хэрэглэх

`/mongolian-humanizer` гэж бичээд текстээ тавина, эсвэл "Энэ текстийг найруулж өгөөч" гэж хэлнэ. Skill юуг зассан, юуг хэвээр үлдээснээ тайлбарлаад засварласан хувилбараа өгнө.

## Хамтдаа сайжруулъя

Skill буруу засвар хийвэл, эсвэл орчуулга шиг санагдсан текст таарвал Issue нээж, аль хэсэг нь яагаад эвгүй байгааг бичээрэй. Дүрэм өөрчилсөн бол `python -m unittest discover -s tests` ажиллуулна уу.

---

## English

An agent skill that edits AI-generated or translated Mongolian (Khalkha, Cyrillic) by the rules of Mongolian stylistics, not English writing advice. "Shorter, plainer, cut the formulas" makes Mongolian blunt and rude.

- **Translated text:** turns noun-heavy calques back into verbs, removes redundant plurals, joins choppy runs of identical endings.
- **Chatbot output:** removes lines addressed to the requester, keeps template placeholders, eases piled-up "Мөн"/"Иймд", flags generic voice and unnamed experts. A 2026 measurement found current chatbots do not write translationese; these are their real tells.
- **Never:** makes a text ruder or lower in register, or adds facts, sources, examples, or opinions.

Rules and evidence: [SKILL.md](SKILL.md), [references/ai-output.md](references/ai-output.md), [references/sources.md](references/sources.md).

**Scripts** (optional, stdlib Python): `scripts/mn_markers.py` reports style hits and flags; `scripts/mn_compare.py ORIGINAL REWRITE` checks a rewrite for register drops, changed numbers, and blunt shortening.

**Evals:** 36 cases in `tests/eval/cases.jsonl` with a deterministic scorer (`tests/eval/check_outputs.py`), and the same cases in `evals/` for `claude plugin eval . --judge-model sonnet`.

### Changelog

- **0.3.0**: measured rebuild. Chatbot-output tells from a corpus comparison (references/ai-output.md); rules that fired on most human texts narrowed; mn_markers.py recalibrated; mn_compare.py, a 36-case eval suite, and CI checks added; SKILL.md cut to the essentials, details in references/.
- **0.2.1**: resolved rule conflicts, fixed examples that changed meaning, rewrote this README in Mongolian.
- **0.2.0**: rebuilt on Mongolian stylistics.
- **0.1.0**: first version, adapted from English humanizer rules.

Structure and the no-fabrication rule follow [blader/humanizer](https://github.com/blader/humanizer). License: MIT.
