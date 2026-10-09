# Mongolian Humanizer

Хиймэл оюуны бичсэн монгол текстийг хүний бичсэн мэт болгох AI agent skill. Claude Code, Codex, Cursor болон SKILL.md уншдаг бусад хэрэгсэлд ажиллана.

*English below.*

## Яагаад хэрэгтэй вэ

ChatGPT, Claude зэрэг загварын бичсэн монгол текст дүрмийн хувьд зөв ч уншихад орчуулга шиг санагддаг. Учир нь загварууд англи өгүүлбэрийн бүтцийг монгол үгээр дүүргэдэг:

> Өнөөгийн хурдацтай хөгжиж буй технологийн эрин үед боловсрол нь хүний амьдралд маш чухал үүрэг гүйцэтгэдэг юм.

Энэ skill ийм текстийг монгол хүний ярьдаг, бичдэг байдлаар дахин бичнэ:

> Боловсролгүй хүнд өнөөдөр амьдрал хэцүү.

## Юуг засдаг вэ

| Бүлэг | Жишээ |
|---|---|
| Орчуулгын хэллэг | "Энэ нь ... юм", "нэг чухал асуудал", "-ын тусламжтайгаар", "-х боломжтой", "өөрсдийн мэдлэгээ" |
| Канцелярит | "зохион байгуулах ажлыг хэрэгжүүлсэн", "-ын хүрээнд", "анхаарч ажиллана", урт -лтын гинж |
| AI-ийн хэвшмэл хэллэг | "чухал үүрэг гүйцэтгэдэг", "Мөн түүнчлэн", "Дүгнэж хэлэхэд", "зүгээр нэг ... биш, харин" |
| Нөхцөл, дагаврын хэтрэлт | Давтагдсан "нь", "болон", "маш", "олон хүмүүс", ижил төгсгөлтэй өгүүлбэрүүд |
| Хэлбэр | Урт зураас (—), эможи, тод үсэгтэй жагсаалт, Том Үсэгтэй Гарчиг |

Бичвэрийн төрлийг (эсээ, албан бичиг, пост, эрдэм шинжилгээ) харгалзана. Албан бичгийг энгийн яриа болгохгүй, зөвхөн илүүдлийг нь хасна. Эх бичвэрт байхгүй баримт, тоо, эх сурвалж хэзээ ч нэмэхгүй.

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

Claude Code дээр `/mongolian-humanizer` гэж бичээд текстээ хуулж тавина. Эсвэл энгийнээр "Энэ текстийг хүний бичсэн мэт болгоод өг" гэж хэлж болно.

Өөрийн бичсэн текстийн жишээ өгвөл skill таны хэв маягийг дагана.

### Шалгах скрипт

Python байгаа бол текстэд хэдэн төрлийн AI тэмдэг байгааг тоолж болно:

```bash
python scripts/mn_markers.py essay.txt
```

0–2 төрөл бол бага зэрэг, 3–5 бол сонгож, 6 ба түүнээс дээш бол бүрэн дахин бичнэ.

## Хувь нэмэр оруулах

Монгол хэлэнд зориулсан humanizer skill одоогоор ховор тул бодит жишээ их хэрэгтэй байна. Хэрэв AI-ийн бичсэн "робот шиг" монгол текст олж харвал:

1. Issue нээгээд текстээ, яагаад байгалийн бус санагдсаныг бичээрэй.
2. Эсвэл `references/` доторх тохирох файлд шинэ хэв маяг нэмж Pull Request илгээгээрэй. Хэв маяг бүрт "Before / After" жишээ байх ёстой.
3. Скрипт өөрчилсөн бол `python -m unittest discover -s tests` ажиллуулна уу.

---

## English

An agent skill that rewrites AI-generated Mongolian (Cyrillic) text so it reads like a native speaker wrote it. Works in Claude Code, Codex, Cursor, and any harness that reads `SKILL.md`.

AI Mongolian is usually grammatical but sounds translated: English sentence skeletons filled with Mongolian words, plus Soviet-style bureaucratic phrasing (канцелярит) learned from government documents. This skill detects those patterns in six groups (English calques, bureaucratic register, AI stock phrases, overused particles and suffixes, rhythm, typography) and rewrites at a level matched to how many it finds. It respects register (essay, official letter, social post, academic) and never adds facts that aren't in the source.

Install with `npx skills add Batsuren02/mongolian-humanizer --global`, or as a Claude Code plugin (see above). Invoke with `/mongolian-humanizer`.

### Credits

- Structure and the no-fabrication rule: [blader/humanizer](https://github.com/blader/humanizer), based on Wikipedia's "Signs of AI writing".
- Signal-count levels and genre rules: the Russian community skill humanizer-ru.
- "Read, look away, re-say" method: the Chinese translationese essay on yage.ai.
- Korean translationese categories: [daleseo/korean-skills](https://github.com/daleseo/korean-skills).
- Mongolian style rules from Mongolian translation and найруулга зүй teaching.

## License

MIT
