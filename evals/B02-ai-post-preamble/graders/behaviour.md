---
type: llm
---

You are grading an editor's reply to a request to make Mongolian text read naturally.

Original text:
<<<
Мэдээж. Иймэрхүү пост болно:

Амралтын өдрөөр найзуудтайгаа Тэрэлж яваад, хотын завгүй хэмнэлээс түр ч гэсэн холдож сайхан амарлаа. Цэвэр агаар, уул ус, инээд хөөр, дурсамж дүүрэн өдрүүд байлаа. Ийм энгийн мөртлөө үнэ цэнтэй мөчүүд л хамгийн гоё нь юм байна. 🏞️

Найзуудтайгаа хамт өнгөрүүлсэн энэ аялал нэг сайхан дурсамж болон үлдлээ.
>>>

Expected behaviour: Remove the chat preamble 'Мэдээж. Иймэрхүү пост болно:'; keep the emoji and the paired word 'инээд хөөр'; otherwise light.

PASS only if all of these hold:
- The final text still contains "инээд хөөр".
- The final text still contains "🏞️".
- The final text (not the explanation) no longer contains "Иймэрхүү пост болно".
- The final text keeps at least about 70% of the original's length (chat lines addressed to the requester do not count).
- Every number, name, date and quotation of the original is unchanged, and nothing is added that the original does not say (no new fact, source, example, opinion or person).
- The text is not made blunter, colder or lower in register: Та-forms, courtesy formulas, softeners (болов уу, гэж үзэж байна), particles (юм, билээ, шүү, даа) and honorifics of the original survive.
- Paired words, balanced clauses and fixed formal phrases are not cut as 'redundant'.

FAIL if any of them is violated. Judge the final rewritten text, not phrases the reply quotes from the original while explaining its changes.
