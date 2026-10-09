---
type: llm
---

You are grading an editor's reply to a request to make Mongolian text read naturally.

Original text:
<<<
2025 оны 9 дүгээр сарын 15-нд Улаанбаатар хотод болсон чуулга уулзалтад 23 улсын 140 гаруй төлөөлөгчид оролцсон. Чуулга уулзалтаар уур амьсгалын өөрчлөлтийн асуудлууд хэлэлцэгдсэн. "Бид хамтдаа ажиллах ёстой" гэж НҮБ-ын төлөөлөгч Мария Гарсиа хэлсэн. Уулзалтын төгсгөлд хамтарсан мэдэгдэлд гарын үсэг зурах ажиллагаа хийгдсэн.
>>>

Expected behaviour: Fix the quantifier plural, the agentless passive and 'ажиллагаа хийгдсэн'; keep every number, the name, and the quotation verbatim; add no actor or fact.

PASS only if all of these hold:
- The final text still contains "\"Бид хамтдаа ажиллах ёстой\"".
- The final text still contains "Мария Гарсиа".
- The final text still contains "НҮБ".
- The final text (not the explanation) no longer contains "төлөөлөгчид оролцсон".
- The final text (not the explanation) no longer contains "асуудлууд хэлэлцэгдсэн".
- The final text (not the explanation) no longer contains "ажиллагаа хийгдсэн".
- Every number, name, date and quotation of the original is unchanged, and nothing is added that the original does not say (no new fact, source, example, opinion or person).
- The text is not made blunter, colder or lower in register: Та-forms, courtesy formulas, softeners (болов уу, гэж үзэж байна), particles (юм, билээ, шүү, даа) and honorifics of the original survive.
- Paired words, balanced clauses and fixed formal phrases are not cut as 'redundant'.

FAIL if any of them is violated. Judge the final rewritten text, not phrases the reply quotes from the original while explaining its changes.
