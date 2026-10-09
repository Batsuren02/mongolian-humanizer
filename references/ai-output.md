# Чатботын бичвэрийн шинж (tells of current chatbot output)

Current chatbots do not write Mongolian translationese. On the translationese markers (noun + хийх, agentless passives, redundant plurals, -сан runs, stacked "нь") their output is at or below pre-2021 human writing, while professional translation is above it **[өгөгдөл]**. What does separate them from human writers is listed here.

**Evidence.** 83 replies from Claude Sonnet, Claude Haiku and GPT-5.5 to 15 ordinary requests (essay, official letter, news, Facebook post, report), compared with 139 human texts in the same five genres written before 2021. Rates are matched by genre; a tell is listed only when all three models show it and the gap is at least 1.5× with a 95% bootstrap interval. Ratios below are AI ÷ human. The human essays, letters and posts were blog essays, open letters and blog posts, so school essays and Facebook posts are not directly covered. **[өгөгдөл]** unless marked.

Contents: A1 chat framing · A2 placeholders · A3 connector piles · A4 generic voice · A5 "-х боломжтой" filler · A6 ghost experts · A7 template openers · A8 what AI leaves out (observe only) · What is not an AI tell

## A1. Chat framing (remove)

47–60% of replies open with a line to the requester, and Claude's replies close with an offer in 37–70% of cases. Human texts: 0%.

- Preamble: "Мэдээж. Иймэрхүү пост болно:", "Доорх нь мэдээний загвар юм.", "Хэд хэдэн хувилбар бичлээ.", "Доорх загварыг өөрийн ... засаж ашиглаарай."
- Outro: "Хэрэв ... хэрэгтэй бол хэлээрэй.", "...-аа өөрийн мэдээллээр солиорой.", word-count notes ("*(Ойролцоогоор 300 үг)*").

Remove them; they speak to the person who asked the chatbot, not to the text's reader. **Keep** a closing such as "Асуух зүйл байвал холбогдоорой" in a real service letter or post: it addresses the reader. When removing the wrapper is the only change, list it under Засвар хийсэн зүйлс and still give the clean text: the author needs a copy without it.

**Several versions in one reply** ("Хувилбар 1 ... Хувилбар 2 ..."): remove the wrapper lines, keep every version, and edit each lightly. Do not merge versions or pick one for the author unless asked. Labels such as "Хувилбар 1 (сэтгэл хөдлөлтэй)" are for the author's choice, not part of any post: keep them as plain labels or replace them with a "---" line, but keep the versions apart.

## A2. Placeholders (keep and list)

AI templates leave "[Нэр]", "[өдөр, сар]", "________" (53 per 1,000 words; human texts almost none). The facts are unknown, so **never fill them in**. Keep them, and list them in Анхаарах so the author sees what to complete. Specific details a chatbot made up to fill a template (a 20% discount, a prize draw, a trip length) are the same kind of thing: keep them, and ask the author in Анхаарах to confirm them, especially where they contradict each other.

## A3. Stacked sentence-initial connectors (ease)

| Sentence-initial word | Human | AI | Ratio |
|---|---|---|---|
| Мөн | 1.1 | 4.9 | 4.5× |
| Иймд | 0.3 | 2.0 | 7× |
| Юуны өмнө | 0.06 | 0.6 | 9.5× |

(per 100 sentences) Human writers instead start sentences with "Тэгээд" and "Гэтэл", which never opened a sentence in the AI sample. Two-thirds of AI essays have three or more connector openers covering a fifth of their sentences or more; none of the human texts in the five genres do, and 1% of human web pages.

**What counts:** additive and consequence connectors (Мөн, Мөн түүнчлэн, Түүнчлэн, Иймд, Иймээс, Тиймээс, Юуны өмнө, Үүнээс гадна, Үүний зэрэгцээ). **What does not:** ordinals that number the essay's points (Нэгдүгээрт, Хоёрдугаарт), the essay frame (Нэг талаас / Нөгөө талаас, Эцэст нь, Дүгнэж хэлэхэд), and contrast (Харин, Гэвч). "Юуны өмнө" or "Дараа нь" that opens a numbered series (followed by Хоёрдугаарт, Гуравдугаарт) works as an ordinal: do not count it. These were not more frequent in AI text, and schools teach them.

**Fix:** keep about one counted connector opener per five sentences. Remove the rest by joining the sentence to the one before it with a converb or "бөгөөд" (follow the merging rule in SKILL.md), or by simply dropping the connector when the logic is clear without it. Dropping is the default; when the link is causal ("Иймд"), drop the word rather than inventing a "тул" clause. Aim at or below the limit: merging lowers the sentence count. Keep "Иймд ...-ыг хүсье" in official letters: it is the request formula. Keep "Дүгнэж хэлэхэд" in an essay's conclusion.

> **Before:** Нөгөө талаас, хэт их ашиглах нь олон сөрөг үр дагавар авчирдаг. Юуны өмнө, унтах цаг багасч, сурлагын амжилт буурдаг. Мөн нийгмийн сүлжээнд бусадтай өөрийгөө харьцуулах нь өөртөө итгэх итгэлийг сулруулж, сэтгэл гутрал, түгшүүр үүсгэх эрсдэлтэй. Үүнээс гадна онлайн дээрх хэрүүл, дээрэлхэлт, тохиромжгүй агуулгад өртөх аюул ч бий.
>
> **After:** Нөгөө талаас, хэт их ашиглах нь олон сөрөг үр дагавар авчирдаг. Унтах цаг багасч, сурлагын амжилт буурдаг. Нийгмийн сүлжээнд бусадтай өөрийгөө харьцуулах нь өөртөө итгэх итгэлийг сулруулж, сэтгэл гутрал, түгшүүр үүсгэх эрсдэлтэй бөгөөд онлайн дээрх хэрүүл, дээрэлхэлт, тохиромжгүй агуулгад өртөх аюул ч бий.

