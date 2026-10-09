# Mongolian Humanizer

Хиймэл оюуны бичсэн болон орчуулсан монгол текстийг монгол найруулга зүйн зарчмаар засварладаг AI agent skill. Claude Code, Codex, Cursor болон SKILL.md уншдаг бусад хэрэгсэлд ажиллана.

*English below.*

## Яагаад хэрэгтэй вэ

ChatGPT, Claude зэрэг загварын бичсэн монгол текст дүрмийн хувьд зөв ч уншихад орчуулга шиг санагдах нь бий. Ринчен гуай нэгэн орчуулгыг "Үг нь монгол, өгүүлбэр нь орос байна" гэж шүүмжилсэн байдаг. AI-ийн монгол текст ч мөн адил: үг нь монгол, өгүүлбэрийн бүтэц нь англи.

> Өчигдөр сургууль дээр эцэг эхчүүдтэй уулзалт хийгдсэн. Уулзалтаар хүүхдүүдийн сурлагын асуудлууд хөндөгдсөн. Олон эцэг эхчүүд санал хэлсэн. Багш нар саналуудыг хүлээн авсан.

Засварласны дараа:

> Өчигдөр сургууль дээр эцэг эхчүүдтэй уулзаж, хүүхдүүдийн сурлагын асуудлыг ярилцлаа. Олон эцэг эх санал хэлж, багш нар саналыг нь хүлээн авсан.

Англи хэлний humanizer-үүд "богино, энгийн, шулуун бич" гэж заадаг. Монгол текстэд ийм зөвлөгөө хэрэглэвэл бичвэр бүдүүлэг, сондгой болдог. Тиймээс энэ skill англи хэлний дүрмийг биш, монгол найруулга зүйн зарчмыг баримтална.

## Долоон зарчим

1. **Үйл үг бол амин сүнс.** "Уулзалт хийлээ" биш "уулзлаа".
2. **Үг нь ч, өгүүлбэр нь ч монгол.** Үйлдэгдэхүүн хэвийг (-гд-) үйлдэгчгүй хэрэглэсэн, илүүдэл олон тооны дагавартай өгүүлбэрийг засна.
3. **Тэгш хэм, хорших ёс.** Хос үг, тэнцвэртэй өгүүлбэрийг хэвээр үлдээнэ.
4. **Нөхцөл үйл үгээр холбох.** "-сан. -сан. -сан." гэж дуусах богино өгүүлбэрүүдийг -ж, -аад нөхцөлөөр холбоно.
5. **Зохистой байх.** Найруулгын төрөлд нийцүүлнэ: хэт чамирхахгүй, хэт товчлохгүй.
6. **Төгсгөл, сул үгийг хадгалах.** "-даг юм", "билээ", "шүү" зэрэг нь утга агуулдаг.
7. **Хүндэтгэл.** Засварласан текст эхээсээ бүдүүлэг, хүйтэн болох ёсгүй.

## Юуг засахгүй вэ

"Чухал үүрэг гүйцэтгэдэг", "Дүгнэж хэлэхэд", "Мөн түүнчлэн" зэрэг тогтсон хэллэг, хос үг, урт нийлмэл өгүүлбэр, сэдэв заасан "нь", "юм" зэрэг нь монгол хэлний жам ёсны хэрэглээ тул засахгүй. Текст аль хэдийн зөв бол skill "засах шаардлагагүй" гэж хэлнэ.

Эх бичвэрт байхгүй баримт, тоо, эх сурвалж, хувийн үзэл бодлыг хэзээ ч нэмэхгүй.

## Суулгах

**Skills CLI (бүх agent-д):**

```bash
npx skills add Batsuren02/mongolian-humanizer --global
```

**Claude Code plugin:**

```
/plugin marketplace add Batsuren02/mongolian-humanizer
/plugin install mongolian-humanizer@mongolian-humanizer
```

**Гараар:**

```bash
git clone https://github.com/Batsuren02/mongolian-humanizer.git ~/.claude/skills/mongolian-humanizer
```

## Хэрэглэх

Claude Code дээр `/mongolian-humanizer` гэж бичээд текстээ хуулж тавина. Эсвэл "Энэ текстийг монгол хүний бичсэн мэт болгоод өг" гэж хэлж болно. Өөрийн бичсэн текстийн жишээ өгвөл skill таны хэв маягийг дагана.

