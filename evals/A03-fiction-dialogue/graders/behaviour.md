---
type: llm
---

You are grading an editor's reply to a request to make Mongolian text read naturally.

Original text:
<<<
— Чи хаашаа явж байгаа юм бэ? гэж ээж асуув.
>>>

Expected behaviour: Already native (dialogue dash, чи between family). Expect 'засвар шаардлагагүй'.

PASS only if all of these hold:
- The reply says the text needs no change, or changes at most a few words (about 0), each a clear error, not a style preference.
- Every number, name, date and quotation of the original is unchanged, and nothing is added that the original does not say (no new fact, source, example, opinion or person).
- The text is not made blunter, colder or lower in register: Та-forms, courtesy formulas, softeners (болов уу, гэж үзэж байна), particles (юм, билээ, шүү, даа) and honorifics of the original survive.
- Paired words, balanced clauses and fixed formal phrases are not cut as 'redundant'.

FAIL if any of them is violated. Judge the final rewritten text, not phrases the reply quotes from the original while explaining its changes.
