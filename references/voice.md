# Хуурай, амьгүй хоолой (lifeless voice and chatbot residue)

Formal phrasing is not the AI problem in Mongolian. What Mongolian readers notice is different.

## V1. Polished but empty [эх сурвалж: Түшигт, writing.mn, 2026]

A Mongolian writing editor's critique of AI prose: it polishes everything until the text is dry, has no personal angle (өнцөг), lacks felt emotion, and repeats well-worn points everyone already knows.

How to recognise it:
- Every paragraph states a general truth; none says anything specific to the author, the place, or the case.
- No example, number, name, or experience, only categories ("хувь хүний хөгжил, нийгмийн дэвшил").
- The conclusion repeats the opening in grander words.

What to do:
- **Do not invent** examples, experiences, or opinions (hard rule).
- Keep every specific the text does have, and move it forward.
- In the "Анхаарах" note, tell the author where their own example or view would bring the text to life ("Энд өөрийн туршлагаас нэг жишээ оруулбал илүү амьд болно").
- If the user supplies their angle or details, weave them in.

## V2. Fluent but wrong [эх сурвалж: Left Behind 2026; MonCulture-Eval 2026; Thomson Foundation 2026]

Benchmarks find models write fluent Mongolian while the content is weaker than in English: confident but false explanations and answers that need manual checking. A Mongolian journalism study found ChatGPT news drafts inventing buyers, volumes and prices (Сандагсүрэн 2026). The benchmark that reports sanitised (outsider) cultural detail found it mostly in traditional script; in Cyrillic it was 1.3 to 5.4% of answers (MonCulture-Eval, Table 4), so do not assume it. A humanizer cannot fix facts, but it must not hide them under smoother prose.
- Flag claims that look invented: unsourced statistics, "судлаачдын үзэж байгаагаар" or "гэж мэргэжилтнүүд үзэж байна" with nobody named (7× more common in chatbot output, ai-output.md A6), quotes with no speaker.
- Never strengthen a doubtful claim while rewriting it.

## V3. Chatbot leftovers (remove when they address a chat user)

Whole preamble and closing paragraphs ("Доорх нь ... загвар юм.", "Хэрэв ... хэрэгтэй бол хэлээрэй.") are covered in ai-output.md A1. The phrases below are the same thing inside a sentence.

Replies to a chat user that leaked into the content. Remove them when they speak to "the user" rather than to the text's real reader:
- "Мэдээж!", "Мэдээжийн хэрэг!", "Маш сайн асуулт байна!"
- "Танд тусалсандаа баяртай байна", "Энэ нь танд тустай байх гэж найдаж байна"
- "Хэрэв нэмэлт мэдээлэл хэрэгтэй бол хэлээрэй", "Доор ...-ыг хүргэж байна"
- "Одоо ...-ыг дэлгэрэнгүй авч үзье", "Ингээд ...-ын талаар ярилцъя" (signposting)

**Keep:** "мэдээжийн хэрэг" used mid-text as ordinary "of course"; "Хэрэв нэмэлт мэдээлэл хэрэгтэй бол холбогдоорой" as a closing in a real service or business letter; signposting in a speech or lecture.

## V4. Over-claiming words [дүгнэлт, use judgment]

Hype adjectives with nothing behind them ("гайхалтай шийдэл", "дэвшилтэт", "инновацлаг") in ads and posts. Keep them if the author clearly wants promotional tone; otherwise prefer the concrete fact the text gives. In essays and official text, formal evaluative phrases ("чухал ач холбогдолтой") are normal; leave them.

## What is not a voice problem

- Formal formulas and school-essay structure (see register-and-tone.md).
- "Дүгнэж хэлэхэд" in an essay conclusion.
- A connective now and then, "Мөн түүнчлэн" included. Translators advise using connectives in official text, because Mongolian has many and they help it flow (unread.today). The problem is a pile at the start of sentences: chatbots open sentences with "Мөн" 4.5× and "Иймд" 7× as often as human writers [өгөгдөл]. Keep about one per five sentences (ai-output.md A3).
