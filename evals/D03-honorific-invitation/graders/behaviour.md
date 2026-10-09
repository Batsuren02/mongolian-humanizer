---
type: llm
---

You are grading an editor's reply to a request to make Mongolian text read naturally.

Original text:
<<<
Эрхэм хүндэт ахмад багш нар аа! Багшийн баярыг тохиолдуулан 2 дугаар сарын 1-ний өдөр болох хүндэтгэлийн хүлээн авалтад та бүхнийг морилон ирэхийг урьж байна. Та бүхний олон жил зүтгэсэн хөдөлмөрийг бид үргэлж дээдлэн хүндэлдэг билээ.
>>>

Expected behaviour: Honorific register addressing elders. Expect no change; never move 'морилон' or 'дээдлэн хүндэлдэг' down a rung.

PASS only if all of these hold:
- The reply says the text needs no change, or changes at most a few words (about 1), each a clear error, not a style preference.
- The final text still contains "Эрхэм хүндэт".
- The final text still contains "морилон".
- The final text still contains "билээ".
- Every number, name, date and quotation of the original is unchanged, and nothing is added that the original does not say (no new fact, source, example, opinion or person).
- The text is not made blunter, colder or lower in register: Та-forms, courtesy formulas, softeners (болов уу, гэж үзэж байна), particles (юм, билээ, шүү, даа) and honorifics of the original survive.
- Paired words, balanced clauses and fixed formal phrases are not cut as 'redundant'.

FAIL if any of them is violated. Judge the final rewritten text, not phrases the reply quotes from the original while explaining its changes.
