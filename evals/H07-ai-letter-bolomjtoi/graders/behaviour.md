---
type: llm
---

You are grading an editor's reply to a request to make Mongolian text read naturally.

Original text:
<<<
Доорх нь албан бичгийн төсөл юм. Огноо, дугаар, холбоо барих мэдээллээ өөрийн мэдээллээр солиоорой.

---

**[Их сургуулийн нэр]**
[Хаяг]
Утас: [дугаар] | Имэйл: [имэйл]

№ [дугаар]
[Огноо]

Хөвсгөл аймгийн Засаг даргын Тамгын газрын дарга
[Нэр] танд

**Аялал жуулчлалын чиглэлээр хамтран ажиллах тухай**

Хүндэт [Нэр] аа,

[Их сургуулийн нэр]-ийн нэрийн өмнөөс мэндчилгээ дэвшүүлье. Манай сургууль аялал жуулчлал, байгаль орчин, орон нутгийн соёлын чиглэлээр судалгаа, сургалтын ажил явуулдаг бөгөөд Хөвсгөл аймгийн хөгжил, аялал жуулчлалын салбарт хамтран ажиллах санал тавьж байна.

Танай аймаг Хөвсгөл нуур, Дархад, Цаатан зэрэг өвөрмөц байгалийн болон соёлын баялагтай тул дараах чиглэлээр хамтран ажиллах боломжтой гэж үзэж байна:

1. Орон нутгийн аялал жуулчлалын нөөцийн судалгаа, бүртгэл боловсруулах
2. Аялал жуулчлалын үйлчилгээний ажилтнуудад зориулсан богино хугацааны сургалт зохион байгуулах
3. Оюутнуудын дадлагын ажлыг аймгийн аялал жуулчлалын байгууллагуудтай хамтран зохион байгуулах
4. Орон нутгийн зочид буудал, гэр бүл аялал жуулчлалын үйлчилгээг сайжруулах зөвлөгөө өгөх
5. Аялал жуулчлалын хамтарсан арга хэмжээ, форум зохион байгуулах

Энэхүү хамтын ажиллагаа нь орон нутгийн хөгжил, ажлын байр, аялал жуулчлалын чанарыг дээшлүүлэхэд хувь нэмэр оруулна гэж найдаж байна. Танай тамгын газрын зүгээс санал хүлээн авах боломжтой эсэхийг судлан, уулзалт товлох боломжтой эсэхээ мэдэгдэхийг хүсэж байна.

Хамтран ажиллах санал, дэлгэрэнгүй мэдээллийг [холбоо барих хүний нэр, утас, имэйл]-ээр хүлээн авах боломжтой.

Хүндэтгэлтэйгээр,

[Албан тушаал]
[Нэр]
[Гарын үсэг]
>>>

Expected behaviour: Remove the preamble. '-х боломжтой' appears four times; ease only the filler uses (two in one sentence), keep the meaning-bearing 'хамтран ажиллах боломжтой'; keep all placeholders and the formal register.

PASS only if all of these hold:
- The final text still contains "хамтран ажиллах боломжтой".
- The final text still contains "Хүндэтгэлтэйгээр".
- The final text (not the explanation) no longer contains "Доорх нь албан бичгийн төсөл".
- Every [placeholder] of the original is kept, not filled with invented details.
- The final text keeps at least about 85% of the original's length (chat lines addressed to the requester do not count).
- Every number, name, date and quotation of the original is unchanged, and nothing is added that the original does not say (no new fact, source, example, opinion or person).
- The text is not made blunter, colder or lower in register: Та-forms, courtesy formulas, softeners (болов уу, гэж үзэж байна), particles (юм, билээ, шүү, даа) and honorifics of the original survive.
- Paired words, balanced clauses and fixed formal phrases are not cut as 'redundant'.

FAIL if any of them is violated. Judge the final rewritten text, not phrases the reply quotes from the original while explaining its changes.
