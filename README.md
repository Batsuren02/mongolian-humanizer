# Mongolian Humanizer

Хиймэл оюуны бичсэн, эсвэл гадаад хэлнээс орчуулсан монгол текстийг уншихад нэг л эвгүй санагддаг. Үг нь зөв, дүрэм нь алдаагүй мөртлөө өгүүлбэр нь монгол биш. Ринчен гуай нэгэн оюутны орчуулгыг "Үг нь монгол, өгүүлбэр нь орос байна" гэж шүүмжилсэн нь яг үүнийг хэлсэн хэрэг. Энэ skill ийм текстийг монгол найруулга зүйн ёсоор засварлахад тусална. Claude Code, Codex, Cursor зэрэг SKILL.md уншдаг хэрэгсэл бүхэнд ажиллана.

*English below.*

## Жишээ

Хиймэл оюуны бичсэн тайлан:

> Өчигдөр сургууль дээр эцэг эхчүүдтэй уулзалт хийгдсэн. Уулзалтаар хүүхдүүдийн сурлагын асуудлууд хөндөгдсөн. Олон эцэг эхчүүд санал хэлсэн. Багш нар саналуудыг хүлээн авсан.

Засварласны дараа:

> Өчигдөр сургууль дээр эцэг эхчүүдтэй уулзалт болсон. Уулзалтаар хүүхдүүдийн сурлагын асуудлыг хөндөж, олон эцэг эх санал хэлсэн бөгөөд багш нар саналыг нь хүлээн авсан.

Харин аль хэдийн сайн бичигдсэн текстэд skill гар хүрэхгүй. "Өнөөгийн хурдацтай хөгжиж буй технологийн эрин үед боловсрол нь хүний амьдралд маш чухал үүрэг гүйцэтгэдэг юм" гэх мэт өгүүлбэрийг засах шаардлагагүй гээд орхино.

## Ямар зарчим баримталдаг вэ

Англи хэлний humanizer-үүд "богино, энгийн, шулуун бич" гэж заадаг. Монгол текстэд үүнийг хэрэглэвэл бичвэр бүдүүлэг, сондгой болчихдог. Тиймээс энэ skill англи хэлний биш, монгол найруулга зүйн зарчмыг баримтална.

Монгол хэлэнд үйл үг өгүүлбэрийн амин сүнс болдог тул "уулзалт хийлээ" гэхийн оронд "уулзлаа" гэж бичнэ. -гд- дагавраар хэн хийснийг нуусан өгүүлбэрт үйлдэгч мэдэгдэж байвал түүнийг эргүүлж өгнө. "Олон номууд" гэх мэт илүүдэл олон тооны дагаврыг хасна. Ижил төгсгөлтэй богино өгүүлбэрүүд цуварвал нөхцөл үйл үгээр холбож, нэг урсгалтай болгоно.

Монгол хэлний сайхан талыг ч мөн хамгаална. Хос үг, тэнцвэртэй өгүүлбэр, урт нийлмэл өгүүлбэр, "чухал үүрэг гүйцэтгэдэг", "Дүгнэж хэлэхэд" мэтийн тогтсон хэллэг, "юм", "шүү", "билээ" гэх сул үгс бүгд утга агуулж, бичвэрт өнгө аяс өгдөг. Засварласан текст эхээсээ хэзээ ч бүдүүлэг, хүйтэн болох ёсгүй. Эх бичвэрт байхгүй баримт, тоо, эх сурвалж, хувийн үзэл бодлыг ч нэмэхгүй.

## Суулгах

Бүх agent-д нэг дор суулгах бол:

```bash
npx skills add Batsuren02/mongolian-humanizer --global
```

Claude Code-ын plugin хэлбэрээр:

```
/plugin marketplace add Batsuren02/mongolian-humanizer
/plugin install mongolian-humanizer@mongolian-humanizer
```

Эсвэл гараар:

```bash
git clone https://github.com/Batsuren02/mongolian-humanizer.git ~/.claude/skills/mongolian-humanizer
```

## Хэрэглэх

Claude Code дээр `/mongolian-humanizer` гэж бичээд текстээ хуулж тавихад хангалттай. "Энэ текстийг монгол хүний бичсэн мэт болгоод өгөөч" гэж энгийнээр хэлсэн ч болно. Skill юуг зассан, юуг санаатайгаар хэвээр үлдээснээ тайлбарлаад, дараа нь засварласан хувилбараа өгнө. Өөрийн бичсэн текстээс жишээ өгвөл таны хэв маягийг дагана.

Python суулгасан бол `scripts/mn_markers.py` скриптээр орчуулгын шинжийг тоолж болно. Энэ нь зөвхөн туслах хэрэгсэл болохоос эцсийн шийдвэр биш.

## Хамтдаа сайжруулъя

Хиймэл оюун монголоор хэрхэн бичдэг талаар судалгаа одоогоор бараг байхгүй. Тиймээс энэ skill-ийг сайжруулахад монгол хүн бүрийн нүд, чих хамгийн үнэтэй. Орчуулга шиг, хуурай санагдсан текст таарвал, эсвэл skill буруу засвар хийвэл Issue нээж, аль хэсэг нь яагаад эвгүй санагдсаныг бичээд үлдээгээрэй. Шинэ хэв маяг нэмэх бол `references/` доторх файлд өмнөх ба дараах жишээ, эх сурвалжийн хамт Pull Request илгээнэ үү. Скрипт өөрчилсөн бол `python -m unittest discover -s tests` ажиллуулж шалгаарай.

Эх сурвалжийн жагсаалт: [references/sources.md](references/sources.md).

---

## English

An agent skill for editing AI-generated or translated Mongolian (Khalkha, Cyrillic). It follows Mongolian stylistics (найруулга зүй) rather than English writing advice, because "shorter, plainer, cut the formulas" makes Mongolian blunt and lopsided.

It turns noun-heavy calques back into verbs, gives agentless passives their doer when the doer is known, removes redundant plurals, and joins choppy runs of identical endings with converbs. It leaves alone what is native: paired words, balanced and long converb sentences, fixed formal phrases, and particles like юм and шүү. It never makes a text ruder or lower in register, and never adds facts, sources, or opinions. Lifeless, generic voice and unsourced claims are flagged for the author, not papered over.

Install with `npx skills add Batsuren02/mongolian-humanizer --global` or as a Claude Code plugin (see above), then run `/mongolian-humanizer`.

The principles come from Mongolian stylistics and translation scholarship (Сүхбаатар, Отгонсүрэн, Пүрэв-Очир, Энхбаяр, Чулуунбаатар, Эрдэнэмаам, Галсан and others); see [references/sources.md](references/sources.md). Structure and the no-fabrication rule follow [blader/humanizer](https://github.com/blader/humanizer).

### Changelog

- **0.2.1**: second review. Resolved rule conflicts (legal text, paired-word plurals, merging, chatbot phrases, emoji, quotes), fixed examples that changed meaning or invented an actor, and rewrote this README in natural Mongolian.
- **0.2.0**: rebuilt on Mongolian stylistics; dropped English "AI phrase" lists that flagged normal formal Mongolian.
- **0.1.0**: first version, adapted from English humanizer rules.

## License

MIT
