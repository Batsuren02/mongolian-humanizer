---
type: llm
---

You are grading an editor's reply to a request to make Mongolian text read naturally.

Original text:
<<<
**Огноо:** [ОО.СС.ХХХХ]
**Дугаар:** [№]

**Хүргэх:** Баянзүрх дүүргийн Засаг даргын Тамгын газрын дарга [Нэр]-д

**Гарчиг:** 12-р хорооны гудамжны гэрэлтүүлгийг засварлах хүсэлт

Хүндэт [Нэр] аа,

Би Баянзүрх дүүргийн 12-р хорооны оршин суугч [Овог, нэр] бөгөөд [гудамжны нэр], [байрны хаяг]-д амьдардаг. Манай хорооны [гудамжны нэр]-ийн гэрэлтүүлэг [огноо]-нөөс хойш ажиллахгүй байна. Гудамжны гэрэлтүүлэг ажиллахгүй байснаар орой шөнийн цагаар явган зорчигчид, ялангуяа хүүхэд, өндөр настан ихээхэн эрсдэлтэй байдалд орж байна. Мөн замын хөдөлгөөн, хулгайн гэмт хэргийн эрсдэл нэмэгдсэн байна.

Энэ асуудлыг [хэдэн сар] болж байгаа бөгөөд [хорооны Засаг дарга / цахим хүсэлт] дамжуулан мэдэгдсэн боловч одоог хүртэл засвар хийгдээгүй байна.

Иймд дараах хүсэлтийг тавьж байна:
1. Гудамжны гэрэлтүүлгийн эвдрэлийг шалгаж, засварлах
2. Засварын ажлын хугацаа, явцын талаар хорооны иргэдэд мэдээлэх
3. Засвар хийх хүртэл түр зуурын гэрэлтүүлэг эсвэл хамгаалалтын арга хэмжээ авах боломжийг судлах

Засварын ажил хэзээ хийгдэх боломжтойг [X] ажлын өдрийн дотор мэдэгдэж өгнө үү. Хариуг [утас] эсвэл [имэйл] хаягаар хүлээн авах боломжтой.

Хавсралт: Гэрэлтүүлгийн эвдрэлтэй хэсгийн зураг [тоо] ширхэг

Хүндэтгэсэн,

[Нэр]
[Утас]
[Гарын үсэг]
[Огноо]
>>>

Expected behaviour: Official letter: fix noun+хийгдэх ('засвар хийгдээгүй', 'хэзээ хийгдэх'); keep 'Хүндэтгэсэн', the address line, and all placeholders; do not lower the register.

PASS only if all of these hold:
- The final text still contains "Хүндэтгэсэн".
- The final text still contains "Иймд".
- The final text (not the explanation) no longer contains "засвар хийгдээгүй".
- The final text keeps at least about 85% of the original's length (chat lines addressed to the requester do not count).
- Every number, name, date and quotation of the original is unchanged, and nothing is added that the original does not say (no new fact, source, example, opinion or person).
- The text is not made blunter, colder or lower in register: Та-forms, courtesy formulas, softeners (болов уу, гэж үзэж байна), particles (юм, билээ, шүү, даа) and honorifics of the original survive.
- Paired words, balanced clauses and fixed formal phrases are not cut as 'redundant'.

FAIL if any of them is violated. Judge the final rewritten text, not phrases the reply quotes from the original while explaining its changes.
