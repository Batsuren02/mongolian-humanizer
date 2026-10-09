---
type: llm
---

You are grading an editor's reply to a request to make Mongolian text read naturally.

Original text:
<<<
# Гар утас өсвөр насныханд үзүүлэх нөлөө

Өнөө үед гар утас өсвөр насныхны өдөр тутмын амьдралын салшгүй хэсэг болжээ. Сурагчдын дийлэнх нь өдөрт хэдэн цагийг утсан дээрээ өнгөрөөдөг. Гар утас нь хоёр талтай хэрэгсэл бөгөөд хэрхэн ашиглахаас хамаарч сайн ч, муу ч нөлөө үзүүлдэг.

Нэг талаас, гар утас нь суралцахад маш их тус дэмтэй. Өсвөр насныхан интернэтээр хэрэгтэй мэдээлэл хайж, онлайн хичээл үзэж, гадаад хэл сурах боломжтой. Мөн найз нөхөд, гэр бүлийнхэнтэйгээ хэзээ ч, хаанаас ч холбогдож чадна. Нийгмийн сүлжээгээр дамжуулан өөрийн авьяас чадвараа харуулж, шинэ танил тал нэмэгдүүлж байгаа залуус цөөнгүй.

Нөгөө талаас, хэт их ашиглах нь олон сөрөг үр дагавар авчирдаг. Юуны өмнө, унтах цаг багасч, сурлагын амжилт буурдаг. Судалгаагаар шөнө дөлөөр утас ашигладаг сурагчид өглөө ядарч, хичээлдээ анхаарлаа төвлөрүүлж чаддаггүй болохыг харуулсан байдаг. Мөн нийгмийн сүлжээнд бусадтай өөрийгөө харьцуулах нь өөртөө итгэх итгэлийг сулруулж, сэтгэл гутрал, түгшүүр үүсгэх эрсдэлтэй. Үүнээс гадна онлайн дээрх хэрүүл, дээрэлхэлт, тохиромжгүй агуулгад өртөх аюул ч бий.

Түүнчлэн утсанд хэт автах нь бодит харилцааг үгүйсгэдэг. Гэр бүлийнхэн хамт хоол идэж байхдаа ч хүн бүр утсаа ширтэж суудаг нь одоо нийтлэг үзэгдэл болсон. Үүний үр дүнд хүмүүсийн хоорондын ойр дотно харилцаа сулрах хандлагатай байна.

Иймд гол асуудал бол гар утсыг ашиглах эсэх биш, яаж ашиглах явдал юм. Өсвөр насныхан өөрсдөө цаг ашиглалтаа хянаж, унтахын өмнө утсаа тавьж, бодит харилцаанд цаг гаргах хэрэгтэй. Харин эцэг эх, багш нар хориглохын оронд тайлбарлаж, жишээ үзүүлж, хамтдаа дүрэм тогтоох нь илүү үр дүнтэй.

Дүгнэж хэлэхэд, гар утас бол зөв ашиглавал хөгжлийн хүчирхэг хэрэгсэл, буруу ашиглавал сурлага, эрүүл мэнд, харилцаанд хор хөнөөл учруулагч болдог. Тиймээс өсвөр насныхан технологийг захирдаг болохоос биш технологид захирагддаг болох ёсгүй.
>>>

Expected behaviour: Sentence-initial connectors (Нэг талаас, Мөн, Юуны өмнө, Үүнээс гадна, Түүнчлэн, Иймд, Тиймээс) piled up. Ease them, mostly by converb merges; keep the essay structure, heading and 'Дүгнэж хэлэхэд'; no register drop.

PASS only if all of these hold:
- The final text still contains "Дүгнэж хэлэхэд".
- Fewer sentences start with a stacked connector (Мөн, Иймд, Юуны өмнө, Түүнчлэн...); the sentences are joined or varied instead.
- The final text keeps at least about 85% of the original's length (chat lines addressed to the requester do not count).
- Every number, name, date and quotation of the original is unchanged, and nothing is added that the original does not say (no new fact, source, example, opinion or person).
- The text is not made blunter, colder or lower in register: Та-forms, courtesy formulas, softeners (болов уу, гэж үзэж байна), particles (юм, билээ, шүү, даа) and honorifics of the original survive.
- Paired words, balanced clauses and fixed formal phrases are not cut as 'redundant'.

FAIL if any of them is violated. Judge the final rewritten text, not phrases the reply quotes from the original while explaining its changes.
