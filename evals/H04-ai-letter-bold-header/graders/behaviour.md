---
type: llm
---

You are grading an editor's reply to a request to make Mongolian text read naturally.

Original text:
<<<
Доорх загварыг өөрийн сургуулийн нэр, огноо, дугаар, хүлээн авагчийн нэрээр засаж ашиглаарай.

---

**Хөвсгөл аймгийн Засаг даргын Тамгын газарт**

**Хамтран ажиллах санал хүргүүлэх тухай**

Манай их сургууль нь аялал жуулчлалын салбарын хүний нөөцийн чадавхыг бэхжүүлэх, судалгаа, сургалт, дадлага, инновацад суурилсан хамтын ажиллагааг өргөжүүлэх зорилгоор Хөвсгөл аймгийн Засаг даргын Тамгын газартай хамтран ажиллах санал хүргүүлж байна.

Хөвсгөл аймаг нь байгалийн өвөрмөц тогтоц, соёлын үнэт өв, аялал жуулчлалын өндөр нөөц бололцоотой бүс нутаг тул тус салбарын тогтвортой хөгжлийг дэмжихэд их, дээд сургууль, орон нутгийн байгууллагын хамтын ажиллагаа чухал ач холбогдолтой гэж үзэж байна.

Иймд дараах чиглэлээр хамтран ажиллах боломжтой гэж санал болгож байна. Үүнд:

1. Аялал жуулчлалын чиглэлээр хамтарсан судалгаа, шинжилгээ хийх;
2. Оюутны дадлага, танилцах аялал, судалгааны ажлыг Хөвсгөл аймагт зохион байгуулах;
3. Орон нутгийн аялал жуулчлалын хүний нөөцийг чадавхжуулах сургалт, семинар зохион байгуулах;
4. Тогтвортой аялал жуулчлал, эко аялал, соёлын аялал жуулчлалын бүтээгдэхүүн хөгжүүлэхэд мэргэжил, арга зүйн дэмжлэг үзүүлэх;
5. Аймгийн аялал жуулчлалын бодлого, төлөвлөлт, сурталчилгааны ажилд судалгаанд суурилсан санал, зөвлөмж боловсруулах.

Дээрх чиглэлээр хамтын ажиллагааны уулзалт зохион байгуулж, цаашид хамтран ажиллах боломж, хэлбэрийг дэлгэрэнгүй ярилцах хүсэлтэй байна.

Та бүхнийг энэхүү саналыг хүлээн авч, хамтран ажиллах боломжийг судлан үзнэ гэдэгт итгэлтэй байна.

Хүндэтгэсэн,

**[Албан тушаал]**  
**[Нэр]**  
**[Их сургуулийн нэр]**  
**[Утас]**  
**[И-мэйл]**

**Огноо:** [он/сар/өдөр]  
**Дугаар:** [албан бичгийн дугаар]
>>>

Expected behaviour: Remove the instruction line to the requester. Official letter: keep 'Иймд', the numbered list, 'Хүндэтгэсэн' and every placeholder; the bold header may stay or become plain, but consistently.

PASS only if all of these hold:
- The final text still contains "Иймд".
- The final text still contains "Хүндэтгэсэн".
- The final text still contains "[Нэр]".
- The final text (not the explanation) no longer contains "Доорх загварыг".
- Every [placeholder] of the original is kept, not filled with invented details.
- The final text keeps at least about 85% of the original's length (chat lines addressed to the requester do not count).
- Every number, name, date and quotation of the original is unchanged, and nothing is added that the original does not say (no new fact, source, example, opinion or person).
- The text is not made blunter, colder or lower in register: Та-forms, courtesy formulas, softeners (болов уу, гэж үзэж байна), particles (юм, билээ, шүү, даа) and honorifics of the original survive.
- Paired words, balanced clauses and fixed formal phrases are not cut as 'redundant'.

FAIL if any of them is violated. Judge the final rewritten text, not phrases the reply quotes from the original while explaining its changes.
