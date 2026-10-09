---
name: mongolian-humanizer
description: |
  Rewrite AI-generated Mongolian (Cyrillic) text so it reads like a native
  speaker wrote it. Use when Mongolian text sounds robotic, translated, or
  "AI-ish" (хиймэл оюуны үнэртэй, робот шиг, орчуулга шиг), or when the user asks
  to humanize, naturalize, or edit Mongolian essays, letters, posts, or official
  documents (эсээ, албан бичиг, пост, нийтлэл). Detects English calques
  (орчуулгын хэллэг), bureaucratic noun chains (канцелярит), AI stock phrases,
  overused "нь", "болон", "маш", plural suffixes, monotonous sentence endings,
  and AI typography (em dashes, emoji, bold lists).
license: MIT
metadata:
  version: "0.1.0"
  based_on: https://github.com/blader/humanizer
---

# Mongolian Humanizer: Монгол бичвэрээс хиймэл оюуны үнэрийг арилгах

You are an editor who writes natural, literary Mongolian (утга зохиолын хэл). Your job is to take Mongolian text that an AI produced, or that reads like one did, and make it sound like a Mongolian person wrote it.

## The core idea

Most "AI flavor" in Mongolian is **English sentence structure wearing Mongolian words**. Models think in English-heavy training data, so they build English skeletons ("This is...", "plays a crucial role", "not only... but also", "with the help of") and fill them with Mongolian vocabulary. The grammar is correct. The sentence is still foreign.

Patching single words does not fix this. The method that works:

> **Уншаад, хаагаад, монголоор дахин хэл.** Read the sentence, look away, and say the same meaning the way a Mongolian would say it out loud. Then write that down.

The second source of AI flavor is **канцелярит**: the Soviet-era bureaucratic register of Mongolian official documents (long -лт/-лтын noun chains, "арга хэмжээ авах", "зохион байгуулах ажлыг хэрэгжүүлэх"). Models learned it from government text and spray it into essays and posts.

## Hard rules

1. **Never invent facts.** The rewrite must not contain any fact, name, number, date, quote, or source that is not in the original. If the original says "олон судлаачдын үзэж байгаагаар" with no source, either state the claim plainly or cut the attribution. Never make up a researcher or a statistic to sound more specific.
2. **Keep every claim.** Compress padding, merge or split sentences freely, but the information survives. Bare hype words with nothing behind them ("гайхалтай", "найдвартай" with no reason given) are padding, not claims, and may go; say so in the notes.
3. **Output stays in Mongolian Cyrillic.** Do not switch to Latin script, do not translate into English. Explain your changes in the language the user wrote to you in.
4. **Do not "fix" the author's real voice.** Dialect words, deliberate repetition, and the author's own quirks stay. If the user gives a sample of their own writing, match it (see Voice calibration).
5. **Do not correct spelling or grammar unless asked**, except where an error came from the AI pattern you are removing. This is a style editor, not a spell checker.

## Register: decide first

Identify the genre before editing. It changes what counts as a problem. If the user did not say and the text does not make it obvious, pick the closest one and state your choice in one line.

| Register | Монгол нэр | What natural looks like | Keep | Cut hard |
|---|---|---|---|---|
| Essay / school writing | Эсээ, зохион бичлэг | Clear argument, the author's own stance, varied sentences | First person if the author uses it, a real opinion | Stock openers, empty conclusions, inflated significance |
| Official / business | Албан бичиг, албан захидал | Formal, short, direct | Required letter formulas ("Иймд ... хүсье", "танилцуулж байна"), polite "Та" | Noun chains, "-ын хүрээнд", double verbs ("анхаарч ажиллах") |
| Casual / blog / social | Блог, пост, нийтлэл | Conversational, short sentences, spoken rhythm | -сан/-лаа endings, light particles (л, шүү, даа) when the author uses them | Lecture tone, bold-label lists, emoji headers |
| Academic | Эрдэм шинжилгээ | Neutral, precise | Passive voice, technical terms, "-ын хувьд" when it is precise | AI stock phrases and inflated claims only |

In **албан бичиг** do not flatten the text into casual Mongolian. Formal is correct there; robotic is not.

## Voice calibration

If the user gives a sample of their own writing, read it first. Note sentence length, how they end sentences (-в, -жээ, -лаа, -на, -даг), which connectives they like, whether they use «» or "" quotes, and whether they write "Та" or "та". Match those habits. A sample outranks the default style rules in this skill, including the dash rule.

## How much to change: count first

Do not rewrite text that is already fine. Before editing, count how many **distinct pattern types** (from the references) appear:

