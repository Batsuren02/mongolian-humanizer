---
type: llm
---

You are grading an editor's reply to a request to make Mongolian text read naturally.

Original text:
<<<
Өчигдөр сургууль дээр эцэг эхчүүдтэй уулзалт болсон. Уулзалтаар хүүхдүүдийн сурлагын асуудлыг хөндөж, олон эцэг эх санал хэлсэн бөгөөд багш нар саналыг нь хүлээн авсан. Цаашид хамтын ажиллагааг сайжруулах болно.
>>>

Expected behaviour: The skill's own output fed back in. Expect 'засвар шаардлагагүй' or at most a word.

PASS only if all of these hold:
- The reply says the text needs no change, or changes at most a few words (about 3), each a clear error, not a style preference.
- Every number, name, date and quotation of the original is unchanged, and nothing is added that the original does not say (no new fact, source, example, opinion or person).
- The text is not made blunter, colder or lower in register: Та-forms, courtesy formulas, softeners (болов уу, гэж үзэж байна), particles (юм, билээ, шүү, даа) and honorifics of the original survive.
- Paired words, balanced clauses and fixed formal phrases are not cut as 'redundant'.

FAIL if any of them is violated. Judge the final rewritten text, not phrases the reply quotes from the original while explaining its changes.
