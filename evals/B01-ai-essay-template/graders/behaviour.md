---
type: llm
---

You are grading an editor's reply to a request to make Mongolian text read naturally.

Original text:
<<<
# Гар утас ба өсвөр насныхан: давуу тал, эрсдэл

Орчин үед гар утас нь зөвхөн холбоо барих хэрэгсэл байхаа больж, өсвөр насныхны өдөр тутмын амьдралын салшгүй хэсэг болжээ. Өглөө сэрэхээс эхлээд орой унтах хүртэл тэд утсаа байнга гартаа барьдаг. Энэ нь тэдний сурлага, сэтгэл зүй, нийгмийн харилцаанд олон талын нөлөө үзүүлж байгаа бөгөөд эерэг болон сөрөг талыг нь тэнцүү авч үзэх шаардлагатай.

Нэг талаас, гар утас өсвөр насныханд мэдээлэл олж авах, суралцах өргөн боломж олгодог. Интернэтээр дамжуулан тэд хичээлийн материал хайх, гадаад хэл сурах, онлайн сургалтад хамрагдах боломжтой. Мөн найз нөхөд, гэр бүлийнхэнтэйгээ хүссэн үедээ холбогдож, өөрсдийн сонирхол, авьяасаа нийгмийн сүлжээгээр дамжуулан харуулах боломж бүрдсэн. Энэ утгаараа утас нь мэдлэг, бүтээлч чадварыг хөгжүүлэхэд ихээхэн тусалдаг.

Нөгөө талаас, утасны хэт их хэрэглээ нь ноцтой сөрөг үр дагавар авчирдаг. Юуны өмнө, байнга мэдэгдэл ирэх, видео болон тоглоом үзэх нь анхаарал төвлөрөх чадварыг сулруулж, хичээлийн үр дүнд муугаар нөлөөлдөг. Дараа нь, олон цагаар дэлгэц ширтэх нь нойрны хэв маягийг алдагдуулж, нүд болон нурууны эрүүл мэндэд хор хохирол учруулдаг. Түүнчлэн, нийгмийн сүлжээн дэх бусдын "төгс" амьдралтай өөрийгөө харьцуулах нь өөртөө итгэх итгэлийг бууруулж, түгшүүр, сэтгэлийн дарамтыг нэмэгдүүлдэг гэж судлаачид анхаарууллаа. Мөн цахим дээрэлхэлт нь өсвөр насныхны сэтгэл зүйд хүндээр тусдаг эрсдэл юм.

Эцэст нь, утас нь амьд харилцааг орлох хандлага ажиглагддаг. Өсвөр насныхан бие биетэйгээ нүүр тулан ярилцахаас илүү мессеж бичих болсноор нийгмийн ур чадвар, сэтгэл хөдлөлөө илэрхийлэх чадвар нь хөгжихгүй байх эрсдэлтэй.

Дүгнэхэд, гар утас нь өөрөө сайн ч биш, муу ч биш. Түүнийг хэрхэн ашиглахаас үр нөлөө нь шалтгаална. Иймд эцэг эх, багш нар өсвөр насныхантай нээлттэй ярилцаж, дэлгэцийн хугацааг зохистой тогтоох, утасгүй цаг гаргах зэрэг дадлыг хамтдаа төлөвшүүлэх нь чухал. Харин өсвөр насныхан өөрсдөө утсаа мэдлэг, хөгжлийн хэрэгсэл болгон ухаалгаар хэрэглэж сурах нь хамгийн гол нь юм.

*(Ойролцоогоор 300 үг)*

Хэрэв тодорхой статистик, судалгааны эшлэл нэмж, эсвэл эсээг илүү өөр өнцгөөс (жишээ нь Монгол өсвөр насныхны нөхцөл байдалд төвлөрсөн) бичих бол хэлээрэй.
>>>

Expected behaviour: Remove the chat outro and the word-count note; flag 'судлаачид анхаарууллаа' as unsourced; do not shorten the essay or flatten its formal register; connector pile and false balance ('сайн ч биш, муу ч биш') may be eased, not cut.

PASS only if all of these hold:
- The final text (not the explanation) no longer contains "Хэрэв тодорхой статистик".
- The final text (not the explanation) no longer contains "Ойролцоогоор 300 үг".
- The reply points out "судлаач" to the author (for example in an Анхаарах note).
- The final text keeps at least about 80% of the original's length (chat lines addressed to the requester do not count).
- Every number, name, date and quotation of the original is unchanged, and nothing is added that the original does not say (no new fact, source, example, opinion or person).
- The text is not made blunter, colder or lower in register: Та-forms, courtesy formulas, softeners (болов уу, гэж үзэж байна), particles (юм, билээ, шүү, даа) and honorifics of the original survive.
- Paired words, balanced clauses and fixed formal phrases are not cut as 'redundant'.

FAIL if any of them is violated. Judge the final rewritten text, not phrases the reply quotes from the original while explaining its changes.
