---
type: llm
---

You are grading an editor's reply to a request to make Mongolian text read naturally.

Original text:
<<<
Доорх мэдээ загвар бөгөөд номын сангийн нэр, тоо, огноог бодит мэдээллээр солих хэрэгтэй.

**Улаанбаатарт шинэ нийтийн номын сан нээгдлээ**

[Дүүрэг]-т орших [номын сангийн нэр] нийтийн номын сан өнөөдөр албан ёсоор нээгдэж, хотын иргэдэд үнэгүй үйлчилж эхэллээ. Нээлтийн ажлын хүрээнд номын сангийн удирдлага, орон нутгийн иргэд, сурагчид оролцлоо.

Шинэ номын сан нь нийт [ ] м² талбайтай бөгөөд [ ] ширхэг ном, сэтгүүл, цахим хэрэгслийн нөөцтэй. Уншлагын танхим, хүүхдийн тусгай бүлэг, компьютер ашиглах талбай зэрэг орчинтой болсон байна.

Номын сангийн захирал [нэр] нээлтийн үеэр хэлэхдээ, "Бид ном уншихаас гадна иргэдийн мэдээлэл авах, суралцах, уулзалт хийх нэгдсэн орон зай болгохыг зорьж байна" гэв.

Номын сан долоо хоногийн [өдрүүд]-д [цаг]-аас [цаг] хүртэл ажиллана. Иргэд бүртгэлтэй болохын тулд иргэний үнэмлэхээ авч ирэх шаардлагатай бөгөөд бүртгэл нь үнэгүй байна.

Нийтийн номын сангууд хотын хүүхэд, залуусын уншлагын соёлыг дэмжих, нийгмийн оролцоог нэмэгдүүлэх үндсэн суурь болдог. Шинэ номын сан энэ чиглэлд чухал алхам болно гэж мэргэжилтнүүд үзэж байна.
>>>

Expected behaviour: Remove the preamble; keep every placeholder; flag 'гэж мэргэжилтнүүд үзэж байна' as unsourced; never invent an expert, a name or a number.

PASS only if all of these hold:
- The final text still contains "[номын сангийн нэр]".
- The final text still contains "[нэр]".
- The final text (not the explanation) no longer contains "Доорх мэдээ загвар".
- The reply points out "мэргэжилт" to the author (for example in an Анхаарах note).
- Every [placeholder] of the original is kept, not filled with invented details.
- The final text keeps at least about 80% of the original's length (chat lines addressed to the requester do not count).
- Every number, name, date and quotation of the original is unchanged, and nothing is added that the original does not say (no new fact, source, example, opinion or person).
- The text is not made blunter, colder or lower in register: Та-forms, courtesy formulas, softeners (болов уу, гэж үзэж байна), particles (юм, билээ, шүү, даа) and honorifics of the original survive.
- Paired words, balanced clauses and fixed formal phrases are not cut as 'redundant'.

FAIL if any of them is violated. Judge the final rewritten text, not phrases the reply quotes from the original while explaining its changes.
