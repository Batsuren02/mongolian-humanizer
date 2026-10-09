---
type: llm
---

You are grading an editor's reply to a request to make Mongolian text read naturally.

Original text:
<<<
Сургуулийн захирал Б.Сарантуяа танаа

Миний хүү Д.Тэмүүлэн 2025-2026 оны хичээлийн жилд танай сургуулийн 9б ангид суралцаж байна. Гэр бүлийн шалтгаанаар бид 11 дүгээр сарын 3-наас 14-нийг хүртэл хөдөө орон нутагт явах болсон тул хүүг энэ хугацаанд хичээлээс чөлөөлж өгөхийг Танаас хүсье. Хоцорсон хичээлээ нөхөх талаар ангийн багштай нь тохиролцоно.

Хүндэтгэсэн,
Эцэг Д.Ганбат
>>>

Expected behaviour: Native petition. Expect no change; never drop танаа/Танаас/хүсье/Хүндэтгэсэн.

PASS only if all of these hold:
- The reply says the text needs no change, or changes at most a few words (about 2), each a clear error, not a style preference.
- The final text still contains "танаа".
- The final text still contains "Танаас хүсье".
- The final text still contains "Хүндэтгэсэн".
- Every number, name, date and quotation of the original is unchanged, and nothing is added that the original does not say (no new fact, source, example, opinion or person).
- The text is not made blunter, colder or lower in register: Та-forms, courtesy formulas, softeners (болов уу, гэж үзэж байна), particles (юм, билээ, шүү, даа) and honorifics of the original survive.
- Paired words, balanced clauses and fixed formal phrases are not cut as 'redundant'.

FAIL if any of them is violated. Judge the final rewritten text, not phrases the reply quotes from the original while explaining its changes.
