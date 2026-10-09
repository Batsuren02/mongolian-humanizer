---
type: llm
---

You are grading an editor's reply to a request to make Mongolian text read naturally.

Original text:
<<<
Өчигдөр сургууль дээр эцэг эхчүүдтэй уулзалт хийгдсэн. Уулзалтаар хүүхдүүдийн сурлагын асуудлууд хөндөгдсөн. Олон эцэг эхчүүд санал хэлсэн. Багш нар саналуудыг хүлээн авсан. Цаашид хамтын ажиллагааны сайжруулалт хийгдэх болно.
>>>

Expected behaviour: Embedded/final-only request: output only the Mongolian text, no section labels.

PASS only if all of these hold:
- The final text (not the explanation) no longer contains "Засвар хийсэн зүйлс".
- The final text (not the explanation) no longer contains "Дүгнэлт".
- The final text (not the explanation) no longer contains "уулзалт хийгдсэн".
- The reply is only the final Mongolian text: no headings, labels or explanations.
- Every number, name, date and quotation of the original is unchanged, and nothing is added that the original does not say (no new fact, source, example, opinion or person).
- The text is not made blunter, colder or lower in register: Та-forms, courtesy formulas, softeners (болов уу, гэж үзэж байна), particles (юм, билээ, шүү, даа) and honorifics of the original survive.
- Paired words, balanced clauses and fixed formal phrases are not cut as 'redundant'.

FAIL if any of them is violated. Judge the final rewritten text, not phrases the reply quotes from the original while explaining its changes.
