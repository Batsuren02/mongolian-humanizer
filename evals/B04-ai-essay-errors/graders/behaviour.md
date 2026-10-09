---
type: llm
---

You are grading an editor's reply to a request to make Mongolian text read naturally.

Original text:
<<<
# Миний нутаг

*Энэ бол жишээ эсээ. Нутгийнхаа нэр, өөрийн дурсамжийг оруулж, өөрийн үгээр солино уу.*

Миний нутаг бол [аймаг], [сум]-ын [нутгийн нэр] юм. Энэ газар намайг өсгөж, миний анхны дурсамжийг бүрдүүлсэн нутаг юм. Хаврын салхи, зуны бороо, намрын шаргал өвс, өвлийн цагаан цас гээд дөрвөн улирал бүр өөрийн онцлогтой. Хүн бүр өөрийн нутгаараа бахархдаг гэдэг нь миний хувьд ч үнэн.

Нутгийн минь байгаль маш өвөрмөц. Өргөн тал нутаг, хойд зүгт харагдах уулс, зүүн талаар урсдаг жижиг гол байдаг. Зуны улиралд тал нутаг ногоон өвс, цэцэгт дүүрэн болдог бол өвөл цас бүх тал нутгийг цагаан хувцасладаг. Бэлчээрт гарсан малын хонхны дуу, салхинд хөдөлж буй өвсний нам гүм нь энд л сонсогддог онцлог юм.

Гэхдээ миний нутгийн хамгийн гол баялаг бол хүмүүс. Малчид өглөө эрт босож, мал сүргээ бэлчээрт гаргадаг. Хөрш зэргэлдээ айлууд бие биедээ туслаж, хүнд цагт хамтдаа зүтгэдэг. Миний аав, ээж хоёр ч ийм сэтгэлгээтэй хүмүүс. Бид хүүхэд байхаасаа л хэн нэгэн ганцаараа биш, олон хүн хамтдаа ажиллах ёстойг мэдэрч өссөн.

Жил бүр зуны наадам болоход нутгийн бүх хүн цугладаг. Морин уралдаан, шагайн тоглоом, бөхийн барилдаан болоход хүүхэд, өндөр настан хамтдаа баяруулдаг. Энэ үед хүмүүс олон жилийн дараа уулзаж, хуучин найз нөхөдтэйгөө дахин таарч, инээлдэн ярилцдаг.

Би хүүхэд байхдаа нутгийн голд хамт усанд орж, гэрийн хашаанд бяруу, ишигтэй тоглож өсөж байсан. Тэр үеийн инээд хөөр одоо ч миний санаанд тод үлджээ.

Миний нутгийн хамгийн том асуудал бол залуучуудын хот руу шилжих явдал юм. Гэвч би нутгаа орхихгүй гэж бодож байна. Сурч мэдсэн зүйлээ нутагтаа хэрэгжүүлж, нутгийнхаа хөгжилд хувь нэмэр оруулахыг хичээнэ.

Миний нутаг бол миний үндэс, миний гэр юм.

Хэрэв та эсээний урт, өгүүлбэрийн түвшинг өөрчлөх хүсэлтэй бол хэлээрэй.
>>>

Expected behaviour: Remove the italic note and the outro addressed to the requester. Fix the malformed 'баяруулдаг'. Review '-жээ' used for the writer's own memory ('санаанд тод үлджээ'). Keep paired words and imagery. [Needs native check of the expected fixes.]

PASS only if all of these hold:
- The final text still contains "мал сүргээ".
- The final text still contains "инээд хөөр".
- The final text (not the explanation) no longer contains "баяруулдаг".
- The final text (not the explanation) no longer contains "Хэрэв та эсээний урт".
- The final text keeps at least about 80% of the original's length (chat lines addressed to the requester do not count).
- Every number, name, date and quotation of the original is unchanged, and nothing is added that the original does not say (no new fact, source, example, opinion or person).
- The text is not made blunter, colder or lower in register: Та-forms, courtesy formulas, softeners (болов уу, гэж үзэж байна), particles (юм, билээ, шүү, даа) and honorifics of the original survive.
- Paired words, balanced clauses and fixed formal phrases are not cut as 'redundant'.

FAIL if any of them is violated. Judge the final rewritten text, not phrases the reply quotes from the original while explaining its changes.
