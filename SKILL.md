---
name: mongolian-humanizer
description: |
  Edit Mongolian (Cyrillic) text so it reads like a skilled Mongolian writer
  wrote it, by the rules of Mongolian stylistics (найруулга зүй), not English
  writing advice. Use when asked to edit, proofread, polish, or humanize
  Mongolian essays, letters, posts, news, or reports (найруулах, засах,
  сайжруулах; эсээ, албан бичиг, пост, нийтлэл, тайлан), or when Mongolian
  text sounds translated, stiff, or AI-written (орчуулга шиг, робот шиг,
  ChatGPT шиг). Keeps the original's facts, register, and politeness.
license: MIT
metadata:
  version: "0.3.0"
  based_on: https://github.com/blader/humanizer
---

# Mongolian Humanizer

Make AI-written or translated Mongolian read as if a good Mongolian writer wrote it. Follow Mongolian stylistics, not English advice: "shorter, plainer, more direct" makes Mongolian rude.

> Энэ асуудлыг анхааралдаа авч, шийдвэрлэж өгөхийг хүсье. → ~~Үүнийг шийд.~~

## Principles

1. **The verb carries the sentence.** "Төслийн үр дүнгийн үнэлгээ хийгдсэн" → "Төслийн үр дүнг үнэлсэн".
2. **The sentence must be Mongolian, not just the words.** Rinchen: "Үг нь монгол, өгүүлбэр нь орос байна."
3. **Balance is a virtue.** Paired words (эрх үүрэг, ах дүү) and parallel clauses are not redundant.
4. **Join actions with converbs** (-ж, -аад, -вал). Do not chop text into short sentences.
5. **Endings and particles carry meaning.** Keep юм, билээ, шүү, "-даг юм".
6. **Respect.** Keep "Та", courtesy formulas, and softeners. Never make a text colder or ruder.

## Rules

1. **Already good? Change nothing,** and say so. Formal is not robotic.
2. **Never invent.** No new facts, names, numbers, sources, examples, or opinions. Never fill a placeholder ("[Нэр]").
3. **Meaning and tone stay.** Same meaning, same or higher politeness. Casual only if the user asks.
4. **The author wins.** Keep their dialect, style, and script (Latin stays Latin). Explain in the user's language.

## What to fix

**Translated text:**
- noun + хийх/хийгдэх instead of a verb
- double passive: "уулзалт зохион байгуулагдахаар төлөвлөгдөж байна" → "уулзалт зохион байгуулахаар төлөвлөж байна"
- plural after a number or quantifier: "олон номууд" → "олон ном"
- three sentences in a row with the same ending: join them

**Chatbot text:**
- lines to the requester ("Мэдээж. Иймэрхүү пост болно:", "Өөр хувилбар хэрэгтэй бол хэлээрэй"): remove
- many sentences opening with Мөн, Иймд, Юуны өмнө: keep about one in five
- unnamed experts, generic "-даг" truths: flag them, never invent the source or example
- placeholders: keep them and list them

## Leave alone

Read [references/false-positives.md](references/false-positives.md) before every edit. Keep formal formulas, paired words, long sentences, particles, news and official passives ("хуулиар хамгаалагдсан"), and school-essay structure. Do not restyle legal text. Never add what chatbots leave out (particles, questions, the author's opinion).

Test: would a Mongolian teacher mark it wrong? If not, leave it.

## Process

1. Name the register and the source: translated, chatbot, or human.
2. Read false-positives.md and the files for what you found (table below).
3. Edit at the right level. **Light** (most texts): up to a third of the sentences have problems; fix only those. **Selective:** up to half. **Full:** more than half; re-say each paragraph from its meaning. Removing chatbot lines does not raise the level.
4. Check: same meaning, no new facts, not colder, no labels on people. Fix anything that fails.

## Output

1. **Дүгнэлт:** one line: style, source, already fine or not.
2. **Засвар хийсэн зүйлс:** each change, quoting the original.
3. **Хэвээр үлдээсэн зүйлс:** native features kept on purpose.
4. **Засварласан хувилбар:** the final text.
5. **Анхаарах:** placeholders, claims to check, where the author's own view would help.

- **Nothing to change:** end Дүгнэлт with "засвар шаардлагагүй" and skip 2 and 4. Removing a chatbot wrapper counts as a change.
- **Several versions:** remove the wrapper, keep every version apart, edit each lightly.
- **"Final text only" or embedded use:** give only the text. **Files:** edit the prose in place.

## Files

| Read | When |
|---|---|
| [references/false-positives.md](references/false-positives.md) | always |
| [references/translationese.md](references/translationese.md) | translated text |
| [references/rhythm-and-grammar.md](references/rhythm-and-grammar.md) | endings, "нь", joining sentences |
| [references/ai-output.md](references/ai-output.md) | chatbot text |
| [references/voice.md](references/voice.md) | dry or generic text |
| [references/register-and-tone.md](references/register-and-tone.md) | formal, honorific, or unclear register |
| [references/typography.md](references/typography.md) | emoji, bold, dashes |
| [references/examples.md](references/examples.md) | worked examples |
| [references/mongolian-principles.md](references/mongolian-principles.md) | the principles in detail |
| [references/sources.md](references/sources.md) | sources |

**Scripts (optional, Python 3):** `python ${CLAUDE_SKILL_DIR}/scripts/mn_markers.py` counts problems and suggests a level; `python ${CLAUDE_SKILL_DIR}/scripts/mn_compare.py original.txt rewrite.txt` checks a rewrite for tone drops and changed numbers. When your reading finds more, your reading wins.
