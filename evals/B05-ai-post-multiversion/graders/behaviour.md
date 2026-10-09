---
type: llm
---

You are grading an editor's reply to a request to make Mongolian text read naturally.

Original text:
<<<
Хэд хэдэн хувилбар бичлээ. Өөрт тохирохыг нь сонгоорой.

---

**Хувилбар 1 (найрсаг, баяртай өнгө аяс)**

☕✨ ШИНЭ САЛБАР НЭЭГДЭЖ БАЙНА! ✨☕

Хүлээсэн цаг ирлээ! 🎉 [Кофе шопын нэр] Зайсан дахь шинэ салбараа албан ёсоор нээж байна!

📍 Хаяг: Зайсан, [тодорхой хаяг]
📅 Нээлт: [сар] дугаар сарын [өдөр]
⏰ Цаг: [эхлэх цаг] – [дуусах цаг]

Таны дуртай кофе, шинэхэн жигнэмэг, тухтай орчин одоо Зайсанд! 🥐☕

🎁 Нээлтийн өдрүүдэд:
✔️ Эхний 100 үйлчлүүлэгчид бялуу ҮНЭГҮЙ
✔️ Бүх кофе 20% хямдралтай
✔️ Хүссэн зүйлээ авбал шагналт сугалаанд оролцох боломжтой

Найз нөхдөө дагуулан ирж, шинэ салбарын анхны үйлчлүүлэгч нь болоорой! 💛

#кофе #Зайсан #шинэсалбар #нээлт #Улаанбаатар

---

**Хувилбар 2 (товч, цэвэр)**

Зайсанд шинэ салбар нээгдлээ ☕

[Кофе шопын нэр] одоо Зайсанд танай хажууд. Өглөөний кофе, үдийн завсар, оройн ярианд тохирсон тухтай орчин таныг хүлээж байна.

📍 [Хаяг]
🕘 Өдөр бүр [цаг]–[цаг]

Нээлтийн долоо хоногт кофе бүр 20% хямдралтай. Уулзацгаая! 🤍

#Зайсан #кофе #шинэсалбар

---

Дээрх хаалтанд бичсэн мэдээллийг (нэр, хаяг, огноо, хямдрал) өөрийн мэдээллээр солиорой. Хэрэв шопын өнгө аяс (залуу, тансаг, гэр бүлийн гэх мэт) эсвэл тодорхой урамшууллаа хэлвэл би постыг илүү тохируулж бичиж өгье.
>>>

Expected behaviour: Post genre: keep emoji, hashtags, exclamations. Remove only the lines addressed to the requester (first and last paragraph). Do not merge or drop the versions.

PASS only if all of these hold:
- The final text still contains "#Зайсан".
- The final text still contains "☕".
- The final text (not the explanation) no longer contains "Хэд хэдэн хувилбар бичлээ".
- The final text (not the explanation) no longer contains "өөрийн мэдээллээр солиорой".
- The final text keeps at least about 75% of the original's length (chat lines addressed to the requester do not count).
- Every number, name, date and quotation of the original is unchanged, and nothing is added that the original does not say (no new fact, source, example, opinion or person).
- The text is not made blunter, colder or lower in register: Та-forms, courtesy formulas, softeners (болов уу, гэж үзэж байна), particles (юм, билээ, шүү, даа) and honorifics of the original survive.
- Paired words, balanced clauses and fixed formal phrases are not cut as 'redundant'.

FAIL if any of them is violated. Judge the final rewritten text, not phrases the reply quotes from the original while explaining its changes.
