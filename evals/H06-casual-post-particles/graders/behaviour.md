---
type: llm
---

You are grading an editor's reply to a request to make Mongolian text read naturally.

Original text:
<<<
Өчигдөр л гэхэд хүйтэн байсан, өнөөдөр бүр дулаарчихлаа даа. Тэгээд бид хэд гол руу гарлаа. Ус нь хүйтэн л байсан шүү, гэхдээ хүүхдүүд бол баярлаад л. Ийм өдөр жилд хэд ч байдаггүй биз дээ.
>>>

Expected behaviour: Casual post rich in particles (л, даа, шүү, биз) and тэгээд. Expect no change; never remove a particle. [Constructed: needs a native speaker's check.]

PASS only if all of these hold:
- The reply says the text needs no change, or changes at most a few words (about 1), each a clear error, not a style preference.
- The final text still contains "даа".
- The final text still contains "шүү".
- The final text still contains "биз дээ".
- The final text still contains "Тэгээд".
- Every number, name, date and quotation of the original is unchanged, and nothing is added that the original does not say (no new fact, source, example, opinion or person).
- The text is not made blunter, colder or lower in register: Та-forms, courtesy formulas, softeners (болов уу, гэж үзэж байна), particles (юм, билээ, шүү, даа) and honorifics of the original survive.
- Paired words, balanced clauses and fixed formal phrases are not cut as 'redundant'.

FAIL if any of them is violated. Judge the final rewritten text, not phrases the reply quotes from the original while explaining its changes.
