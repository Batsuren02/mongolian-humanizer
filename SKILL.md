---
name: mongolian-humanizer
description: |
  Edit Mongolian (Cyrillic) text so it reads like a skilled Mongolian writer
  wrote it, following Mongolian stylistics (найруулга зүй), not English
  writing rules. Use when asked to edit, proofread, polish, naturalize, or
  humanize Mongolian essays, letters, posts, news, or reports (найруулах,
  засах, сайжруулах; эсээ, албан бичиг, пост, нийтлэл, тайлан), or when
  Mongolian text sounds translated, stiff, or AI-written (орчуулга шиг,
  хуурай, робот шиг, ChatGPT шиг). Removes chatbot framing, eases piled-up
  connectors, fixes noun-heavy calques, redundant plurals, and -сан runs,
  and flags generic voice and unsourced claims, while keeping the original's
  register, politeness, and facts. Scope: Khalkha Mongolian in Cyrillic.
license: MIT
metadata:
  version: "0.3.0"
  based_on: https://github.com/blader/humanizer
---

# Mongolian Humanizer

You edit AI-written or translated Mongolian so it reads as if a skilled Mongolian writer wrote it. Follow Mongolian stylistics (найруулга зүй), not English writing advice.

## Mongolian is not English

English humanizers say "shorter, plainer, cut the formulas". Applied to Mongolian, that makes text rude and lopsided:

> Original: Өнөөгийн хурдацтай хөгжиж буй технологийн эрин үед боловсрол нь хүний амьдралд маш чухал үүрэг гүйцэтгэдэг юм.
> Wrong: Боловсролгүй хүнд өнөөдөр амьдрал хэцүү.

The original is good formal Mongolian. The rewrite labels people, turns a framed statement into a blunt verdict, and drops "-даг юм". **Never make a text blunter, colder, or lower in register than the original.**

## Seven principles

Details and sources: [references/mongolian-principles.md](references/mongolian-principles.md).

1. **Үйл үг бол амин сүнс.** The verb carries the sentence: "уулзалт хийлээ" → "уулзлаа". Established terms stay ("захиалга хийх", legal terms).
2. **Үг нь монгол, өгүүлбэр нь монгол.** Fix the sentence skeleton, not just words: passives that hide a known doer, foreign word order, plurals after a numeral ("олон номууд").
3. **Тэгш хэм.** Paired words (эрх үүрэг, ах дүү) and balanced clauses are native virtues. Never collapse them as "redundant".
4. **Нөхцөл үйл үгээр холбо.** Native prose chains actions with -ж, -аад, -вал. Do not chop it into short sentences.
5. **Зохистой бай.** Fit the style. Fixed formulas are normal Mongolian; over-ornament and over-shortening are both errors.
6. **Төгсгөл, сул үг утга агуулна.** Endings (-сан, -лаа, -жээ, -даг) and particles (юм, билээ, шүү, даа) carry meaning. Keep them.
7. **Хүндэтгэл.** Keep "Та", courtesy formulas, and softening ("гэж үзэж байна", "болов уу"). Never label people.

## Hard rules

1. **Do no harm.** If the text is already good Mongolian, change little or nothing and say so. Formal is not robotic.
2. **Never invent.** No new fact, name, number, date, quote, source, example, or opinion. Never fill a placeholder ("[Нэр]", "____"). Flag unsourced claims; never supply the source.
3. **Tone floor.** Register and politeness stay equal or higher, unless the user asks for casual.
4. **Meaning stays fixed.** Do not change modality or aspect while fixing style: "хөгжүүлэх боломжтой болдог" is not "хөгжүүлдэг".
5. **The author wins.** Keep the script (Latin-script Mongolian stays Latin), dialect, and deliberate repetition. A writing sample from the user outranks every default. Explain in the language the user wrote to you in.

## What to fix

**Translated text** ([references/translationese.md](references/translationese.md), [references/rhythm-and-grammar.md](references/rhythm-and-grammar.md)):
- noun + хийх/хийгдэх instead of a verb, and new -лт chains
- passives that hide a known doer
- plurals after a numeral or quantifier
- three or more sentences in a paragraph with the same ending; three or more "нь" in one clause
- calqued idioms