(Before: a Claude Sonnet essay. After: **[дүгнэлт]**, needs a native speaker's review. Two connectors dropped, two sentences with different subjects joined with "бөгөөд"; no word of content changed.)

## A4. Generic voice: general truths and prescriptions (flag)

| Sentence ending | Human | AI | Ratio |
|---|---|---|---|
| -даг (general truth) | 4.1 | 10.6 | 2.6× |
| хэрэгтэй, шаардлагатай, боломжтой, чухал | 0.5 | 3.2 | 6.5× |

(per 100 sentences) In about two-thirds of AI essays at least 45% of sentences end this way; in human texts this happens in under 1%. This is the measurable side of V1 in voice.md (polished but empty).

**Do:** flag it in Анхаарах and point to where the author's own example, place or view would go. Where a sentence is a general truth the text does not need, you may cut its padding.
**Do not:** change modality to make it "livelier" (a general truth is not a past event; "хэрэгтэй" is not "хийнэ"), or invent the example yourself. "-даг юм" is a deliberate stance, used by human writers and never by the models measured: keep it.

## A5. "-х боломжтой" filler (ease when repeated)

2.9 per 1,000 words in AI text, 0.3 in human text (10×). One use usually carries meaning (opportunity, possibility: keep it, see translationese.md). When two or three pile into one passage, keep the ones that mean something and drop the rest.

> **Before:** Танай тамгын газрын зүгээс санал хүлээн авах боломжтой эсэхийг судлан, уулзалт товлох боломжтой эсэхээ мэдэгдэхийг хүсэж байна.
>
> **After:** Танай тамгын газрын зүгээс санал хүлээн авах эсэхийг судлан, уулзалт товлох боломжтой эсэхээ мэдэгдэхийг хүсэж байна.

(Before: a Claude Haiku letter. After: **[дүгнэлт]**, needs review.)

## A6. Ghost experts (flag)

"гэж мэргэжилтнүүд үзэж байна", "гэж судлаачид анхаарууллаа", "Мэргэжилтнүүдийн үзэж байгаагаар" with nobody named: 7× the human rate. A Mongolian journalism study also found ChatGPT news drafts inventing buyers, volumes and prices (Сандагсүрэн 2026, sources.md). **[эх сурвалж]**

Flag every unnamed expert, study or statistic in Анхаарах ("аль мэргэжилтэн болохыг нэрлэх, эсвэл энэ хэсгийг хасах"). Never supply a name, and never strengthen the claim while rewriting it.

## A7. Template openers and skeletons (observe; change only if asked)

All six AI answers to one education prompt opened "Боловсрол бол ..."; several essays opened "Өнөө үед ...". Human openers in the sample never repeated. AI essays also follow a fixed skeleton: Нэг талаас / Нөгөө талаас, ending in a balanced verdict ("сайн ч биш, муу ч биш"). These were too rare to measure reliably.

Mongolian schools teach such openers and the three-part essay, so do not cut them by default (register-and-tone.md). If the user asks for a fresher opening, suggest one built from the essay's own content.

## A8. What AI leaves out (observe only)

Human Mongolian has far more of these than current chatbot output:

| Feature | Human | AI |
|---|---|---|
| Particles л / даа, дээ / биз (per 1,000 words) | 7.8 / 2.8 / 0.6 | 1.7 / 0.4 / 0 |
| "-даг юм", "билээ" endings (per 100 sentences) | 0.5, 1.6 | 0, 0.4 |
| Questions (per 100 sentences) | 5.5 | 2.0 |
| "би" (per 1,000 words) | 5.4 | 1.7 |
| Sentences of 25+ words (per 100 sentences) | 18.6 | 2.6 |
| Sequential converb -аад (per 1,000 words) | 17.2 | 6.2 |
| Reported speech "гэж / гэсэн", simile "шиг" | about 2× and 10× more | |

**Never add these by default.** An absence is something to notice, not a fault to fill: adding particles, questions or "би" puts words in the author's mouth (other humanizers learned this the hard way). What you may do:

- Join short same-subject sentences into a longer converb chain where the merging rule allows. This restores length without adding content.
- Tell the author in Анхаарах that the text has no personal voice, and where it could go.
- Use particles only when the user asks for a more conversational text, or gives a sample of their own style.

## What is not an AI tell

Measured and found not to separate AI from human Mongolian, so not a reason to change anything:

- Translationese markers: noun + хийх, agentless passives, redundant plurals, -сан runs, stacked "нь". Fix them as style or correctness problems where they occur (translationese.md), not as proof of AI.
- Stock phrases once listed as "AI phrases": "чухал үүрэг гүйцэтгэ", "салшгүй хэсэг", "орчин үе", "зүгээр нэг ... биш", "Мөн түүнчлэн". Rare in both.
- Paired words: about 1.8× more in AI text, but driven by topic words. Keep protecting them.
- Dashes: Claude uses many more than human writers, GPT fewer. A model habit, handled by typography.md.
- Loanwords: no consistent difference.
