---
type: llm
---

You are grading an editor's reply to a request to make Mongolian text read naturally.

Original text:
<<<
Танай байгууллагын үйл ажиллагааг сайжруулах чиглэлээр хамтран ажиллах асуудлыг судлан үзэх зорилгоор уулзалт зохион байгуулагдахаар төлөвлөгдөж байна. Энэхүү уулзалт нь хоёр талын хамтын ажиллагааг цаашид өргөжүүлэн бэхжүүлэхэд онцгой ач холбогдолтой юм.
>>>

Expected behaviour: Selective: only the double passive changes.

PASS only if all of these hold:
- The final text still contains "өргөжүүлэн бэхжүүлэх".
- The final text still contains "онцгой ач холбогдолтой юм".
- The final text still contains "Танай".
- The final text still contains "судлан үзэх".
- The final text (not the explanation) no longer contains "төлөвлөгдөж".
- Every number, name, date and quotation of the original is unchanged, and nothing is added that the original does not say (no new fact, source, example, opinion or person).
- The text is not made blunter, colder or lower in register: Та-forms, courtesy formulas, softeners (болов уу, гэж үзэж байна), particles (юм, билээ, шүү, даа) and honorifics of the original survive.
- Paired words, balanced clauses and fixed formal phrases are not cut as 'redundant'.

FAIL if any of them is violated. Judge the final rewritten text, not phrases the reply quotes from the original while explaining its changes.
