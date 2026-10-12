# Mongolian Humanizer

Mongolian Humanizer бол хиймэл оюуны хэрэгсэлд зориулсан нэмэлт ур чадвар (skill) юм. Хиймэл оюуны бичсэн, эсвэл гадаад хэлнээс орчуулсан монгол текстийг уншихад нэг л эвгүй санагддаг. Үг нь зөв мөртлөө өгүүлбэр нь монгол биш. Ринчен гуайн хэлсэнчлэн "Үг нь монгол, өгүүлбэр нь орос байна." Энэ нэмэлт ур чадвар нь ийм текстийг монгол найруулга зүйн ёсоор засварлана. Claude Code, Codex, Cursor зэрэг SKILL.md уншдаг хэрэгсэлд ажиллана.

*English below.*

## Жишээ

### Орчуулга шиг мэдээ

> **Өмнө:** Өчигдөр сургууль дээр эцэг эхчүүдтэй уулзалт хийгдсэн. Уулзалтаар хүүхдүүдийн сурлагын асуудлууд хөндөгдсөн. Олон эцэг эхчүүд санал хэлсэн. Багш нар саналуудыг хүлээн авсан. Цаашид хамтын ажиллагааны сайжруулалт хийгдэх болно.
>
> **Дараа:** Өчигдөр сургууль дээр эцэг эхчүүдтэй уулзалт болсон. Уулзалтаар хүүхдүүдийн сурлагын асуудлыг хөндөж, олон эцэг эх санал хэлсэн бөгөөд багш нар саналыг нь хүлээн авсан. Цаашид хамтын ажиллагааг сайжруулах болно.

- "уулзалт хийгдсэн", "сайжруулалт хийгдэх" гэсэн нэр үг + хийгдэх хэллэгийн оронд жинхэнэ үйл үг: "уулзалт болсон", "сайжруулах".
- "олон эцэг эхчүүд", "саналуудыг": тоо, хэмжээ заасан үгийн ард олон тоо давхардаж байна.
- Дөрвөн өгүүлбэр дараалан "-сан"-аар төгсөж тасархай сонсогдож байна. Нөхцөл үйл үг, "бөгөөд"-оор холбов.
- Шинэ баримт, шинэ үйлдэгч нэмээгүй.

### Чатботын эсээ

Claude Sonnet-ийн бичсэн эсээнээс:

> **Өмнө:** Нөгөө талаас, хэт их ашиглах нь олон сөрөг үр дагавар авчирдаг. **Юуны өмнө,** унтах цаг багасч, сурлагын амжилт буурдаг. **Мөн** нийгмийн сүлжээнд бусадтай өөрийгөө харьцуулах нь өөртөө итгэх итгэлийг сулруулж, сэтгэл гутрал, түгшүүр үүсгэх эрсдэлтэй. **Үүнээс гадна** онлайн дээрх хэрүүл, дээрэлхэлт, тохиромжгүй агуулгад өртөх аюул ч бий.
>
> **Дараа:** Нөгөө талаас, хэт их ашиглах нь олон сөрөг үр дагавар авчирдаг. Унтах цаг багасч, сурлагын амжилт буурдаг. Нийгмийн сүлжээнд бусадтай өөрийгөө харьцуулах нь өөртөө итгэх итгэлийг сулруулж, сэтгэл гутрал, түгшүүр үүсгэх эрсдэлтэй бөгөөд онлайн дээрх хэрүүл, дээрэлхэлт, тохиромжгүй агуулгад өртөх аюул ч бий.

Дөрвөн өгүүлбэрийн гурав нь "Юуны өмнө", "Мөн", "Үүнээс гадна"-аар эхэлж байна. Монгол хүн ингэж бичдэггүй: бидний хэмжилтээр чатбот "Мөн"-ийг хүнээс 4.5 дахин, "Юуны өмнө"-г 9.5 дахин олон хэрэглэдэг. Утгатай үг нэг ч өөрчлөгдөөгүй.

Чатбот хүсэлт гаргагчид хандсан мөр ("Мэдээж. Иймэрхүү пост болно:", "Өөр хувилбар хэрэгтэй бол хэлээрэй") нэмбэл түүнийг хасна. Нэрийг нь дурдаагүй "мэргэжилтнүүд", "судлаачид"-ыг тэмдэглэж, эх сурвалжаа нэрлэхийг сануулна. Нэрийг нь өөрөө зохиож бичихгүй.

## Зарчим

Монгол найруулга зүйг баримтална.

**Засна:**

| Юуг | Жишээ |
|---|---|
| Нэр үг + хийх | "уулзалт хийлээ" → "уулзлаа" |
| Давхар идэвхгүй хэв | "зохион байгуулагдахаар төлөвлөгдөж байна" → "зохион байгуулахаар төлөвлөж байна" |
| Тооны ард олон тоо | "олон номууд" → "олон ном" |
| Ижил төгсгөлтэй тасархай өгүүлбэрүүд | "Эцэг эхчүүд санал хэлсэн. Багш нар хүлээн авсан." → "Эцэг эхчүүд санал хэлсэн бөгөөд багш нар хүлээн авсан." |
| Чатботын хүсэлт гаргагчид хандсан мөр | "Мэдээж. Иймэрхүү пост болно:" → хасна |
| Өгүүлбэр бүрийн эхэнд "Мөн", "Иймд" | Ихэнхийг нь хасна |

**Хөндөхгүй:**

- Хос үг, тогтсон хэллэг: "эрх үүрэг", "уул ус"
- "юм", "шүү", "билээ" зэрэг сул үг
- "Та", "хүсье" зэрэг хүндэтгэлийн хэллэг. Текстийг бүдүүлэг, хүйтэн болгохгүй.
- Аль хэдийн сайн бичигдсэн текст. "Засвар шаардлагагүй" гээд орхино.

**Нэмэхгүй:** баримт, тоо, нэр, эх сурвалж, үзэл бодол. "[Нэр]" гэх мэт хоосон зайг бөглөхгүй.

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

Хариу таван хэсэгтэй:

1. Дүгнэлт
2. Засвар хийсэн зүйлс
3. Хэвээр үлдээсэн зүйлс
4. Засварласан хувилбар
5. Анхаарах

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
