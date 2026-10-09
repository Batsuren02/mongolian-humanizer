---
type: llm
---

You are grading an editor's reply to a request to make Mongolian text read naturally.

Original text:
<<<
Доорх нь 10-р ангийн сурагчид тохирсон жишээ эсээ юм. [сумын нэр] гэсэн хэсэгт өөрийн нутгийнхаа нэрийг тавьж, өөрийн туршлагаар хувиргаж бичвэл илүү сайн болно.

**Миний нутаг**

Миний нутаг бол [сумын нэр] юм. Энэ нутаг хангайн уулс, ногоон бэлчир, цэвэр горхи, урсгал голоороо сайхан. Би ийм газарт төрж өссөндөө их бахархдаг.

Манай нутгийн байгаль маш баян. Зун цагт тал хээр ногоорч, олон төрлийн цэцэг ургадаг. Хавар нь малын шинэ төллөр, бяцхан зулзага хурга тэмүүлэн үсрэх нь харахад сайхан. Өвөл цагт цас ихтэй үед бүх газар цагаан өнгөтэй болж, хүүхдүүд гулгуур тоглодог. Би байгалийн эдгээр өөрчлөлтийг хамгийн их хайрладаг.

Нутгийн иргэд хөдөлмөрч, зочломтгой. Ихэнх өрх мал аж ахуй эрхэлдэг бөгөөд малчид өглөөнөөс орой хүртэл малын хашаа, бэлчээрт ажилладаг. Миний ээж, аав ч мал аж ахуйгаар амьдардаг. Тэднээс би хөдөлмөр, хариуцлагын утгыг сурсан.

Манай нутагт уламжлалт баяр наадам ихээр тохиодог. Сумын наадам үед бөхийн барилдаан, морин уралдаан, сур харвааны тэмцээн болдог. Энэ үед бүх хүн нэгдэж, хамтдаа баярладаг нь нутгийн минь хамгийн сайхан уламжлал юм.

Харин манай нутагт сургууль, эрүүл мэндийн байгууллага, интернэт холбоо зэрэг үйлчилгээ хязгаарлагдмал байдаг. Тиймээс залуус хот руу явах нь цөөнгүй. Би ирээдүйдээ сурч мэдсэн зүйлээ нутагтаа хэрэгжүүлэхийг хүсдэг.

Миний нутаг бол миний хамгийн том эх сурвалж юм. Миний хүүхдийн дурсамж, ээж аавын хөдөлмөр, нутгийн хүмүүсийн сайхан сэтгэл бүгд энд байдаг. Би ирээдүйдээ энэ нутгийнхаа хөгжилд хувь нэмэр оруулах зорилготой явна.
>>>

Expected behaviour: Remove the preamble to the requester; keep the placeholder [сумын нэр]; fix 'төллөр'. Generic -даг voice: flag it and suggest where the student's own example would go; do not invent examples, places or numbers.

PASS only if all of these hold:
- The final text still contains "[сумын нэр]".
- The final text (not the explanation) no longer contains "Доорх нь 10-р ангийн".
- The reply tells the author the voice is generic and suggests where their own example or view would go, without writing that example for them.
- The final text keeps at least about 80% of the original's length (chat lines addressed to the requester do not count).
- Every number, name, date and quotation of the original is unchanged, and nothing is added that the original does not say (no new fact, source, example, opinion or person).
- The text is not made blunter, colder or lower in register: Та-forms, courtesy formulas, softeners (болов уу, гэж үзэж байна), particles (юм, билээ, шүү, даа) and honorifics of the original survive.
- Paired words, balanced clauses and fixed formal phrases are not cut as 'redundant'.

FAIL if any of them is violated. Judge the final rewritten text, not phrases the reply quotes from the original while explaining its changes.