Skill юуг зассан, юуг санаатайгаар хэвээр үлдээснээ тайлбарлаж, дараа нь засварласан хувилбарыг өгнө.

### Шалгах скрипт

Python байгаа бол орчуулгын шинжийг (нэр үг + хийх, үйлдэгчгүй -гд-, илүүдэл олон тоо, ижил төгсгөлтэй өгүүлбэрийн цуваа гэх мэт) тоолж болно:

```bash
python scripts/mn_markers.py essay.txt
```

Энэ бол зөвхөн туслах хэрэгсэл, эцсийн шийдвэр биш.

## Хувь нэмэр оруулах

Энэ skill-ийн хамгийн сул тал нь AI монгол хэлээр хэрхэн бичдэг тухай судалгаа бараг байхгүйд оршино. Тиймээс монгол хэлтэй хүмүүсийн бодит жишээ хамгийн үнэ цэнэтэй.

1. AI-ийн бичсэн, орчуулга шиг эсвэл хуурай санагдсан текст олж харвал Issue нээж, текстээ болон аль хэсэг нь яагаад эвгүй санагдсаныг бичээрэй.
2. Skill буруу засвар хийсэн бол (жишээ нь бүдүүлэг болгосон, хос үг хассан) мөн Issue нээгээрэй.
3. Шинэ хэв маяг нэмэх бол `references/` доторх тохирох файлд "Before / After" жишээ, эх сурвалжийн хамт Pull Request илгээгээрэй.
4. Скрипт өөрчилсөн бол `python -m unittest discover -s tests` ажиллуулна уу.

Эх сурвалжийн жагсаалт: [references/sources.md](references/sources.md).

---

## English

An agent skill that edits AI-generated or translated Mongolian (Cyrillic) text following Mongolian stylistics (найруулга зүй), not English writing rules. Works in Claude Code, Codex, Cursor, and any harness that reads `SKILL.md`.

**Why not just port an English humanizer?** English advice ("shorter, plainer, cut the formulas") makes Mongolian blunt and lopsided. Version 0.1 of this skill made exactly that mistake. Version 0.2 is rebuilt on principles from Mongolian stylistics and translation scholarship:

1. The verb carries the sentence: turn noun + хийх back into the verb.
2. The sentence skeleton must be Mongolian, not just the words (Rinchen: "Үг нь монгол, өгүүлбэр нь орос").
3. Balance and paired words (хос үг) are virtues, not redundancy.
4. Chain clauses with converbs; avoid runs of identical -сан endings.
5. Fit the functional style; over-shortening is as much an error as over-ornament.
6. Finite endings and particles carry evidential and stance meaning; keep them.
7. Respect: a rewrite must never be blunter or lower in register than the original.

It fixes noun-heavy calques, agentless passives, redundant plurals, choppy ending runs, calqued idioms, chatbot leftovers, and lifeless generic voice. It leaves formal formulas, paired words, long converb sentences, and particles alone, and never adds facts, sources, or opinions.

Install with `npx skills add Batsuren02/mongolian-humanizer --global`, or as a Claude Code plugin (see above). Invoke with `/mongolian-humanizer`.

### Credits

- Mongolian principles: Ц.Сүхбаатар, Д.Отгонсүрэн, Пүрэв-Очир (via nairuulga.mn, National Council for Language Policy); Энхбаяр, Чулуунбаатар, Эрдэнэмаам, Шагдарсүрэн, Бүрнээ, Галсан (NUM translation studies); Brosig on evidentiality and particles. Full list in [references/sources.md](references/sources.md).
- Structure and the no-fabrication rule: [blader/humanizer](https://github.com/blader/humanizer).
- Ideas from other-language humanizers: humanizer-ru, [daleseo/korean-skills](https://github.com/daleseo/korean-skills), and the Chinese translationese essay on yage.ai.

### Changelog

- **0.2.0**: rebuilt on Mongolian stylistics. Dropped English-derived "AI phrase" lists that flagged normal formal Mongolian. Added the seven principles, register and tone guard, evidence tags, verified translationese patterns, and a sources list. The marker script no longer flags formulas, topic "нь", or connectives.
- **0.1.0**: first version, adapted from English humanizer rules.

## License

MIT
