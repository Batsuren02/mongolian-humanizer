---
type: llm
---

You are grading an editor's reply to a request to make Mongolian text read naturally.

Original text:
<<<
Миний бодлоор хүүхдийг багаас нь ном уншиж сургах нь эцэг эхийн хамгийн чухал үүрэг юм. Ном уншдаг хүүхэд асуулт их асуудаг, бодож сэтгэх чадвар нь эрт хөгждөг гэж багш нар ярьдаг. Мэдээж бүх гэр бүлд номын сан байхгүй байж болох юм. Гэхдээ өдөрт ганц хуудас ч гэсэн хүүхэддээ уншиж өгвөл түүний ирээдүйд том хөрөнгө оруулалт болох болов уу гэж би боддог.
>>>

Expected behaviour: Personal stance with softeners. Expect no change; keep 'юм', 'болов уу', 'гэж би боддог', mid-text 'Мэдээж'.

PASS only if all of these hold:
- The reply says the text needs no change, or changes at most a few words (about 2), each a clear error, not a style preference.
- The final text still contains "болов уу".
- The final text still contains "гэж би боддог".
- The final text still contains "байж болох юм".
- The final text still contains "Мэдээж".
- Every number, name, date and quotation of the original is unchanged, and nothing is added that the original does not say (no new fact, source, example, opinion or person).
- The text is not made blunter, colder or lower in register: Та-forms, courtesy formulas, softeners (болов уу, гэж үзэж байна), particles (юм, билээ, шүү, даа) and honorifics of the original survive.
- Paired words, balanced clauses and fixed formal phrases are not cut as 'redundant'.

FAIL if any of them is violated. Judge the final rewritten text, not phrases the reply quotes from the original while explaining its changes.
