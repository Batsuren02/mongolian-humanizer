---
type: llm
---

You are grading an editor's reply to a request to make Mongolian text read naturally.

Original text:
<<<
Тэрэлж явсан аяллын тухай фэйсбүүк постын хэдэн хувилбарыг бичлээ. Сэтгэл зүрхэнд тань хамгийн ойр байгааг сонгоод, өөрийн хэлдэг үгээр бага зэрэг засаарай 😊

---

**Хувилбар 1 (сэтгэл хөдлөлтэй)**

Хотын шуургаас хэдэн хоногоор зугтаж, Тэрэлжийн цэнгэг агаарт амьсгалчихлаа 🏞️⛰️

Найзуудтайгаа хамт болсон энэ амралтын өдөр үнэхээр сайхан байлаа. Өглөө эрт сэрж, ногоон хөндийгөөр алхан, үдэш нь галын дэргэд дуулж хөгжилдсөн мөчүүд сэтгэлд маань удаан үлдэх байх 🔥🎶

Заримдаа зүгээр л цонхон дээрх утсаа орхиод, үнэнч найзуудтайгаа байгальд гарах л хэрэгтэй юм шиг санагдлаа. Дахиад очно оо, Тэрэлж! 💚

#Тэрэлж #амралт #найзууд #байгаль #Монгол

---

**Хувилбар 2 (богино, хөнгөн)**

Амралтын өдрийн төлөвлөгөө: Тэрэлж ✅
Найзууд ✅
Шарсан мах ✅
Цэлмэг тэнгэр ✅
Сэтгэл санаа сэргэсэн ✅

Ийм л амралт байх хэрэгтэй юм байна 😎🌲

#Тэрэлж #weekend #найзууд

---

**Хувилбар 3 (хошин өнгөөр)**

Бид Тэрэлжид "амрахаар" явсан гэж хэлж байсан ч, үнэндээ ихэнх нь хоол идэж, зураг авхуулж, түүнээс үлдсэн цагаараа "Хэдэн цагт гэртээ харих вэ?" гэж маргалдсан 😂🍖📸

Гэсэн ч нутгийн сайхан байгаль, найзуудынхаа инээд хөөр, шөнийн одтой тэнгэр бүгд үнэхээр зохилоо. Дахиад л явъя шүү, найзуудаа! 🏕️✨

#Тэрэлж #аялал #найзууд #амралт

---

Хэрэв та аяллынхаа тодорхой мөчүүдээ (жишээ нь морь унасан, Мэлхий хад үзсэн, майхантай хоносон г.м.) хэлбэл би постыг илүү хувийн, тодорхой болгож өгнө. Мөн найзуудаа tag хийх, байршил нэмэх зэргийг бас бичиж болно.
>>>

Expected behaviour: Three post versions wrapped in a chat preamble and a closing offer. Remove the two wrapper paragraphs; keep all three versions with their emoji and hashtags; at most light fixes inside.

PASS only if all of these hold:
- The final text still contains "Дахиад очно оо".
- The final text still contains "Шарсан мах".
- The final text still contains "Дахиад л явъя шүү".
- The final text still contains "😂".
- The final text still contains "#Тэрэлж".
- The final text (not the explanation) no longer contains "хэдэн хувилбарыг бичлээ".
- The final text (not the explanation) no longer contains "Хэрэв та аяллынхаа".
- The final text keeps at least about 70% of the original's length (chat lines addressed to the requester do not count).
- Every number, name, date and quotation of the original is unchanged, and nothing is added that the original does not say (no new fact, source, example, opinion or person).
- The text is not made blunter, colder or lower in register: Та-forms, courtesy formulas, softeners (болов уу, гэж үзэж байна), particles (юм, билээ, шүү, даа) and honorifics of the original survive.
- Paired words, balanced clauses and fixed formal phrases are not cut as 'redundant'.

FAIL if any of them is violated. Judge the final rewritten text, not phrases the reply quotes from the original while explaining its changes.
