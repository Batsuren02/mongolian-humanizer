---
type: llm
---

You are grading an editor's reply to a request to make Mongolian text read naturally.

Original text:
<<<
Өнөөгийн хурдацтай хөгжиж буй технологийн эрин үед боловсрол нь хүний амьдралд маш чухал үүрэг гүйцэтгэдэг юм. Боловсрол нь зөвхөн мэдлэг олж авах хэрэгсэл биш, харин хувь хүний хөгжил, нийгмийн дэвшил, эдийн засгийн өсөлтийн үндэс суурь юм. Мөн түүнчлэн, олон судлаачдын үзэж байгаагаар чанартай боловсрол нь ирээдүйн амжилтын түлхүүр болдог. Түүгээр ч зогсохгүй, сурагчид өөрсдийн мэдлэг, ур чадвараа хөгжүүлэх боломжтой болдог. Дүгнэж хэлэхэд, боловсрол бол бидний ирээдүйн гэрэлт замын эхлэл юм.
>>>

Expected behaviour: Acceptable formal essay. At most the plural fix 'олон судлаачдын'; flag the unsourced attribution; keep every formula.

PASS only if all of these hold:
- The reply says the text needs no change, or changes at most a few words (about 3), each a clear error, not a style preference.
- The final text still contains "маш чухал үүрэг гүйцэтгэдэг юм".
- The final text still contains "Дүгнэж хэлэхэд".
- The final text still contains "боломжтой болдог".
- The reply points out "судлаач" to the author (for example in an Анхаарах note).
- Every number, name, date and quotation of the original is unchanged, and nothing is added that the original does not say (no new fact, source, example, opinion or person).
- The text is not made blunter, colder or lower in register: Та-forms, courtesy formulas, softeners (болов уу, гэж үзэж байна), particles (юм, билээ, шүү, даа) and honorifics of the original survive.
- Paired words, balanced clauses and fixed formal phrases are not cut as 'redundant'.

FAIL if any of them is violated. Judge the final rewritten text, not phrases the reply quotes from the original while explaining its changes.