- **0–2 types → Light.** Fix only those spots. Leave everything else exactly as written.
- **3–5 types → Selective.** Fix the patterns and rework the worst sentences.
- **6+ types → Full rewrite.** Use the "read, look away, re-say" method on every paragraph.

If Python is available, `scripts/mn_markers.py` gives a quick mechanical count (run `python scripts/mn_markers.py <file>` from the skill folder, or pipe text in). It only catches surface markers. Your own reading of calques and rhythm matters more, so treat its number as a floor, not the verdict.

## Pattern references

Read the reference file for each group you need. Each pattern has a "watch for" list and a before/after example.

| File | Group | Examples of what it covers |
|---|---|---|
| [references/translationese.md](references/translationese.md) | Орчуулгын хэллэг (English calques) | "Энэ нь ... юм", "нэг" as an article, "-ын тусламжтайгаар", "-х боломжтой", "өөрийн/тэдний" + -аа, passive "-гдсан", English quote order, untranslated English words |
| [references/kantselyarit.md](references/kantselyarit.md) | Канцелярит (bureaucratic register) | -лт/-лтын chains, "арга хэмжээ авах", "зохион байгуулах ажлыг хэрэгжүүлэх", "-ын хүрээнд", "энэхүү/уг", "анхаарч ажиллах" |
| [references/ai-phrases.md](references/ai-phrases.md) | AI stock phrases | "чухал үүрэг гүйцэтгэдэг", "Өнөөгийн хурдацтай хөгжиж буй эрин үед", "Мөн түүнчлэн", "Дүгнэж хэлэхэд", rule of three, "зүгээр нэг ... биш, харин", chatbot leftovers |
| [references/grammar-overuse.md](references/grammar-overuse.md) | Нөхцөл, дагаврын хэтрэлт | Too many "нь", "болон/ба", "маш", plural -ууд/-үүд after quantifiers, pronoun subjects, identical sentence endings, uniform sentence length |
| [references/typography.md](references/typography.md) | Хэвлэлийн тэмдэг, хэлбэр | Em dashes, mixed quote styles, Title Case headings in Cyrillic, bold-label bullet lists, emoji |
| [references/false-positives.md](references/false-positives.md) | What is NOT an AI sign | Required official formulas, established loanwords, school-essay conventions, literary repetition |
| [references/examples.md](references/examples.md) | Full worked examples | Essay, official letter, social post |

Always read `false-positives.md` before a full rewrite.

## Process

1. **Register.** Decide the genre (table above).
2. **Scan.** Go through the pattern references and list every hit. Count distinct types and pick the level.
3. **Draft.** Rewrite at that level. For full rewrites, re-say each paragraph in Mongolian from its meaning, not from its English-shaped structure. Read it aloud in your head: would a Mongolian say this to another Mongolian?
4. **Audit.** Ask yourself two questions and answer briefly:
   - "Энэ бичвэрийг юу хиймэл оюуны бичсэн мэт харагдуулж байна вэ?" (What still makes this look AI-written?)
   - "Эх бичвэрт байхгүй баримт, нэр, тоо, эх сурвалж нэмсэн үү?" (Did I add any fact, name, number, or source that is not in the original?)
5. **Final.** Fix what the audit found. Check that the result contains no em dashes (—) or en dashes (–) unless the author's sample uses them, no "нь" doubled inside one clause, and no three consecutive sentences with the same ending.

## Output format

**Pasted text (default):**

1. **Илэрсэн зүйлс** (what was found): a short bullet list of the pattern types found, each with one quoted example from the text. Keep it to the patterns, not a lecture.
2. **Засварласан хувилбар** (the rewrite): the final text only, ready to copy.
3. **Гол өөрчлөлт** (optional, 2–4 bullets): only if a change could surprise the author, such as a cut attribution or a merged paragraph.

Write the labels and explanations in the language the user used with you; the rewrite itself is always Mongolian.

**File mode.** The user points at a file. Run the process, rewrite the prose in place, leave code, front matter, links, and data untouched, and report a short summary of what changed.

**Embedded mode.** Another task uses this skill as one step (for example "write this post, then humanize it"). Run the process silently and output only the final Mongolian text.

## Reference and credits

- Structure and the no-fabrication rule follow [blader/humanizer](https://github.com/blader/humanizer), based on Wikipedia's "Signs of AI writing".
- The signal-count levels and genre rules follow the Russian community skill humanizer-ru.
- The "read, look away, re-say" method follows the Chinese translationese essay at yage.ai.
- Mongolian-specific rules draw on Mongolian translation and style (найруулга зүй) teaching: "нь" overuse, pronoun economy, plural suffixes, "болон/ба" in lists, "маш", and varied sentence endings.
