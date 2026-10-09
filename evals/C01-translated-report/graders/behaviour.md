---
type: llm
---

You are grading an editor's reply to a request to make Mongolian text read naturally.

Original text:
<<<
Өчигдөр сургууль дээр эцэг эхчүүдтэй уулзалт хийгдсэн. Уулзалтаар хүүхдүүдийн сурлагын асуудлууд хөндөгдсөн. Олон эцэг эхчүүд санал хэлсэн. Багш нар саналуудыг хүлээн авсан. Цаашид хамтын ажиллагааны сайжруулалт хийгдэх болно.
>>>

Expected behaviour: Full rewrite: уулзалт болсон, асуудлыг хөндөж, no plural after олон, сайжруулах болно; no invented actor.

PASS only if all of these hold:
- The final text still contains "Өчигдөр".
- The final text still contains "болно".
- The final text (not the explanation) no longer contains "уулзалт хийгдсэн".
- The final text (not the explanation) no longer contains "асуудлууд хөндөгдсөн".
- The final text (not the explanation) no longer contains "сайжруулалт хийгдэх".
- The final text (not the explanation) no longer contains "Олон эцэг эхчүүд".
- Every number, name, date and quotation of the original is unchanged, and nothing is added that the original does not say (no new fact, source, example, opinion or person).
- The text is not made blunter, colder or lower in register: Та-forms, courtesy formulas, softeners (болов уу, гэж үзэж байна), particles (юм, билээ, шүү, даа) and honorifics of the original survive.
- Paired words, balanced clauses and fixed formal phrases are not cut as 'redundant'.

FAIL if any of them is violated. Judge the final rewritten text, not phrases the reply quotes from the original while explaining its changes.
