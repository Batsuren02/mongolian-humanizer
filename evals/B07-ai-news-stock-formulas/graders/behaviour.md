---
type: llm
---

You are grading an editor's reply to a request to make Mongolian text read naturally.

Original text:
<<<
**Аймгийн наадмын хурдан морьдын уралдаан өргөн дэлгэр боллоо**

Аймгийн баяр наадмын хурдан морьдын уралдаан энэ сарын ___-ны өдөр ___ сумын нутагт өргөн дэлгэр зохион байгуулагдлаа. Уралдаанд аймаг, сумдын шилдэг уяачдын хурдан хүлгүүд нас насны ангиллаар тоосоо өргөж, наадамчин олныг баясгав.

Энэ жилийн уралдаанд азарга, их нас, соёолон, хязаалан, шүдлэн, даага зэрэг насны морьд уралдаж, уяачдын хөдөлмөр, хүүхэд унаачдын авхаалж самбаа, хурдан хүлгийн шандас сорьсон онцлогтой байлаа.

Уралдааны үеэр зохион байгуулагчдын зүгээс хүүхэд унаачдын аюулгүй байдлыг хангах, хамгаалалтын хувцас хэрэглэл өмсүүлэх, замын хяналт зохион байгуулалтыг сайжруулахад анхаарч ажилласан байна.

Наадамчин олон хурдан хүлгүүдийн тоосонд хийморь сэргээж, түрүүлж айрагдсан морьдын уяач, унаач хүүхдүүдэд баяр хүргэн, шагнал гардууллаа. Аймгийн наадмын морин уралдаан ийнхүү уламжлал, бахархал, хийморь золбоог илтгэсэн сайхан үйл явдал болон өндөрлөв.
>>>

Expected behaviour: AI text that is already native news style. 'өргөн дэлгэр зохион байгуулагдлаа', 'тоосоо өргөж', 'болон өндөрлөв' are stock newspaper formulas. Expect little or no change; must not 'fix' the passive.

PASS only if all of these hold:
- The reply says the text needs no change, or changes at most a few words (about 6), each a clear error, not a style preference.
- The final text still contains "зохион байгуулагдлаа".
- The final text still contains "өндөрлөв".
- Every number, name, date and quotation of the original is unchanged, and nothing is added that the original does not say (no new fact, source, example, opinion or person).
- The text is not made blunter, colder or lower in register: Та-forms, courtesy formulas, softeners (болов уу, гэж үзэж байна), particles (юм, билээ, шүү, даа) and honorifics of the original survive.
- Paired words, balanced clauses and fixed formal phrases are not cut as 'redundant'.

FAIL if any of them is violated. Judge the final rewritten text, not phrases the reply quotes from the original while explaining its changes.