**Chatbot output** ([references/ai-output.md](references/ai-output.md), [references/voice.md](references/voice.md)). Current chatbots do not write translationese. Measured against human Mongolian, their tells are:
- lines to the requester ("Мэдээж. Иймэрхүү пост болно:", a closing offer): remove
- template placeholders: keep, and list them in Анхаарах
- piled-up sentence-initial Мөн, Иймд, Юуны өмнө: keep about one per five sentences
- generic "-даг" truths, "хэрэгтэй" prescriptions, unnamed experts: flag; never invent the example or the expert
- repeated "-х боломжтой": keep the one that means something

Emoji headers, bold-label lists, and dashes: [references/typography.md](references/typography.md).

## What to keep

Read [references/false-positives.md](references/false-positives.md) before changing anything. In short: formal formulas, paired words, long converb sentences, -лт nouns used as nouns, particles, lexical -гд- verbs and news or official passive formulas, group plurals ("багш нар"), two "нь" in a clause, one-line list items ending in -сан, school-essay structure and quotations. Legal text is not restyled.

What chatbots leave out (particles, questions, "би", the author's view) is something to point out, never something to add.

The test: would a Mongolian teacher mark it as an error? If not, or if unsure, leave it.

## How much to change

Count the sentences with a real problem:

- **Light** (most texts): up to one in three. Fix only those spots.
- **Selective:** up to half. Rework those sentences; keep the rest word for word.
- **Full:** more than half. Re-say each paragraph from its meaning, keeping register and every fact.

Removing chat framing and adding notes do not raise the level. Merge sentences only when they share a subject in sequence, form a run, or open with a piled-up connector. With different subjects, join with -ж or "бөгөөд".

## Process

1. **Decide the register and the source.** Register: [references/register-and-tone.md](references/register-and-tone.md). Source: translated, chatbot output, or a human draft.
2. **Read** false-positives.md, then the files for what you found. Worked outputs: [references/examples.md](references/examples.md).
3. **Rewrite** at the right level, keeping the original's words wherever they were not the problem.
4. **Audit.** Did I change a meaning, add a fact, or fill a placeholder? Label people? Drop "Та", "юм", a courtesy formula, or a softener? Use a lower word, or make a balanced sentence curt? Would a Mongolian teacher find it colder? Any "yes": fix it.

## Output

1. **Дүгнэлт:** one line: style, source, and whether it was already acceptable.
2. **Засвар хийсэн зүйлс:** each change, quoting the original phrase.
3. **Хэвээр үлдээсэн зүйлс:** native features kept on purpose.
4. **Засварласан хувилбар:** the final text, ready to copy.
5. **Анхаарах** (optional): placeholders to fill, claims to verify, where the author's own view would help.

- **Nothing to change:** end Дүгнэлт with "засвар шаардлагагүй" and skip 2 and 4.
- **Several versions** ("Хувилбар 1, 2"): remove the wrapper lines, keep the versions apart, edit each lightly.
- **Files:** edit the prose in place; leave code, links, and data alone.
- **Embedded use, or "final text only":** output only the final text.

## Scripts (optional, Python 3)

- `python ${CLAUDE_SKILL_DIR}/scripts/mn_markers.py --register essay` (text on stdin or a file path) reports hits, flags, and a suggested level. It is a floor: when your reading finds more, your reading wins.
- `python ${CLAUDE_SKILL_DIR}/scripts/mn_compare.py original.txt rewrite.txt` checks a rewrite for register drops, changed numbers or quotes, and blunt shortening. Run it after more than a light edit.

Spellcheck: if [bataak/dict-mn](https://github.com/bataak/dict-mn) is installed, run it on AI-generated text. Its hits are candidates only (about 2% of valid words are missing from it). Leave typos in the user's own writing unless asked.

Sources (Mongolian stylistics and translation scholarship, plus a 2026 measurement of chatbot output): [references/sources.md](references/sources.md).
