---
type: llm
---

You are grading an editor's reply to a request to make Mongolian text read naturally.

Original text:
<<<
Доорх нь мэдээний загвар юм. Тоон үзүүлэлтүүдийг албан ёсны эх сурвалжаас шалгаж оруулаарай.

**Өвлийн агаарын бохирдол эрс нэмэгдэж, иргэдийг анхаарахыг сануулж байна**

Өвлийн улирлын эхнээс хотын агаарын бохирдлын түвшин мэдэгдэхүйц өссөн байна. Нүүрсээр халаалт хийх, автомашины ялгарал нэмэгдэх, агаарын температур буурч утаа тархахгүй байх зэрэг олон хүчин зүйл энэ байдалд нөлөөлж байгаа гэж мэргэжилтнүүд тайлбарлаж байна.

Агаарын чанарын мэдээллээр, ялангуяа PM2.5 гэх жижиг тоосны агууламж хэт өндөр байгаа бөгөөд [өдөр, сар]-ын хугацаанд зарим дүүрэгт стандартын түвшнээс хэд дахин давсан үзүүлэлт бүртгэгджээ. [Эх сурвалж]-аас гаргасан мэдээллээр...

Эрүүл мэндийн мэргэжилтнүүд хүүхэд, өндөр настан, амьсгалын замын болон зүрх судасны өвчтэй хүмүүс бохирдлын нөлөөнд илүү мэдрэмтгий байдгийг анхааруулж байна. Тиймээс эдгээр хүмүүс шаардлагагүй үед гадаа удаан байхаас зайлсхийж, гэрийн агааржуулалтад анхаарч, маск зүүх талаар зөвлөж байна.

Мөн нүүрсний хэрэглээг хянах, чанартай түлш ашиглах, автомашины техникийн үзлэгт хамрагдах зэрэг арга хэмжээ авах шаардлагатай байна. Хот болон дүүргийн удирдлагууд хяналтаа сайжруулах талаар ажиллаж байгаагаа мэдэгдэв.

Иргэд агаарын чанарын мэдээллийг тогтмол шалгаж, өдрийн байдлаас хамааран үйл ажиллагаагаа төлөвлөхийг зөвлөж байна.
>>>

Expected behaviour: Remove the preamble addressed to the requester; keep placeholders (facts unknown); flag the unnamed 'мэргэжилтнүүд'; keep native news formulas.

PASS only if all of these hold:
- The final text still contains "[өдөр, сар]".
- The final text (not the explanation) no longer contains "Доорх нь мэдээний загвар юм".
- The reply points out "мэргэжилт" to the author (for example in an Анхаарах note).
- The final text keeps at least about 80% of the original's length (chat lines addressed to the requester do not count).
- Every number, name, date and quotation of the original is unchanged, and nothing is added that the original does not say (no new fact, source, example, opinion or person).
- The text is not made blunter, colder or lower in register: Та-forms, courtesy formulas, softeners (болов уу, гэж үзэж байна), particles (юм, билээ, шүү, даа) and honorifics of the original survive.
- Paired words, balanced clauses and fixed formal phrases are not cut as 'redundant'.

FAIL if any of them is violated. Judge the final rewritten text, not phrases the reply quotes from the original while explaining its changes.
