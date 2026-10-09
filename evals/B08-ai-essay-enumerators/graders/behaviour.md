---
type: llm
---

You are grading an editor's reply to a request to make Mongolian text read naturally.

Original text:
<<<
# Боловсролын ач холбогдол

Боловсрол бол хүний амьдралын хамгийн үнэтэй хөрөнгө оруулалт, нийгмийн хөгжлийн үндсэн суурь юм. Хүн төрсөн цагаасаа эхлэн суралцаж, мэдлэг, ур чадвар, үнэт зүйлсээ эзэмших замаар өөрийгөө төдийгүй эргэн тойрныхоо хүмүүсийг өөрчилдөг.

Юуны өмнө боловсрол нь хувь хүний хөгжлийг дэмждэг. Сайн боловсрол эзэмшсэн хүн шинэ мэдээллийг шүүн тунгааж, асуудлыг зөв шийдэж, хүссэн мэргэжлээрээ амжилттай ажиллах боломжтой болдог. Мөн боловсрол нь хүнийг өөртөө итгэлтэй, бие даасан болгож, амьдралын сорилтыг даван туулах хүч чадлыг өгдөг.

Хоёрдугаарт, боловсрол бол эдийн засгийн өсөлтийн гол хүчин зүйл юм. Боловсролтой, мэргэшсэн ажиллах хүч нь бүтээмжийг нэмэгдүүлж, шинэ технологи нэвтрүүлэх, шинэ бүтээн байгуулалт хийх боломжийг бүрдүүлдэг. Дэлхийн хөгжилтэй орнуудын туршлагаас харахад байгалийн баялгаас илүүтэй хүний нөөцөд хөрөнгө оруулсан улсууд урт хугацаанд тогтвортой хөгжиж ирсэн байдаг.

Гуравдугаарт, боловсрол нь нийгмийн нэгдмэл байдал, ардчилал, хүний эрхийг хамгаалахад чухал үүрэгтэй. Боловсролтой иргэд хууль эрх зүйгээ мэддэг, бусдын үзэл бодлыг хүндэлдэг, нийгмийн асуудалд идэвхтэй оролцдог тул нийгэмд ядуурал, ялгаварлан гадуурхалт, гэмт хэрэг багасдаг.

Түүнчлэн өнөөгийн хурдацтай өөрчлөгдөж буй дэлхийд боловсрол нь зөвхөн сургууль, их дээд сургуульд хязгаарлагдахгүй, насан туршийн үйл явц болж байна. Технологи огцом хөгжиж, зарим мэргэжил алга болж, шинэ мэргэжил бий болж буй энэ үед суралцах чадвар нь хамгийн чухал чадваруудын нэг болоод байна.

Эцэст нь хэлэхэд, боловсрол бол хувь хүн, гэр бүл, нийгэм, улс орны ирээдүйг тодорхойлогч хүчин зүйл юм. Иймд бид боловсролд хөрөнгө оруулж, чанартай, хүртээмжтэй боловсролыг хүн бүрт олгохыг нэн тэргүүнд чухалчлах ёстой.

Хэрэв танд тодорхой түвшинд (жишээ нь сурагч, оюутан) тохируулсан эсвэл өөр өнцгөөс бичсэн хувилбар хэрэгтэй бол хэлээрэй.
>>>

Expected behaviour: Remove the outro. Ease the sentence-initial connector pile (Юуны өмнө / Хоёрдугаарт / Гуравдугаарт / Түүнчлэн / Иймд) by merging with converbs; flag the generic -даг voice; never shorten or lower register.

PASS only if all of these hold:
- The final text (not the explanation) no longer contains "Хэрэв танд тодорхой түвшинд".
- Fewer sentences start with a stacked connector (Мөн, Иймд, Юуны өмнө, Түүнчлэн...); the sentences are joined or varied instead.
- The final text keeps at least about 80% of the original's length (chat lines addressed to the requester do not count).
- Every number, name, date and quotation of the original is unchanged, and nothing is added that the original does not say (no new fact, source, example, opinion or person).
- The text is not made blunter, colder or lower in register: Та-forms, courtesy formulas, softeners (болов уу, гэж үзэж байна), particles (юм, билээ, шүү, даа) and honorifics of the original survive.
- Paired words, balanced clauses and fixed formal phrases are not cut as 'redundant'.

FAIL if any of them is violated. Judge the final rewritten text, not phrases the reply quotes from the original while explaining its changes.
